from openai import OpenAI
from core.config import OPENAI_API_KEY, SYSTEM_INSTRUCTIONS

client = OpenAI(api_key=OPENAI_API_KEY)
import json
from core.config import OPENAI_API_KEY
from schemas.products import ProductRecommendationRequest, ProductRecommendationResponse

class AIProductRecommendationService:
    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        self.client = client

    def generate_ai_recommendation(self, request: ProductRecommendationRequest) -> str:
        """OpenAI를 활용한 AI 상품 추천"""

        # 사용자 데이터를 JSON으로 변환
        user_data = request.dict()

        system_prompt = """
        당신은 전문 금융 상품 추천 AI입니다. 사용자의 소비 패턴과 재정 상황을 분석하여 
        정기예금과 적금 상품을 추천해주세요.
        
        추천 기준:
        1. 사용자의 위험 성향 (안전/보통/적극)
        2. 월 소득 대비 지출 비율
        3. 절약 가능 금액
        4. 투자 기간 선호도
        5. 재정 목표
        
        응답 형식:
        {
            "user_profile_analysis": "사용자 프로필 분석 결과",
            "recommended_strategy": "추천 투자 전략",
            "time_deposit_recommendation": {
                "suitable_period": "추천 투자 기간",
                "recommended_amount": "추천 투자 금액",
                "key_factors": ["고려 요소 1", "고려 요소 2", "고려 요소 3"]
            },
            "saving_recommendation": {
                "suitable_period": "추천 적금 기간", 
                "monthly_amount": "월 적립 권장 금액",
                "key_factors": ["고려 요소 1", "고려 요소 2", "고려 요소 3"]
            },
            "portfolio_advice": "포트폴리오 구성 조언",
            "cautions": ["주의사항 1", "주의사항 2", "주의사항 3"]
        }
        """

        user_prompt = f"""
        사용자 재정 분석 데이터:
        - 월 총 지출: {user_data.get('total_spent', 0):,}원
        - 지출 성향: {user_data.get('spending_type', '일반')}
        - 위험 패턴: {user_data.get('risk_patterns', [])}
        - 과소비 카테고리: {user_data.get('overspending_categories', [])}
        - 절약 제안: {user_data.get('saving_suggestions', {})}
        
        추가 정보:
        - 월 소득: {user_data.get('monthly_income', '정보없음')}원
        - 현재 저축액: {user_data.get('current_savings', '정보없음')}원
        - 투자 기간 선호: {user_data.get('investment_period_preference', '정보없음')}
        - 위험 선호도: {user_data.get('risk_preference', '정보없음')}
        - 재정 목표: {user_data.get('financial_goals', [])}
        
        위 정보를 바탕으로 정기예금과 적금 상품 추천 전략을 제시해주세요.
        """

        try:
            response = client.chat.completions.create(model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000)

            return response.choices[0].message.content

        except Exception as e:
            return f"AI 추천 생성 중 오류가 발생했습니다: {str(e)}"

    def enhance_recommendation_with_ai(self, base_recommendation: ProductRecommendationResponse, request: ProductRecommendationRequest) -> ProductRecommendationResponse:
        """기본 추천에 AI 인사이트 추가"""

        ai_analysis = self.generate_ai_recommendation(request)

        try:
            ai_data = json.loads(ai_analysis)

            # AI 분석으로 기존 분석 보강
            enhanced_analysis = f"{base_recommendation.user_profile_analysis}\n\nAI 분석: {ai_data.get('user_profile_analysis', '')}"
            enhanced_strategy = f"{base_recommendation.investment_strategy}\n\nAI 추천 전략: {ai_data.get('recommended_strategy', '')}"
            enhanced_portfolio = f"{base_recommendation.portfolio_suggestion}\n\nAI 포트폴리오 조언: {ai_data.get('portfolio_advice', '')}"

            # AI 주의사항 추가
            ai_cautions = ai_data.get('cautions', [])
            enhanced_cautions = base_recommendation.cautions + ai_cautions

            # 기존 추천 결과 업데이트
            base_recommendation.user_profile_analysis = enhanced_analysis
            base_recommendation.investment_strategy = enhanced_strategy
            base_recommendation.portfolio_suggestion = enhanced_portfolio
            base_recommendation.cautions = list(set(enhanced_cautions))  # 중복 제거

        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트로 추가
            base_recommendation.user_profile_analysis += f"\n\nAI 분석:\n{ai_analysis}"

        return base_recommendation
