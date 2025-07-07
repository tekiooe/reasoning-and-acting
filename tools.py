from actions import (
    calculate, search_wikipedia, company_basic_information, 
    stock_trade_information, trading_guide, finance_terms_and_basic_knowledge,
    get_upCode, get_sectorCode, get_jongCode
)

tools = {
    "calculate": {
        "func": calculate,
        "description": """
def calculate(expression: str) -> str:
    \"\"\"
    expression을 계산하여 결과를 반환
    \"\"\"
    return str(result)
"""
    },
    "company_basic_information": {
        "func": company_basic_information,
        "description": """
def company_basic_information(jongCode: str) -> dict:
    \"\"\"
    회사명, 회사 정보, 웹사이트, CEO, 기업 정보 요약, 액면가, 결산월, 발행주식수, 상장일, 업종
    \"\"\"
    return {{
    \"isuNm\": \"삼성전자\",
    \"isuEngNm\": \"CrowdWorks, inc.\",
    \"foundDd\": \"2017/04/25\",
    \"ceo\": \"김우승\",
    \"addr\": \"서울특별시 강남구 테헤란로 309 삼성제일빌딩, 5층\",
    \"summary\": \"주요 사업으로는 인공지능 데이터 구축 서비스 ...\"
    }}
"""
    },
    "stock_trade_information": {
        "func": stock_trade_information,
        "description": """
def stock_trade_information(jongCode: str, fromDate: str, toDate: str) -> dict:
    \"\"\"
    특정 종목의 종목의 매수자, 매수량, 매도량, 순매수량
    \"\"\"
    return {{
    \"기준일\": \"20241213\",
    \"외국인매수수량\": 4682213,
    \"외국인매도수량\": 6662972,
    \"외국인순매수수량\": -1980759,
    \"외국인매수금액(원)\": 262127600000,
    \"외국인매도금액(원)\": 372854000000,
    \"외국인순매수금액(원)\": -110726400000,
    \"기관매수수량\": 3682869,
    \"기관매도수량\": 3887369,
    \"기관순매수수량\": -204500,
    \"기관매수금액(원)\": 206143010000,
    \"기관매수금액(원)\": 217683660000,
    \"기관순매수금액(원)\": -11540650000,
    \"개인매수수량\": 5879826,
    \"개인매도수량\": 5208568,
    \"개인순매수수량\": 671258,
    \"개인매수금액(원)\": 329206780000,
    \"개인매도금액(원)\": 291692130000,
    \"개인순매수금액(원)\": 37514650000
    }}
"""
    },
    "trading_guide": {
        "func": trading_guide,
        "description": """def trading_guide(question: str) -> dict:
    \"\"\"
    주식거래에 있어 도움이 될 부가 정보 검색

    Parameters:
        - question: 검색할 질문
    \"\"\"
    return {{
    \"answer\": \"응답\"
    }}
"""
    },
    "finance_terms_and_basic_knowledge": {
        "func": finance_terms_and_basic_knowledge,
        "description": """def finance_terms_and_basic_knowledge(question: str) -> dict:
    \"\"\"
    기본적인 금융(주식) 용어 및 (투자) 이론 및 실정, 투자 방법 검색

    Parameters:
        - question: 검색할 질문
    \"\"\"
    return {{
    \"answer\": \"응답\"
    }}
"""
    },
    "get_upCode": {
        "func": get_upCode,
        "description": """def get_upCode(top_k: int = 5, indexName: str) -> dict:
    \"\"\"
    indexName (인덱스 명) 으로 upCode (업종 코드) 조회

    Parameters:
        - top_k: 반환할 상위 결과의 개수
        - indexName: 인덱스 명, score: float (유사도 점수)
    \"\"\"
    return {{
    \"upCode\": None
    }}
"""
    },
    "get_sectorCode": {
        "func": get_sectorCode,
        "description": """def get_sectorCode(top_k: int = 1, sectorName: str, typeCode: Optional[int] = 4) -> dict:
    \"\"\"
    섹터 명으로 섹터 코드를 조회

    Parameters:
        - top_k: 반환할 상위 결과의 개수
        - sectorName: 인덱스 명, score: float (유사도 점수)
        - typeCode: 1: KOSPI, 2: KOSDAQ, 4: THEME
    \"\"\"
    return {{
    \"sectorCode\": \"0\"
    }}
"""
    },
    "get_jongCode": {
        "func": get_jongCode,
        "description": """def get_jongCode(top_k: int = 1, jongName: str) -> dict:
    \"\"\"
    주식 종목명(회사명)으로 종목 코드 조회

    Parameters:
        - top_k: 반환할 상위 결과의 개수
        - jongName: 종목명(회사명), score: float (유사도 점수)
    \"\"\"
    return {{
    \"jongCode\": None
    }}
"""
    }
}