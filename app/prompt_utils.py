import os
from typing import Dict, List
from pathlib import Path
from functools import reduce
from datetime import datetime

reserved_keywords = {
    "{{param::assistant_role::textarea}}": "{assistant_role}",
    "{{param::user_role::textarea}}": "{user_role}",
    "{{resv::TODAY_DATE}}": "{today_date}",
    "{{resv::CURRENT_YEAR}}": "{current_year}",
    "{{resv::NEXT_YEAR}}": "{next_year}",
    "{{choices::functions::inferenceUnit::multi}}": "{tools_description}",
    # "{{param::observations::textarea}}": "{history_text}",
    "{{param::user_query::textfield}}": "{query}",
    "{{param::react_history::textarea}}": "{agent_scratchpad}",
    "{{param::iters}}": "{iters}",
    "{{param::max_iters}}": "{max_iterations}",
}


def get_prompt_version() -> str:
    """
    현재 프롬프트 버전을 반환합니다.

    Returns:
        str: 프롬프트 버전 정보
    """
    # 프롬프트 파일의 수정 시간을 기반으로 버전 정보 생성
    current_dir = Path(__file__).resolve()
    prompt_file_path = (
        current_dir.parent.parent / "prompts" / get_prompt_template_name()
    )

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


def load_prompt_template(template_name: str = get_prompt_template_name()) -> str:
    """
    프롬프트 템플릿 파일을 로드합니다.

    Args:
        template_name (str): 템플릿 파일명 (예: 'react_prompt_template.txt')

    Returns:
        str: 로드된 프롬프트 템플릿
    """
    # 현재 파일의 디렉토리를 기준으로 prompts 디렉토리 경로 설정
    current_dir = Path(__file__).resolve()
    prompt_file_path = current_dir.parent.parent / "prompts" / template_name

    if not prompt_file_path.exists():
        raise FileNotFoundError(
            f"프롬프트 템플릿 파일을 찾을 수 없습니다: {prompt_file_path}"
        )

    with open(prompt_file_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    # Filter out lines that start and end with /**** ****/: v8부터 Alpy 포맷으로 변경되었음.
    filtered_prompt = "\n".join(
        line
        for line in prompt.splitlines()
        if not (line.startswith("/****") and line.endswith("****/"))
    )

    # Replace reserved keywords: v8부터 Alpy 포맷으로 변경되었음.
    for key, value in reserved_keywords.items():
        filtered_prompt = filtered_prompt.replace(key, value)

    return filtered_prompt


def create_react_prompt(params: dict) -> str:
    """
    ReAct 프롬프트를 생성합니다.

    Returns:
        str: 완성된 ReAct 프롬프트
    """
    # 프롬프트 템플릿 로드
    template = load_prompt_template(get_prompt_template_name())

    # 템플릿 변수 치환
    prompt = template.format(**params)

    return prompt


def print_prompt_in_alpy_format() -> str:
    """
    ReAct 프롬프트를 예약어와 블록 구분자를 포함한 alpy 포맷으로 출력합니다.
    """
    return


if __name__ == "__main__":
    # 테스트
    print("사용 가능한 프롬프트:", list_available_prompts())
    print("사용할 프롬프트 파일:", get_prompt_template_name())
