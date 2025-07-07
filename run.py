import re
import logging
import os
import sys
from typing import Dict, List
from dotenv import load_dotenv
from langchain_openai import OpenAI, ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate

# Add parent directory to path to import re_act_actions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompt_utils import create_react_prompt, get_prompt_version
from tools import tools

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# LoadOpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Anthropic API Key
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")


################################################################################
# Initialize LLM client
################################################################################
# llm = ChatAnthropic(temperature=0, anthropic_api_key=anthropic_api_key, model="claude-3-5-sonnet-20241022")
llm = ChatAnthropic(temperature=0, anthropic_api_key=anthropic_api_key, model="claude-3-5-haiku-20241022")
# llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model="gpt-4.1-nano")
# llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model="gpt-4.1-mini")
#################################################################################

def format_param_description(param_info: List[Dict]) -> str:
    """
    함수의 파라미터 정보를 description 문자열로 변환

    Args:
        param_info (List[Dict]): 파라미터 정보를 담은 딕셔너리의 리스트
            [{
                "name": str,      # 파라미터 이름
                "type": str,      # 파라미터 타입
                "description": str # 파라미터 설명
            }]

    Returns:
        str: 포맷팅된 파라미터 설명 문자열
    """
    descriptions = []
    for param in param_info:
        descriptions.append(f"'{param.get("name")} ({param.get("type")})': {param.get("description")}")
    
    return ", ".join(descriptions)

def parse_llm_output(llm_output: str) -> Dict[str, str]:
    """Parse LLM output to extract action and action input"""
    if "Final Answer:" in llm_output:
        return {
            "type": "final_answer",
            "answer": llm_output.split("Final Answer:")[-1].strip()
        }
    
    # Look for Action and Action Input
    action_match = re.search(r"Action: (.*?)(?:\n|$)", llm_output)
    
    if action_match:
        # Split actions by '&&' and strip whitespace
        actions = [action.strip() for action in action_match.group(1).split("&&")]
        print(f"### actions: {actions}")
        return {
            "type": "action",
            "actions": actions
        }
    
    return {
        "type": "error",
        "error": f"Could not parse LLM output: {llm_output}"
    }

def execute_tool(action: str) -> str:
    """Execute a tool with the given input"""
    # print(f"[execute_tool] {action}")
    try:
        # 직접 action 문자열을 eval하여 실행
        # tools 딕셔너리의 함수들만 사용 가능하도록 제한된 환경에서 실행
        allowed_globals = {name: info["func"] for name, info in tools.items()}
        result = eval(action, {"__builtins__": {}}, allowed_globals)
        return str(result)
    except Exception as e:
        logger.error(f"Error executing action {action}: {str(e)}")
        return f"Error executing action: {str(e)}"


def run_react_agent(query: str, max_iterations: int = 10) -> str:
    """
    Run the ReAct agent with the given query
    
    Args:
        query (str): The question to ask the agent
        max_iterations (int): Maximum number of reasoning iterations
        
    Returns:
        str: The agent's response
    """
    try:
        conversation_history = []
        agent_scratchpad = ""
        iters = 1
        
        while max_iterations > iters:
            iters += 1
            # Create the prompt for this iteration
            prompt_template = create_react_prompt(tools, conversation_history)
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["input", "agent_scratchpad"]
            )
            
            print(f"************[prompt]************\n{prompt.format(input=query, agent_scratchpad=agent_scratchpad)}\n********************************")
            
            # Get LLM response
            llm_response = llm.invoke(prompt.format(input=query, agent_scratchpad=agent_scratchpad))
            # ChatOpenAI는 AIMessage 객체를 반환하므로 content를 추출
            llm_response_text = llm_response.content if hasattr(llm_response, 'content') else str(llm_response)
            print(f"----------[llm_response]----------\n{llm_response_text}\n----------------------------------")
            
            # Parse the response
            parsed = parse_llm_output(llm_response_text)
            # print(f"### parsed: {parsed}")
            
            if parsed["type"] == "final_answer":
                print(f"--------[agent_scratchpad]--------\n{agent_scratchpad}\n{llm_response_text}\n---------------------------------")
                return parsed["answer"]
            
            elif parsed["type"] == "action":
                # Execute the tool
                observation = ""
                for action in parsed["actions"]:
                    result = execute_tool(action)
                    result_data = eval(result)
                    if isinstance(result_data, list):
                        # Handle list of dictionaries
                        if result_data:  # Check if list is not empty
                            result_md = "| " + " | ".join(result_data[0].keys()) + " |\n"
                            result_md += "| " + " | ".join(["---"] * len(result_data[0].keys())) + " |\n"
                            for row in result_data:
                                result_md += "| " + " | ".join(str(v) for v in row.values()) + " |\n"
                            result_md = result_md.rstrip()  # Remove trailing newline
                        else:
                            result_md = "Empty result list"
                    elif isinstance(result_data, dict):
                        result_md = str(result_data)
                        # Handle single dictionary
                        result_md = "| " + " | ".join(result_data.keys()) + " |\n"
                        result_md += "| " + " | ".join(["---"] * len(result_data.keys())) + " |\n"
                        result_md += "| " + " | ".join(str(v) for v in result_data.values()) + " |"
                    else:
                        result_md = str(result_data)
                    observation += result_md + "\n"
                    
                print(f"----------[observation]----------\n{observation}\n---------------------------------")
                
                # Add to scratchpad
                agent_scratchpad += f"\n{llm_response_text}\nObservation: \n{observation}\n"
                
                # Add to conversation history for context
                conversation_history.append(f"Actions: {', '.join(parsed['actions'])}\nObservation: {observation}")
                
            else:
                return f"Error: {parsed['error']}"
        
        return f"Error: Maximum iterations ({max_iterations}) reached without finding a final answer."
        
    except Exception as e:
        logger.error(f"Error running ReAct agent: {str(e)}")
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # 프롬프트 버전 정보 출력
    print(f"{'='*10}Using prompt version: {get_prompt_version()}{'='*10}")
    
    # Test with different types of queries
    test_queries = [
        # "What is 15 * 23?",
        # "Calculate the square root of 144",
        # "What is the capital of France?",
        # "Tell me about Samsung Electronics stock code",
        "삼성전자 종목 코드 알려줘.",
        # "compare the bigger: 15 * 23 and the square root of 144",
        # "삼성전자 회사 정보 알려줘.",
        # "삼성전자 거래 정보 요약해줘.",
        # "삼성전자 외국인 거래량 알려줘?",
        # "삼성전자 주가는 얼마인가요?"
        # "삼성전자 주가랑 외국인 거래량 알려줘",
        # "2 * 15 * 300 은 삼성전자 외국인 매수량보다 많아?"
        # "삼성전자 거래량 정보 알려줘.",
        # "삼성전자 회사 정보랑 외국인 거래량 알려줘"
        # "2 * 15 랑 15 * 2 의 차이는 얼마야?",
        # "2 * 15 * 30 은 삼성전자 설립 년도보다 커?",
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        result = run_react_agent(query)
        print(f"\n{'='*50}")
        print(f"Final Answer:\n{result}")
        print(f"{'='*50}")