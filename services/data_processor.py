# services/data_processor.py
import datetime as dt
from typing import List, Dict, Any
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


def enrich_transactions(txns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """거래 내역을 보강하여 시간대 버킷, 금액 힌트, 키워드 힌트 추가"""
    enriched = []
    
    for t in txns:
        # 시간대 버킷 할당
        tb = assign_time_bucket(t["date"], t["time"])
        
        # 금액 힌트 생성
        a_hints = amount_hint(t["amount"])
        
        # 키워드 힌트 생성
        k_hints = keyword_hint(t.get("merchant", ""), t.get("category", ""))
        
        # 원본 데이터에 보강 데이터 추가
        enriched.append({
            **t,
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
