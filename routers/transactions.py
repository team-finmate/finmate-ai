# routers/transactions.py
from fastapi import APIRouter
from typing import List
from schemas.transactions import Transaction, AnalysisResponse
from services.data_processor import enrich_transactions
from services.openai_service import OpenAIService

# 라우터 인스턴스 생성
router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

# OpenAI 서비스 인스턴스
openai_service = OpenAIService()


@router.post("/analyze/", response_model=AnalysisResponse)
def analyze_transactions(transactions: List[Transaction]):
    """
    결제 내역 리스트를 입력받아 분석 결과를 반환하는 엔드포인트.
    
    Args:
        transactions: 결제 내역 리스트 (Pydantic 모델)
        
    Returns:
        분석 결과 (시간대별 패턴, 금액 패턴, 3단계 절약 제안 포함)
    """
    # 1. Pydantic 모델 리스트를 딕셔너리 리스트로 변환
    transactions_dict = [txn.model_dump() for txn in transactions]
    
    # 2. 거래 내역 보강 (enrich)
    enriched_data = enrich_transactions(transactions_dict)

    # 3. OpenAI API를 통한 분석 + 3단계 절약 제안 생성
    result = openai_service.analyze_transactions(enriched_data)
    
    return result
