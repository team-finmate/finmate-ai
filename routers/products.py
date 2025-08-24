from fastapi import APIRouter, HTTPException
from schemas.products import ProductRecommendationRequest, ProductRecommendationResponse
from services.product_recommendation_service import ProductRecommendationService
from services.ai_product_service import AIProductRecommendationService

router = APIRouter()

@router.post("/recommend-products", response_model=ProductRecommendationResponse)
async def recommend_financial_products(request: ProductRecommendationRequest):
    """
    사용자의 재정 분석 데이터를 바탕으로 정기예금과 적금 상품을 추천합니다.
    
    Parameters:
    - request: 사용자의 재정 분석 데이터 및 추가 정보
    
    Returns:
    - ProductRecommendationResponse: 추천 상품 목록과 분석 결과
    """
    try:
        # 기본 상품 추천 서비스
        recommendation_service = ProductRecommendationService()
        base_recommendation = recommendation_service.generate_recommendation(request)
        
        # AI 기반 추천 강화 (선택사항)
        try:
            ai_service = AIProductRecommendationService()
            enhanced_recommendation = ai_service.enhance_recommendation_with_ai(base_recommendation, request)
            return enhanced_recommendation
        except Exception as ai_error:
            # AI 서비스 실패 시 기본 추천만 반환
            print(f"AI 서비스 오류: {ai_error}")
            return base_recommendation
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상품 추천 생성 중 오류가 발생했습니다: {str(e)}")

@router.get("/products/time-deposits")
async def get_time_deposits():
    """
    모든 정기예금 상품 목록을 조회합니다.
    """
    try:
        service = ProductRecommendationService()
        return {"products": service.time_deposits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"정기예금 목록 조회 중 오류가 발생했습니다: {str(e)}")

@router.get("/products/savings")
async def get_saving_products():
    """
    모든 적금 상품 목록을 조회합니다.
    """
    try:
        service = ProductRecommendationService()
        return {"products": service.saving_products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"적금 목록 조회 중 오류가 발생했습니다: {str(e)}")

@router.post("/ai-recommend")
async def get_ai_product_recommendation(request: ProductRecommendationRequest):
    """
    AI만을 사용한 상품 추천을 제공합니다.
    """
    try:
        ai_service = AIProductRecommendationService()
        ai_recommendation = ai_service.generate_ai_recommendation(request)
        return {"ai_recommendation": ai_recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 상품 추천 생성 중 오류가 발생했습니다: {str(e)}")
