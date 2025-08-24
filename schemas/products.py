from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# 정기예금 상품 스키마
class TimeDepositProduct(BaseModel):
    금융회사: str
    상품명: str
    기간개월: int
    금리유형: str
    이자지급주기: str
    이자계산방식: str
    세전이자율_num: float
    세후이자율_num: float
    최고우대금리_num: float
    세전우대합계_num: float
    세후우대합계_num: float
    우대금리세부내역: List[str]
    최소가입금액: int
    권장예치금액: int
    예금자보호여부: bool
    보호기관: str
    보호한도: int
    가입채널: List[str]
    가입대상: str
    판매상태: str
    세제혜택: str

# 적금 상품 스키마 (실제 데이터 구조에 맞춤)
class SavingProduct(BaseModel):
    금융회사: str
    상품명: str
    적립방식: str  # "자유적립식", "정액적립식" 등
    세전이자율_num: float
    세후이자율_num: float
    세전우대합계_num: float
    세후우대합계_num: float
    세후이자_예시: Optional[int] = None
    기간개월_기본: int
    기간별이자율: List[Dict[str, Any]]  # 기간별 이자율 정보
    최소월적립액: int
    최대월적립액: int
    최대가입금액: int
    가입채널: List[str]
    가입대상: str
    우대금리세부내역: List[str]
    이자계산방식: str  # "단리", "복리"
    이자지급주기: str  # "만기지급", "월지급" 등
    중도해지이율_num: float
    자동재예치: bool
    판매상태: str
    예상세후이자_기본: Optional[int] = None
    예상세후이자_우대만족: Optional[int] = None

# 상품 추천 이유 스키마
class ProductRecommendationReason(BaseModel):
    reason_title: str
    reason_detail: str
    benefit_amount: Optional[int] = None
    benefit_description: str

# 추천 정기예금 상품 스키마
class RecommendedTimeDeposit(BaseModel):
    product: TimeDepositProduct
    recommendation_score: float
    recommended_amount: int
    expected_interest: int
    reasons: List[ProductRecommendationReason]
    fit_analysis: str

# 추천 적금 상품 스키마
class RecommendedSaving(BaseModel):
    product: SavingProduct
    recommendation_score: float
    recommended_monthly_amount: int
    expected_total_amount: int
    expected_interest: int
    reasons: List[ProductRecommendationReason]
    fit_analysis: str

# 금융상품 추천 요청 스키마
class ProductRecommendationRequest(BaseModel):
    # 사용자 재정 분석 데이터 (기존 AnalysisResponse와 동일한 구조)
    total_spent: int
    category_breakdown: Dict[str, Any]
    spending_trend: str
    avg_transaction: int
    top_expenses: List[Dict[str, Any]]
    spending_type: str
    risk_patterns: List[str]
    overspending_categories: List[str]
    spending_feedback: Dict[str, Any]
    monthly_comparison: Dict[str, Any]
    saving_suggestions: Dict[str, Any]
    
    # 추가 사용자 정보
    monthly_income: Optional[int] = None
    current_savings: Optional[int] = None
    investment_period_preference: Optional[str] = None  # "단기", "중기", "장기"
    risk_preference: Optional[str] = None  # "안전", "보통", "적극"
    financial_goals: Optional[List[str]] = None  # ["비상자금", "내집마련", "노후준비", "여행자금"]

# 금융상품 추천 응답 스키마
class ProductRecommendationResponse(BaseModel):
    user_profile_analysis: str
    recommended_time_deposits: List[RecommendedTimeDeposit]
    recommended_savings: List[RecommendedSaving]
    portfolio_suggestion: str
    total_expected_benefit: int
    investment_strategy: str
    cautions: List[str]
