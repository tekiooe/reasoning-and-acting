import os
from typing import Dict, List
from pathlib import Path


def load_prompt_template(template_name: str) -> str:
    """
    프롬프트 템플릿 파일을 로드합니다.
    
    Args:
        template_name (str): 템플릿 파일명 (예: 'react_prompt_template.txt')
        
    Returns:
        str: 로드된 프롬프트 템플릿
    """
    # 현재 파일의 디렉토리를 기준으로 prompts 디렉토리 경로 설정
    current_dir = Path(__file__).parent
    prompt_file_path = current_dir / "prompts" / template_name
    
    if not prompt_file_path.exists():
        raise FileNotFoundError(f"프롬프트 템플릿 파일을 찾을 수 없습니다: {prompt_file_path}")
    
    with open(prompt_file_path, 'r', encoding='utf-8') as f:
        return f.read()


def create_react_prompt(tools_dict: Dict, conversation_history: List[str]) -> str:
    """
    ReAct 프롬프트를 생성합니다.
    
    Args:
        tools_dict (Dict): 사용 가능한 도구들의 딕셔너리
        conversation_history (List[str]): 대화 히스토리
        
    Returns:
        str: 완성된 ReAct 프롬프트
    """
    # 프롬프트 템플릿 로드
    template = load_prompt_template("react_prompt_template.txt")
    
    # 도구 설명 생성
    tools_description = "\n".join([
        f"{info['description']}\n\n"
        for name, info in tools_dict.items()
    ])
    
    # 히스토리 텍스트 생성
    history_text = "\n".join(conversation_history) if conversation_history else ""
    
    # 템플릿 변수 치환
    prompt = template.format(
        tools_description=tools_description,
        history_text=history_text,
        input="{input}",
        agent_scratchpad="{agent_scratchpad}"
    )
    
    return prompt


def get_prompt_version() -> str:
    """
    현재 프롬프트 버전을 반환합니다.
    
    Returns:
        str: 프롬프트 버전 정보
    """
    # 프롬프트 파일의 수정 시간을 기반으로 버전 정보 생성
    current_dir = Path(__file__).parent
    prompt_file_path = current_dir / "prompts" / "react_prompt_template.txt"
    
    if prompt_file_path.exists():
        mtime = prompt_file_path.stat().st_mtime
        return f"v1.0.{int(mtime)}"
    else:
        return "unknown"


def list_available_prompts() -> List[str]:
    """
    사용 가능한 프롬프트 템플릿 목록을 반환합니다.
    
    Returns:
        List[str]: 프롬프트 템플릿 파일명 목록
    """
    current_dir = Path(__file__).parent
    prompts_dir = current_dir / "prompts"
    
    if not prompts_dir.exists():
        return []
    
    return [f.name for f in prompts_dir.glob("*.txt")]


if __name__ == "__main__":
    # 테스트
    print("사용 가능한 프롬프트:", list_available_prompts())
    print("현재 프롬프트 버전:", get_prompt_version()) 