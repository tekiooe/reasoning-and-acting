import re
import json
import logging
import os
import sys
from typing import Dict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

from datetime import datetime

# Add parent directory to path to import re_act_actions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompt_utils import get_prompt_version, load_prompt_template
from tools import tools
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


# Initialize LLM client
openai_models = ["gpt-4.1-mini", "gpt-4.1-nano", "gpt-4.1", "gpt-4.5-preview", "gpt-4o", "gpt-4o-mini"]
openai_reasoning_models = ["o1", "o1-pro", "o3-pro", "o3", "o3-deep-research", "o4-mini", "o4-mini-deep-research", "o3-mini", "o1-mini"]
gemini_modles = ["gemini-2.5-flash", "gemini-2.5-flash-lite-preview-06-17"]
claude_models = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"]

print(f"************[ {config.model_name} ]************")
if config.model_name in openai_reasoning_models:
    llm = ChatOpenAI(openai_api_key=config.openai_api_key, model=config.model_name)
elif config.model_name in openai_models + openai_reasoning_models:
    llm = ChatOpenAI(temperature=config.temperature, openai_api_key=config.openai_api_key, model=config.model_name)
elif config.model_name in gemini_modles:
    if config.is_reasoning:
        llm = ChatGoogleGenerativeAI(temperature=config.temperature, google_api_key=config.google_api_key, model=config.model_name, additional_kwargs={"reasoning_mode": "enabled"})
    else:
        llm = ChatGoogleGenerativeAI(temperature=config.temperature, google_api_key=config.google_api_key, model=config.model_name)
elif config.model_name in claude_models:
    llm = ChatAnthropic(temperature=config.temperature, anthropic_api_key=config.anthropic_api_key, model=config.model_name)
else:
    raise ValueError(f"Unrecognized model name: {config.model_name}")


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
        descriptions.append(
            f"'{param.get("name")} ({param.get("type")})': {param.get("description")}"
        )

    return ", ".join(descriptions)


def parse_llm_output(llm_output: str) -> Dict[str, str]:
    """Parse LLM output to extract action and action input"""
    if "Final Answer:" in llm_output:
        return {
            "type": "final_answer",
            "answer": llm_output.split("Final Answer:")[-1].strip(),
        }
    elif "⟦status:start:answer⟧" in llm_output:
        return {
            "type": "final_answer",
            "answer": llm_output.split("⟦status:start:answer⟧")[-1]
            .split("⟦status:end:answer⟧")[0]
            .strip(),
        }

    # Look for Action and Action Input
    action_match = re.search(r"Action: (.*?)(?:\n|$)", llm_output)

    if action_match:
        # prompt v7 이전 버전용
        actions = [action.strip() for action in action_match.group(1).split("&&")]
        return {"type": "action", "actions": actions}
    elif (
        "⟦status:start:thought⟧" in llm_output and "⟦status:start:action⟧" in llm_output
    ):
        actions = json.loads(
                    llm_output.split("⟦status:start:action⟧")[-1]
                    .split("⟦status:end:action⟧")[0]
                    .strip(),
                )
        if isinstance(actions, dict):
            actions = [actions]
        return {
            "type": "action",
            "thought": llm_output.split("⟦status:start:thought⟧")[-1]
            .split("⟦status:end:thought⟧")[0]
            .strip(),
            "actions": [
                f"{action['name']}({', '.join([f'{k}={v if isinstance(v, int) else repr(v)}' for k, v in action['inputs'].items()])})"
                for action in json.loads(
                    llm_output.split("⟦status:start:action⟧")[-1]
                    .split("⟦status:end:action⟧")[0]
                    .strip(),
                )
            ],
        }
    else:
        print(f"************[llm_output]************\n{llm_output}\n********************************")

    return {"type": "error", "error": f"Could not parse LLM output: {llm_output}"}


def execute_tool(action: str) -> str:
    """Execute a tool with the given input"""
    # print(f"[execute_tool] {action}")
    # Check if action is empty or None
    if not action or not isinstance(action, str):
        logger.error(f"Invalid action: {action}")
        return "Action Execution Error: Invalid action"

    # Check if action contains only allowed function names
    allowed_funcs = tools.keys()
    func_name = action.split("(")[0] if "(" in action else action
    if func_name not in allowed_funcs:
        logger.error(f"Function {func_name} not found in allowed tools")
        return f"Action Execution Error: Function {func_name} not allowed"

    try:
        # Execute action with restricted globals
        allowed_globals = {name: info["func"] for name, info in tools.items()}
        result = eval(action, {"__builtins__": {}}, allowed_globals)
        return str(result)
    # except NameError as e:
    #     logger.error(f"Name error in action {action}: {str(e)}")
    #     return f"Action Execution Error: Invalid function or variable name - {str(e)}"
    # except SyntaxError as e:
    #     logger.error(f"Syntax error in action {action}: {str(e)}")
    #     return f"Action Execution Error: Invalid syntax in action - {str(e)}"
    except Exception as e:
        logger.error(f" >>>> Error executing action {action}: {str(e)}")
        return f"Action Execution Error: {str(e)}"

def format_observation(result_data: str) -> str:
    if isinstance(result_data, list):
        # Handle list of dictionaries
        if result_data:  # Check if list is not empty
            result_md = (
                "| " + " | ".join(result_data[0].keys()) + " |\n"
            )
            result_md += (
                "| "
                + " | ".join(["---"] * len(result_data[0].keys()))
                + " |\n"
            )
            for row in result_data:
                result_md += (
                    "| "
                    + " | ".join(str(v) for v in row.values())
                    + " |\n"
                )
            result_md = result_md.rstrip()  # Remove trailing newline
        else:
            result_md = "Empty result list"
    elif isinstance(result_data, dict):
        result_md = str(result_data)
        # Handle single dictionary
        result_md = "| " + " | ".join(result_data.keys()) + " |\n"
        result_md += (
            "| "
            + " | ".join(["---"] * len(result_data.keys()))
            + " |\n"
        )
        result_md += (
            "| "
            + " | ".join(str(v) for v in result_data.values())
            + " |"
        )
    else:
        result_md = str(result_data)
    return result_md

def run_react_agent(params: dict) -> str:
    """
    Run the ReAct agent with the given query

    Args:
        query (str): The question to ask the agent
        max_iterations (int): Maximum number of reasoning iterations

    Returns:
        str: The agent's response
    """
    try:
        
        while params["max_iterations"] > params["iters"]:
            params["iters"] += 1
            # Create the prompt for this iteration
            prompt_template = load_prompt_template()
            # print(f"************[prompt_template]************\n{prompt_template}\n********************************")
            prompt = PromptTemplate.from_template(
                template=prompt_template
            )
            full_prompt = prompt.format(**params)

            # print(
            #     f"************[prompt]************\n{full_prompt}\n********************************"
            # )

            # Get LLM response
            llm_response = llm.invoke(full_prompt)

            # ChatOpenAI는 AIMessage 객체를 반환하므로 content를 추출
            llm_response_text = (
                llm_response.content
                if hasattr(llm_response, "content")
                else str(llm_response)
            )
            print(
                f"************[llm_response]************\n{llm_response_text}\n********************************"
            )

            # Parse the response
            parsed = parse_llm_output(llm_response_text)

            if parsed["type"] == "final_answer":
                return parsed["answer"]

            elif parsed["type"] == "action":
                # Execute the tool
                observation = ""
                actions_history = []
                for action in parsed["actions"]:
                    actions_history.append(action)
                    observation += f"## {action}\n" + format_observation(execute_tool(action)) + "\n\n"

                # Add to scratchpad
                params["agent_scratchpad"] += (
                    f"\nThought: {parsed['thought']}\n\nAction: {' && '.join(actions_history)}\n\nObservation: \n{observation}"
                )
                print(f"### params['agent_scratchpad']: {params['agent_scratchpad']}")

            else:
                return f"Error: {parsed['error']}"

        return f"Error: Maximum iterations ({params['max_iterations']}) reached without finding a final answer."

    except Exception as e:
        logger.error(f"Error running ReAct agent: {str(e)}")
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Test with different types of queries
    test_queries = [
        # "What is 15 * 23?",
        # "Calculate the square root of 144",
        # "What is the capital of France?",
        # "Tell me about Samsung Electronics stock code",
        # "삼성전자 종목 코드 알려줘.",
        # "compare the bigger: 15 * 23 and the square root of 144",
        # "삼성전자 회사 정보 알려줘.",
        # "삼성전자 거래 정보 요약해줘.",
        # "삼성전자 외국인 거래량 알려줘?",
        # "삼성전자 주가는 얼마인가요?"
        # "삼성전자 주가랑 외국인 거래량 알려줘",
        # "2 * 15 * 300 은 삼성전자 외국인 매수량보다 많아?"
        # "삼성전자 거래량 정보 알려줘.",
        # "오늘 삼성전자 주가를 알려줘",
        # "삼성전자 회사 정보랑 외국인 거래량 알려줘"
        # "2 * 15 랑 15 * 2 의 차이는 얼마야?",
        # "2 * 15 * 30 은 삼성전자 설립 년도보다 커?",
        # "오늘 점심 메뉴 뭐였어?",
        # "주식 거래 가이드 알려줘"
        "PER이 뭐야?"
    ]

    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        result = run_react_agent(
            {
                "query": query,
                "assistant_role": "당신은 function을 사용해 정확한 정보로 신뢰할 수 있는 답변을 제공합니다.",
                "user_role": "사용자는 정확한 정보를 얻기 위해 당신에게 질문합니다.",
                "today_date": datetime.now().strftime("%Y-%m-%d"),
                "current_year": str(datetime.now().year),
                "next_year": str(datetime.now().year + 1),
                # "tools": tools,
                "tools_description": "\n".join(
                    [f"{info['description']}\n\n" for name, info in tools.items()]
                ),
                "agent_scratchpad": "",
                "iters": 0,
                "max_iterations": int(os.getenv("MAX_ITERATIONS", 10)),
            }
        )
        print(f"\n{'='*50}")
        print(f"Final Answer:\n{result}")
        print(f"{'='*50}")
