import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """환경 변수와 설정을 관리하는 클래스"""

    def __init__(self):
        self._load_env_file()

    def _load_env_file(self):
        """프로젝트 루트의 .env 파일을 로드합니다."""
        # 프로젝트 루트 디렉토리 찾기 (app 디렉토리의 상위)
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        env_file = project_root / ".env"

        if env_file.exists():
            load_dotenv(env_file)
        else:
            # .env 파일이 없으면 기본값 사용
            print(f"Warning: .env file not found at {env_file}")

    @property
    def prompt_version(self) -> str:
        """프롬프트 버전을 반환합니다."""
        return os.getenv("PROMPT_VERSION", "default")

    @property
    def prompt_template_name(self) -> str:
        """프롬프트 템플릿 파일명을 반환합니다."""
        version = self.prompt_version
        if version == "default":
            return "react_prompt_template_default.txt"
        else:
            return f"react_prompt_template_{version}.txt"

    @property
    def debug_mode(self) -> bool:
        """디버그 모드 여부를 반환합니다."""
        return os.getenv("DEBUG", "False").lower() == "true"

    @property
    def log_level(self) -> str:
        """로그 레벨을 반환합니다."""
        return os.getenv("LOG_LEVEL", "INFO")

    @property
    def max_tokens(self) -> int:
        """최대 토큰 수를 반환합니다."""
        return int(os.getenv("MAX_TOKENS", "1000"))

    @property
    def temperature(self) -> float:
        """모델의 temperature를 반환합니다."""
        return float(os.getenv("TEMPERATURE", "0"))

    def get(self, key: str, default=None):
        """환경 변수 값을 반환합니다."""
        return os.getenv(key, default)

    def set(self, key: str, value: str):
        """환경 변수를 설정합니다."""
        os.environ[key] = value


# 전역 설정 인스턴스 생성
config = Config()


# 편의 함수들
def get_prompt_version() -> str:
    """프롬프트 버전을 반환하는 편의 함수"""
    return config.prompt_version


def get_prompt_template_name() -> str:
    """프롬프트 템플릿 파일명을 반환하는 편의 함수"""
    return config.prompt_template_name


def is_debug_mode() -> bool:
    """디버그 모드 여부를 반환하는 편의 함수"""
    return config.debug_mode


def get_api_key() -> Optional[str]:
    """API 키를 반환하는 편의 함수"""
    return config.api_key


if __name__ == "__main__":
    # 설정 테스트
    print(f"Prompt Version: {config.prompt_version}")
    print(f"Prompt Template: {config.prompt_template_name}")
    print(f"Debug Mode: {config.debug_mode}")
    print(f"Log Level: {config.log_level}")
    print(f"Model Name: {config.model_name}")
    print(f"Max Tokens: {config.max_tokens}")
    print(f"Temperature: {config.temperature}")
