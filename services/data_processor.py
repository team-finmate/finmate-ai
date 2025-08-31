# services/data_processor.py
import datetime as dt
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from core.config import (
    WEEKEND_DAYS, WEEKDAY_BUCKETS, WEEKEND_BUCKETS, 
    AMOUNT_HINTS, KEYWORD_HINTS, RISK_PATTERNS
)


def in_range(t_str: str, start: str, end: str) -> bool:
    """시간이 주어진 범위 안에 있는지 확인"""
    def to_time(s: str) -> dt.time:
        if s == "24:00": 
            return dt.time(23, 59, 59)
        h, m = map(int, s.split(":"))
        return dt.time(h, m, 0)
    
    t = dt.time(*map(int, t_str.split(":")))
    return to_time(start) <= t <= to_time(end)


def assign_time_bucket(date_str: str, time_str: str) -> Dict[str, str]:
    """날짜와 시간을 기반으로 시간대 버킷 할당"""
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
    """금액을 기반으로 카테고리 힌트 제공"""
    hints = []
    for label, lo, hi in AMOUNT_HINTS:
        if lo <= amount <= hi:
            hints.append(label)
    return hints


def keyword_hint(merchant: str, category: str) -> List[str]:
    """상점명과 카테고리를 기반으로 키워드 힌트 제공"""
    merged = f"{merchant} {category}"
    hits = set()
    
    for k, v in KEYWORD_HINTS.items():
        if k in merged:
            hits.add(v)
    
    return list(hits)


def separate_transactions_by_month(txns: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    거래 내역을 월별로 분리하여 현재 달과 이전 달로 구분
    
    Args:
        txns: 전체 거래 내역 리스트
        
    Returns:
        tuple: (현재 달 거래, 이전 달 거래)
    """
    # 월별로 거래 그룹화
    monthly_groups = defaultdict(list)
    
    for txn in txns:
        # date에서 년-월 추출
        date_str = txn.get("date", "")
        if date_str:
            try:
                # "YYYY-MM-DD" 형식에서 "YYYY-MM" 추출
                year_month = "-".join(date_str.split("-")[:2])
                monthly_groups[year_month].append(txn)
            except (ValueError, IndexError):
                # 날짜 형식이 잘못된 경우 현재 달로 분류
                current_month = dt.date.today().strftime("%Y-%m")
                monthly_groups[current_month].append(txn)
    
    # 월별 정렬 (최신 순)
    sorted_months = sorted(monthly_groups.keys(), reverse=True)
    
    if len(sorted_months) == 0:
        return [], []
    elif len(sorted_months) == 1:
        # 한 달 데이터만 있는 경우
        return monthly_groups[sorted_months[0]], []
    else:
        # 두 달 이상 데이터가 있는 경우
        current_month = sorted_months[0]
        previous_month = sorted_months[1]
        return monthly_groups[current_month], monthly_groups[previous_month]


def normalize_category(category: str) -> str:
    """카테고리를 16개 표준 카테고리로 정규화"""
    category_mapping = {
        # 기존 카테고리를 표준 카테고리로 매핑
        "배달음식": "식비",
        "문화/여가": "취미/여가",
        "카페": "카페/간식",
        "대중교통": "교통/자동차",
        "쇼핑몰": "쇼핑",
        "편의점": "편의점/마트/잡화",
        "마트": "편의점/마트/잡화",
        "병원": "의료/건강/피트니스",
        "약국": "의료/건강/피트니스",
        "주유소": "교통/자동차",
        "통신비": "주거/통신",
        "구독서비스": "주거/통신",
        "헬스장": "의료/건강/피트니스",
        "피트니스": "의료/건강/피트니스",
        "미용실": "미용",
        "네일샵": "미용",
        "학원": "교육",
        "온라인강의": "교육",
        "항공료": "여행/숙박",
        "호텔": "여행/숙박",
        "펜션": "여행/숙박",
        "보험료": "보험/세금/기타금융",
        "세금": "보험/세금/기타금융",
        "계좌이체": "이체",
        "송금": "이체",
        "ATM": "이체",
        "세탁소": "생활",
        "택배": "생활",
        "우체국": "생활"
    }
    
    # 매핑된 카테고리가 있으면 반환, 없으면 원본 반환
    return category_mapping.get(category, category)


def enrich_transactions(txns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """거래 내역을 보강하여 시간대 버킷, 금액 힌트, 키워드 힌트 추가"""
    enriched = []
    
    for t in txns:
        # 카테고리 정규화
        normalized_category = normalize_category(t.get("category", "카테고리 없음"))
        
        # 시간대 버킷 할당
        tb = assign_time_bucket(t["date"], t["time"])
        
        # 금액 힌트 생성
        a_hints = amount_hint(t["amount"])
        
        # 키워드 힌트 생성 (정규화된 카테고리 사용)
        k_hints = keyword_hint(t.get("merchant", ""), normalized_category)
        
        # 원본 데이터에 보강 데이터 추가
        enriched.append({
            **t,
            "category": normalized_category,  # 정규화된 카테고리로 교체
            **tb,
            "amount_hints": a_hints,
            "keyword_hints": k_hints
        })
    
    return enriched


def detect_risk_patterns(enriched_data: List[Dict[str, Any]]) -> List[str]:
    """위험 패턴 감지"""
    risk_patterns = []
    
    # 새벽 시간대 소비 패턴 감지
    dawn_transactions = [t for t in enriched_data 
                        if t.get("time_bucket") in RISK_PATTERNS["새벽_소비"]]
    if len(dawn_transactions) >= 3:
        total_dawn_amount = sum(t["amount"] for t in dawn_transactions)
        risk_patterns.append(f"새벽 시간대 {len(dawn_transactions)}회 소비 (총 {total_dawn_amount:,}원)")
    
    # 고액 단건 결제 감지
    high_amount_transactions = [t for t in enriched_data 
                               if t["amount"] >= RISK_PATTERNS["고액_단건"]]
    if high_amount_transactions:
        max_amount = max(t["amount"] for t in high_amount_transactions)
        risk_patterns.append(f"고액 단건 결제 {len(high_amount_transactions)}건 (최대 {max_amount:,}원)")
    
    # 반복 배달 주문 감지
    delivery_transactions = [t for t in enriched_data 
                           if "배달음식" in t.get("keyword_hints", [])]
    if len(delivery_transactions) >= RISK_PATTERNS["반복_배달"]["threshold"]:
        avg_delivery = sum(t["amount"] for t in delivery_transactions) // len(delivery_transactions)
        risk_patterns.append(f"배달 주문 {len(delivery_transactions)}회 (평균 {avg_delivery:,}원)")
    
    return risk_patterns


def identify_overspending_categories(enriched_data: List[Dict[str, Any]]) -> List[str]:
    """과소비 카테고리 식별"""
    category_totals = {}
    
    # 카테고리별 총액 계산
    for t in enriched_data:
        for hint in t.get("keyword_hints", []):
            if hint not in category_totals:
                category_totals[hint] = 0
            category_totals[hint] += t["amount"]
    
    # 전체 지출 대비 높은 비율의 카테고리 식별
    total_spent = sum(category_totals.values())
    overspending = []
    
    for category, amount in category_totals.items():
        ratio = (amount / total_spent) * 100 if total_spent > 0 else 0
        if ratio > 25:  # 전체 지출의 25% 이상
            overspending.append(category)
    
    return overspending


def generate_saving_suggestions(enriched_data: List[Dict[str, Any]]) -> List[str]:
    """절약 제안 생성"""
    suggestions = []
    
    # 배달음식 관련 제안
    delivery_transactions = [t for t in enriched_data 
                           if "배달음식" in t.get("keyword_hints", [])]
    if len(delivery_transactions) >= 2:
        avg_delivery = sum(t["amount"] for t in delivery_transactions) // len(delivery_transactions)
        monthly_saving = avg_delivery * 2  # 월 2회 줄인다고 가정
        suggestions.append(f"월 2회 배달 주문 줄이면 {monthly_saving:,}원 절약")
    
    # 카페 관련 제안
    cafe_transactions = [t for t in enriched_data 
                        if "카페/간식" in t.get("keyword_hints", [])]
    if len(cafe_transactions) >= 5:
        avg_cafe = sum(t["amount"] for t in cafe_transactions) // len(cafe_transactions)
        monthly_saving = avg_cafe * 10  # 월 10회 줄인다고 가정
        suggestions.append(f"월 10회 카페 이용 줄이면 {monthly_saving:,}원 절약")
    
    # 구독서비스 관련 제안
    subscription_transactions = [t for t in enriched_data 
                               if "구독서비스" in t.get("keyword_hints", [])]
    if len(subscription_transactions) >= 3:
        total_subscription = sum(t["amount"] for t in subscription_transactions)
        suggestions.append(f"불필요한 구독 서비스 정리로 월 {total_subscription//2:,}원 절약 가능")
    
    return suggestions
