
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os, json, datetime as dt
from typing import List, Dict, Any

# 환경 변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# Pydantic 모델 정의
# API 요청 본문의 JSON 데이터 구조를 정의합니다.
class Transaction(BaseModel):
    transaction_id: str
    date: str
    time: str
    merchant: str
    category: str
    amount: int
    payment_method: str
    balance: int

# 1) 규칙 정의 -----------------------------------------------------------------
WEEKEND_DAYS = {5, 6}
WEEKDAY_BUCKETS = [
    ("07:30", "09:00", "아침_커피/편의점"),
    ("12:00", "13:30", "점심_식사"),
    ("18:00", "20:00", "저녁_식사/배달"),
    ("22:00", "24:00", "야식/편의점"),
]
WEEKEND_BUCKETS = [
    ("10:30", "13:00", "늦은_오전_브런치"),
    ("13:00", "18:00", "오후_쇼핑/문화"),
    ("18:00", "24:00", "저녁_외식/술"),
]
AMOUNT_HINTS = [
    ("커피", 4000, 7000),
    ("점심", 8000, 15000),
    ("배달음식", 15000, 25000),
    ("편의점", 3000, 10000),
]
KEYWORD_HINTS = {
    "배달의민족": "배달음식", "요기요": "배달음식", "배민": "배달음식",
    "스타벅스": "커피", "이디야": "커피", "커피": "커피",
    "편의점": "편의점", "CU": "편의점", "GS25": "편의점", "세븐일레븐": "편의점",
    "CGV": "문화/여가", "롯데시네마": "문화/여가", "메가박스": "문화/여가",
}

# 2) 헬퍼 함수 -----------------------------------------------------------------
def in_range(t_str: str, start: str, end: str) -> bool:
    def to_time(s: str) -> dt.time:
        if s == "24:00": return dt.time(23, 59, 59)
        h, m = map(int, s.split(":"))
        return dt.time(h, m, 0)
    t = dt.time(*map(int, t_str.split(":")))
    return to_time(start) <= t <= to_time(end)

def assign_time_bucket(date_str: str, time_str: str) -> Dict[str, str]:
    y, m, d = map(int, date_str.split("-"))
    weekday = dt.date(y, m, d).weekday()
    weekend = weekday in WEEKEND_DAYS
    t_hm = time_str[:5]
    buckets = WEEKEND_BUCKETS if weekend else WEEKDAY_BUCKETS
    for start, end, label in buckets:
        if in_range(t_hm, start, end):
            return {"weekday_type": "주말" if weekend else "평일", "time_bucket": label}
    return {"weekday_type": "주말" if weekend else "평일", "time_bucket": "기타"}

def amount_hint(amount: int) -> List[str]:
    hints = []
    for label, lo, hi in AMOUNT_HINTS:
        if lo <= amount <= hi: hints.append(label)
    return hints

def keyword_hint(merchant: str, category: str) -> List[str]:
    merged = f"{merchant} {category}"
    hits = set()
    for k, v in KEYWORD_HINTS.items():
        if k in merged: hits.add(v)
    return list(hits)

def enrich_transactions(txns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    enriched = []
    for t in txns:
        tb = assign_time_bucket(t["date"], t["time"])
        a_hints = amount_hint(t["amount"])
        k_hints = keyword_hint(t.get("merchant", ""), t.get("category", ""))
        enriched.append({**t, **tb, "amount_hints": a_hints, "keyword_hints": k_hints})
    return enriched

# --- 3) 모델 시스템 지시문 ------------------------------------------------------
instructions = """
너는 결제내역(이미 버킷팅 및 힌트가 포함됨)을 집계하여 다음 두 출력을 만드는 데이터 분석가다.

[해야 할 일]
1) 시간대별 패턴: 같은 'weekday_type'와 'time_bucket' 안에서, 무엇을 주로 소비했는지(커피/편의점/점심/배달음식/문화/쇼핑/야식/술 등)를 간단 요약.
   - 근거는 'keyword_hints', 'amount_hints', 원본 category/merchant를 종합.
   - 항목별로 대표 예시 merchant 1~2개와 평균금액(정수 원)을 포함.
2) 금액 패턴: 라벨(커피/점심/배달음식/편의점 등)별로 관측된 금액 범위(min~max)와 평균금액을 산출.

[출력 형식(JSON만)]
{
  "시간대별_패턴": [
    {
      "구분": "평일|주말",
      "시간대": "라벨",
      "주요_소비": ["커피", "편의점", ...],
      "대표_가맹점": ["상호1", "상호2"],
      "평균금액": 0
    }
  ],
  "금액_패턴": [
    {
      "라벨": "커피|점심|배달음식|편의점|문화/여가|쇼핑|야식|술",
      "관측범위": {"min": 0, "max": 0},
      "평균금액": 0
    }
  ]
}

[주의]
- 반드시 유효한 JSON만 출력.
- 추정이 불확실하면 보수적으로 판단하고, 근거가 부족한 라벨은 제외.
- 원 단위 정수로 반올림.
"""

# 루트 경로 ("/")에 대한 GET 요청 핸들러
@app.get("/")
def read_root():
    return {"Hello": "World"}

# "/items/{item_id}" 경로에 대한 GET 요청 핸들러
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# --- API 엔드포인트 정의 ---
@app.post("/analyze-transactions/")
def analyze_transactions(transactions: List[Transaction]):
    """
    결제 내역 리스트를 입력받아 분석 결과를 반환하는 엔드포인트.
    """
    # 1. Pydantic 모델 리스트를 딕셔너리 리스트로 변환
    transactions_dict = [txn.model_dump() for txn in transactions]
    
    # 2. 거래 내역 보강 (enrich)
    enriched_data = enrich_transactions(transactions_dict)

    # 3. OpenAI API 호출
    # 기존 코드에서 `resp` 변수 할당 부분
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": instructions},
            {
                "role": "user",
                "content": f"다음 결제내역(버킷팅/힌트 포함)을 집계해줘. 반드시 유효한 JSON만 출력:\n{json.dumps(enriched_data, ensure_ascii=False)}"
            }
        ],
        response_format={"type": "json_object"}
    )
    
    # 4. JSON 응답 파싱 및 반환
    # OpenAI 응답은 `resp.choices[0].message.content`에 담겨있습니다.
    # 이를 JSON으로 변환하여 반환
    try:
        result = json.loads(resp.choices[0].message.content)
        return result
    except (json.JSONDecodeError, IndexError) as e:
        return {"error": "Failed to parse API response", "details": str(e)}