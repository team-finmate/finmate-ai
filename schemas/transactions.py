from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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

# 절약 전략 스키마
class SavingStrategy(BaseModel):
    category: str
    current_amount: int
    target_amount: int
    saving_amount: int
    method: str
    difficulty: str

# 절약 레벨 스키마
class SavingLevel(BaseModel):
    level: str
    description: str
    expected_saving: int
    reduction_rate: str
    strategies: List[SavingStrategy]

# 카테고리 분석 스키마
class CategoryBreakdown(BaseModel):
    amount: int
    ratio: float
    transaction_count: int
    avg_amount: int

# 최고 지출 스키마
class TopExpense(BaseModel):
    merchant: str
    amount: int
    category: str

# 절약 요약 스키마
class SavingSummary(BaseModel):
    total_saving: int
    category_count: int
    avg_difficulty: str
    top_category: Optional[str]

# 전체 분석 결과 응답 스키마
class AnalysisResponse(BaseModel):
    total_spent: int
    category_breakdown: Dict[str, CategoryBreakdown]
    spending_trend: str
    avg_transaction: int
    top_expenses: List[TopExpense]
    spending_type: str
    risk_patterns: List[str]
    overspending_categories: List[str]
    saving_suggestions: Dict[str, SavingLevel]
    saving_summary: Optional[Dict[str, SavingSummary]] = None