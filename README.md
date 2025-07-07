# ReAct


## ReAct 패턴

이 프로젝트는 ReAct (Reasoning and Action) 패턴을 구현합니다:

1. Thought: 문제 해결을 위한 단계별 추론
2. Action: 적절한 function 선택 및 실행
3. Observation: Action Retriever
4. Final Answer: 최종 답변

## 지원하는 AI 모델

### GPT 버전 (`run_gpt.py`)
- **모델**: GPT-4.1-nano (기본값) 또는 GPT-4.1-mini
- **API**: OpenAI API
- **환경변수**: `OPENAI_API_KEY` 필요

### Claude 버전 (`run_claude.py`)
- **모델**: Claude-3-5-haiku-20241022 (기본값) 또는 Claude-3-5-sonnet-20241022
- **API**: Anthropic API
- **환경변수**: `ANTHROPIC_API_KEY` 필요

## 설치 및 설정

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정
`.env` 파일을 생성하고 API 키를 설정하세요:

```env
# OpenAI API 키 (GPT 용)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API 키 (Claude 용)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. ReAct Actions 모듈 설정
`actions.py` 파일이 있어야 합니다. 이 파일에는 실제 도구 함수들이 구현되어 있습니다.

## 사용법

### GPT 버전 실행
```bash
python run_gpt.py
```

### Claude 버전 실행
```bash
python run_claude.py
```

### 예시 질문들

1. **1개 Loop 생성**
   - "005930 종목의 회사 정보를 조회해줘"
   - "3 * 300 은 얼마야?"

2. **2개 Loop 생성**
   - "삼성전자의 기본 정보를 알려줘"
   - "삼성전자의 외국인 거래량 알려줘"

3. **복합/병렬 Loop 생성**
   - "삼성전자 회사 정보랑 외국인 거래량 알려줘"
   - "2 * 15 랑 15 * 2 의 차이는 얼마야?"


## 프로젝트 구조

```
ReAct/
├── README.md                 # 프로젝트 설명서
├── requirements.txt          # Python 의존성
├── actions.py         # Action 정의
├── run_gpt.py               # GPT 모델 기반 ReAct 에이전트
├── run_claude.py            # Claude 모델 기반 ReAct 에이전트
├── prompt_utils.py          # 프롬프트 유틸리티 함수
├── prompts/                 # 프롬프트 템플릿 디렉토리
│   └── react_prompt_template.txt  # ReAct 프롬프트 템플릿
└── .env                     # API 키 설정 (사용자 생성 필요)
```
