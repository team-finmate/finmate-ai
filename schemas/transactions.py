from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date
from decimal import Decimal

# 거래 내역 요청 스키마
class TransactionAnalysisRequest(BaseModel):
    transactions: List[Dict[str, Any]]

# 목표 관련 스키마
class Goal(BaseModel):
    id: Optional[str] = None
    user_id: str
    type: str  # TRAVEL, HOUSE, MARRIAGE, CAR, EMERGENCY, EDUCATION, CUSTOM
    name: str  # 자동생성 이름
    custom_name: Optional[str] = None  # CUSTOM일 때만 사용
    target_amount: float
    current_amount: float = 0
    target_date: date
    status: str = "ACTIVE"  # ACTIVE, COMPLETED, PAUSED, CANCELLED

class GoalAchievementAnalysis(BaseModel):
    goal_id: str
    goal_name: str
    goal_type: str
    target_amount: float
    current_amount: float
    target_date: date
    required_monthly_saving: float
    is_achievable: bool
    achievement_probability: float  # 0-100% 확률
    recommended_saving_level: str  # 강한절약, 보통절약, 약한절약
    months_remaining: int
    shortfall_amount: float  # 부족 금액 (음수면 여유 금액)
    analysis_message: str

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
    avg_amount: float  # 평균이므로 float로 변경

# 최고 지출 스키마
class TopExpense(BaseModel):
    merchant: str
    amount: int
    category: str

# 소비습관 피드백 스키마
class SpendingFeedback(BaseModel):
    spending_tips: List[str]
    goal_progress: str
    positive_changes: List[str]
    improvement_guide: List[str]

# 월간 비교 카테고리 스키마
class MonthlyComparisonCategory(BaseModel):
    category: str
    current_amount: int
    previous_amount: int
    change_amount: int
    change_rate: float

# 월간 비교 스키마
class MonthlyComparison(BaseModel):
    all_categories: List[MonthlyComparisonCategory]  # 전체 카테고리, change_rate 오름차순 정렬

# 절약 요약 스키마
class SavingSummary(BaseModel):
    total_saving: int
    category_count: int
    avg_difficulty: str
    top_category: Optional[str]

# 기본 분석 응답 스키마
class BasicAnalysisResponse(BaseModel):
    total_spent: int
    category_breakdown: Dict[str, CategoryBreakdown]
    spending_trend: str
    avg_transaction: float  # 평균이므로 float로 변경
    top_expenses: List[TopExpense]
    spending_type: str
    risk_patterns: List[str]
    overspending_categories: List[str]

# 월간 비교 분석 응답 스키마
class MonthlyComparisonResponse(BaseModel):
    monthly_comparison: MonthlyComparison

# 절약 제안 응답 스키마 (목표 분석 포함)
class SavingSuggestionsResponse(BaseModel):
    saving_suggestions: Dict[str, SavingLevel]
    saving_summary: Optional[Dict[str, SavingSummary]] = None
    goal_achievement_analysis: Optional[List[GoalAchievementAnalysis]] = None

# 소비습관 피드백 응답 스키마
class SpendingFeedbackResponse(BaseModel):
    spending_feedback: SpendingFeedback

# 전체 분석 결과 응답 스키마 (기존 유지 - 레거시 지원)
class AnalysisResponse(BaseModel):
    total_spent: int
    category_breakdown: Dict[str, CategoryBreakdown]
    spending_trend: str
    avg_transaction: float  # 평균이므로 float로 변경
    top_expenses: List[TopExpense]
    spending_type: str
    risk_patterns: List[str]
    overspending_categories: List[str]
    spending_feedback: SpendingFeedback
    monthly_comparison: MonthlyComparison
    saving_suggestions: Dict[str, SavingLevel]
    saving_summary: Optional[Dict[str, SavingSummary]] = None