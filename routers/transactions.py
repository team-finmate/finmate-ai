# routers/transactions.py
from fastapi import APIRouter
from typing import List, Optional
from schemas.transactions import (
    Transaction, 
    AnalysisResponse, 
    BasicAnalysisResponse,
    MonthlyComparisonResponse,
    SavingSuggestionsResponse,
    SpendingFeedbackResponse,
    Goal
)
from services.data_processor import enrich_transactions
from services.analysis_service import AnalysisService
from services.saving_service import SavingService
from services.goal_analysis_service import GoalAnalysisService

# 라우터 인스턴스 생성
router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

# 서비스 인스턴스들
analysis_service = AnalysisService()
saving_service = SavingService()
goal_analysis_service = GoalAnalysisService()


# 1. 기본 분석 엔드포인트
@router.post("/analysis/basic", response_model=BasicAnalysisResponse)
def get_basic_analysis(transactions: List[Transaction]):
    """
    기본 거래 분석 (소비 패턴, 카테고리 분석, 위험 패턴)
    
    Args:
        transactions: 결제 내역 리스트
        
    Returns:
        기본 분석 결과 (총 지출액, 카테고리별 분석, 트렌드, 위험 패턴 등)
    """
    transactions_dict = [txn.model_dump() for txn in transactions]
    enriched_data = enrich_transactions(transactions_dict)
    result = analysis_service.get_basic_analysis(enriched_data)
    return result


# 2. 월간 비교 분석 엔드포인트 (자동 월별 분리)
@router.post("/analysis/monthly-comparison", response_model=MonthlyComparisonResponse)
def get_monthly_comparison(transactions: List[Transaction]):
    """
    월간 비교 분석 (자동 월별 분리)
    
    Args:
        transactions: 전체 거래 내역 리스트 (여러 달 포함 가능)
        
    Returns:
        월간 비교 분석 결과 (최신 2개월 기준 자동 비교)
    """
    transactions_dict = [txn.model_dump() for txn in transactions]
    enriched_data = enrich_transactions(transactions_dict)
    
    # 자동 월별 분리 및 분석
    result = analysis_service.get_monthly_comparison(enriched_data)
    return result


# 3. 절약 제안 엔드포인트 (목표 분석 포함)
@router.post("/suggestions/saving", response_model=SavingSuggestionsResponse)
def get_saving_suggestions(
    transactions: List[Transaction],
    goals: Optional[List[Goal]] = None,
    current_monthly_surplus: Optional[float] = 0
):
    """
    3단계 레벨별 절약 전략 제안 및 목표 달성 분석
    
    Args:
        transactions: 결제 내역 리스트
        goals: 사용자 목표 리스트 (선택사항)
        current_monthly_surplus: 현재 월간 여유 자금 (선택사항)
        
    Returns:
        3단계 절약 제안 + 목표 달성 분석
    """
    transactions_dict = [txn.model_dump() for txn in transactions]
    enriched_data = enrich_transactions(transactions_dict)
    
    # 기본 분석으로 카테고리 정보 추출
    basic_analysis = analysis_service.get_basic_analysis(enriched_data)
    
    if "category_breakdown" in basic_analysis and "total_spent" in basic_analysis:
        # 절약 제안 생성
        saving_suggestions = saving_service.generate_saving_suggestions(
            basic_analysis["category_breakdown"], 
            basic_analysis["total_spent"]
        )
        saving_summary = saving_service.get_saving_summary(saving_suggestions)
        
        # 목표 달성 분석 (목표가 제공된 경우)
        goal_achievement_analysis = None
        if goals:
            goal_achievement_analysis = goal_analysis_service.analyze_goals_achievement(
                goals, saving_suggestions, current_monthly_surplus
            )
        
        return {
            "saving_suggestions": saving_suggestions,
            "saving_summary": saving_summary,
            "goal_achievement_analysis": goal_achievement_analysis
        }
    else:
        return {"error": "절약 제안 생성을 위한 기본 분석 실패"}


# 4. 소비습관 피드백 엔드포인트
@router.post("/feedback/habits", response_model=SpendingFeedbackResponse)
def get_spending_feedback(transactions: List[Transaction]):
    """
    개인화된 소비습관 피드백
    
    Args:
        transactions: 결제 내역 리스트
        
    Returns:
        소비습관 피드백 (팁, 진행률, 긍정적 변화, 개선 가이드)
    """
    transactions_dict = [txn.model_dump() for txn in transactions]
    enriched_data = enrich_transactions(transactions_dict)
    
    # 기본 분석 결과를 컨텍스트로 활용
    basic_analysis = analysis_service.get_basic_analysis(enriched_data)
    result = analysis_service.get_spending_feedback(enriched_data, basic_analysis)
    return result


# 5. 종합 분석 엔드포인트 (기존 유지 - 레거시 지원)
@router.post("/analyze/", response_model=AnalysisResponse)
def analyze_transactions(transactions: List[Transaction]):
    """
    결제 내역 리스트를 입력받아 전체 분석 결과를 반환하는 엔드포인트.
    
    Args:
        transactions: 결제 내역 리스트 (Pydantic 모델)
        
    Returns:
        전체 분석 결과 (모든 분석 결과 통합)
    """
    transactions_dict = [txn.model_dump() for txn in transactions]
    enriched_data = enrich_transactions(transactions_dict)
    result = analysis_service.get_full_analysis(enriched_data)
    return result
