import logging
from math import sqrt, exp, log, sin, cos, tan, pi, e
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# def calculate(expression: str, numbers: list[int]) -> str:
#     """수학 표현식 계산 (예: 'sqrt(16)')"""
#     try:
#         result = eval(expression, {"__builtins__": {}}, allowed_names)
#         return str(result)
#     except Exception as e:
#         logger.error(f"Calculation error: {str(e)}")
#         return f"Error: Calculation failed - {str(e)}"

def news_analyze(jongCode: str) -> dict:
    """
    뉴스를 분석합니다.
    """
    return {
        "code": 200,
        "result": None
    }

def stock_list(
    jongName: str,
    top_k: int = 5,
) -> dict:
    """
    주식 종목 정보를 조회합니다.
    
    Parameters:
        - top_k: 반환할 상위 결과의 개수
        - jongName: 종목명, score: float (유사도 점수)
    """
    return [
        {
            "jongName": "삼성전자",
            "jongCode": "0000000590"
        },
        {
            "jongName": "현대자동차",
            "jongCode": "0000001928"
        },
        {
            "jongName": "SK하이닉스",
            "jongCode": "0000000182"
        },
        
    ]

def calculate(expression: str) -> str:
    """수학 표현식 계산 (예: 'sqrt(16)')"""
    # 보안을 위해 허용된 함수만 사용
    allowed_names = {
        "sqrt": sqrt,
        "exp": exp,
        "log": log,
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "pi": pi,
        "e": e,
    }

    try:
        # 위험한 함수나 변수명 차단
        if any(
            dangerous in expression.lower()
            for dangerous in ["import", "eval", "exec", "__", "open", "file"]
        ):
            return "Error: Potentially dangerous expression detected"

        # 안전한 계산 실행
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError as err:
        return f"Error: Invalid mathematical expression - {str(err)}"
    except Exception as err:
        logger.error(f"Calculation error: {str(err)}")
        return f"Error: Calculation failed - {str(err)}"

def search_wikipedia(query: str) -> str:
    """위키백과 검색 결과 요약"""
    try:
        if not query or not query.strip():
            return "Error: Empty search query"

        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
            },
            timeout=10,  # 타임아웃 설정
        )
        response.raise_for_status()  # HTTP 오류 체크

        data = response.json()

        if "query" not in data or "search" not in data["query"]:
            return "Error: No search results found"

        search_results = data["query"]["search"]
        if not search_results:
            return f"Error: No Wikipedia articles found for '{query}'"

        return search_results[0]["snippet"]

    except requests.exceptions.Timeout:
        return "Error: Wikipedia API request timed out"
    except requests.exceptions.RequestException as e:
        logger.error(f"Wikipedia API request failed: {str(e)}")
        return f"Error: Failed to fetch Wikipedia data - {str(e)}"
    except (KeyError, IndexError) as e:
        logger.error(f"Wikipedia API response parsing error: {str(e)}")
        return "Error: Invalid response format from Wikipedia API"
    except Exception as e:
        logger.error(f"Unexpected error in Wikipedia search: {str(e)}")
        return f"Error: Unexpected error occurred - {str(e)}"

def company_basic_information(jongCode: str) -> dict:
    """
    회사명, 회사 정보, 웹사이트, CEO, 기업 정보 요약, 액면가, 결산월, 발행주식수, 상장일, 업종

    Parameters:
        - jongCode: 종목 코드
    """
    if jongCode == "0000000590":
        return {
            "isuNm": "삼성전자",
            "isuEngNm": "Samsung Electronics",
            "foundDd": "1975/6/11",
            "ceo": "전영현",
            "addr": "경기 수원시 영통구 삼성로 129 (매탄동, 삼성전자)",
            "corpTelNo": "02-2255-0114",
            "hpage": "www.samsung.com",
        }
    else:
        return {
            "isuNm": "크라우드웍스",
            "isuEngNm": "Crowdworks Inc.",
            "foundDd": "2017/04/25",
            "ceo": "김우승",
            "addr": "서울특별시 강남구 테헤란로 309 삼성제일빌딩, 5층",
            "corpTelNo": "02-6954-2960",
            "hpage": "www.crowdworks.kr",
            "parval": 0,
            "acntclsMm": 12,
            "listShrs": 0,
            "sectNm": "기술성장기업부",
            "listDd": "2023/08/31",
            "indNm": "소프트웨어 개발 및 공급",
            "summary": "주요 사업으로는 인공지능 데이터 구축 서비스 ...",
        }


def stock_trade_information(jongCode: str, fromDate: str, toDate: str) -> dict:
    """
    특정 종목의 종목의 매수자, 매수량, 매도량, 순매수량

    Parameters:
        - jongCode: 종목 코드
        - fromDate: 검색 시작일 ('YYYYMMDD')
        - toDate: 검색 종료일 ('YYYYMMDD')
    """
    print(
        f"stock_trade_information: jongCode={jongCode}, fromDate={fromDate}, toDate={toDate}"
    )
    return {
        "기준일": "20250625",
        "외국인매수수량": 4682213,
        "외국인매도수량": 6662972,
        "외국인순매수수량": -1980759,
        "외국인매수금액(원)": 262127600000,
        "외국인매도금액(원)": 372854000000,
        "외국인순매수금액(원)": -110726400000,
        "기관매수수량": 3682869,
        "기관매도수량": 3887369,
        "기관순매수수량": -204500,
        "기관매수금액(원)": 206143010000,
        "기관매수금액(원)": 217683660000,
        "기관순매수금액(원)": -11540650000,
        "개인매수수량": 5879826,
        "개인매도수량": 5208568,
        "개인순매수수량": 671258,
        "개인매수금액(원)": 329206780000,
        "개인매도금액(원)": 291692130000,
        "개인순매수금액(원)": 37514650000,
    }


def trading_guide(question: str) -> dict:
    """
    주식거래에 있어 도움이 될 부가 정보 검색

    Parameters:
        - question: 검색할 질문
    """
    from config import config
    from openai import OpenAI

    client = OpenAI(api_key=config.openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "주식거래와 투자에 대한 전문가로서 주식거래에 있어 도움이 될 부가 정보를 제공합니다. 답변은 500자 내외로 간단하고 명료하게 작성하세요."},
            {"role": "user", "content": question}
        ]
    )

    answer = response.choices[0].message.content
    return {"answer": answer}


def finance_terms_and_basic_knowledge(question: str = "default") -> dict:
    """
    기본적인 금융(주식) 용어 및 (투자) 이론 및 실정, 투자 방법 검색

    Parameters:
        - question: 검색할 질문
    """
    
    from config import config
    from openai import OpenAI

    client = OpenAI(api_key=config.openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "주식거래와 투자에 대한 전문가로서 기본적인 금융(주식) 용어 및 (투자) 이론 및 실전 정보, 투자 방법을 제공합니다. 답변은 500자 내외로 간단하고 명료하게 작성하세요."},
            {"role": "user", "content": question}
        ]
    )

    answer = response.choices[0].message.content
    return {"answer": answer}


def get_upCode(top_k: int = 5, indexName: str = "default") -> dict:
    """
    indexName (인덱스 명) 으로 upCode (업종 코드) 조회

    Parameters:
        - top_k: 반환할 상위 결과의 개수
        - indexName: 인덱스 명, score: float (유사도 점수)
    """
    return {"upCode": None}


def get_sectorCode(
    top_k: int = 1, sectorName: str = "default", typeCode: Optional[int] = 4
) -> dict:
    """
    섹터 명으로 섹터 코드를 조회

    Parameters:
        - top_k: 반환할 상위 결과의 개수
        - sectorName: 인덱스 명, score: float (유사도 점수)
        - typeCode: 1: KOSPI, 2: KOSDAQ, 4: THEME
    """
    print(
        f"get_sectorCode: top_k={top_k}, sectorName={sectorName}, typeCode={typeCode}"
    )
    return {"sectorCode": "0"}


def get_jongCode(top_k: int = 1, jongName: str = "default") -> dict:
    """
    주식 종목명(회사명)으로 종목 코드 조회

    Parameters:
        - top_k: 반환할 상위 결과의 개수
        - jongName: 종목명(회사명), score: float (유사도 점수)
    """
    if jongName == "삼성전자":
        return {"jongCode": "0000000590"}
    else:
        return {"jongCode": "0000001928"}
