import os
from typing import Dict, List
from pathlib import Path


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
    current_dir = Path(__file__).resolve()
    prompts_dir = current_dir.parent.parent / "prompts"

    if not prompts_dir.exists():
        return []

    return [f.name for f in prompts_dir.glob("*.txt")]


def get_prompt_template_name() -> str:
    """
    환경변수로 지정한 버전의 프롬프트 템플릿 이름을 반환합니다.
    또는 .env 파일에 지정된 버전의 프롬프트 템플릿 이름을 반환합니다.

    Returns:
        str: 프롬프트 템플릿 이름
    """
    from config import get_prompt_template_name as PROMPT_TEMPLATE_NAME

    return PROMPT_TEMPLATE_NAME()


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
        raise FileNotFoundError(
            f"프롬프트 템플릿 파일을 찾을 수 없습니다: {prompt_file_path}"
        )

    with open(prompt_file_path, "r", encoding="utf-8") as f:
        return f.read()


def format_prompt_params(*params) -> str:
    """
    프롬프트 파라미터를 포맷팅합니다.
    """
    params.query = params.query
    params.agent_scratchpad = params.agent_scratchpad
    params.tools_dict = "\n".join(
        [f"{info['description']}\n\n" for name, info in params.tools_dict.items()]
    )
    params.conversation_history = (
        "\n".join(params.conversation_history) if params.conversation_history else ""
    )
    return params


def create_react_prompt(*params) -> str:
    """
    ReAct 프롬프트를 생성합니다.

    Returns:
        str: 완성된 ReAct 프롬프트
    """
    # 프롬프트 템플릿 로드
    template = load_prompt_template("react_prompt_template.txt")

    # 템플릿 변수 치환
    prompt = template.format(**format_prompt_params(*params))

    return prompt


if __name__ == "__main__":
    # 테스트
    print("사용 가능한 프롬프트:", list_available_prompts())
    print("사용할 프롬프트 파일:", get_prompt_template_name())
