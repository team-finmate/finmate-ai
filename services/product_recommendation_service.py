import json
from typing import List, Dict, Any
from schemas.products import (
    ProductRecommendationRequest,
    ProductRecommendationResponse,
    TimeDepositProduct,
    SavingProduct,
    RecommendedTimeDeposit,
    RecommendedSaving,
    ProductRecommendationReason
)

class ProductRecommendationService:
    def __init__(self):
        self.time_deposits = self.load_time_deposits()
        self.saving_products = self.load_saving_products()
        
    def load_time_deposits(self) -> List[TimeDepositProduct]:
        """정기예금 상품 데이터 로드"""
        try:
            with open('time_deposits.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [TimeDepositProduct(**item) for item in data[:50]]  # 상위 50개만 로드
        except FileNotFoundError:
            return []
            
    def load_saving_products(self) -> List[SavingProduct]:
        """적금 상품 데이터 로드"""
        try:
            with open('savings_products.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [SavingProduct(**item) for item in data[:100]]  # 상위 100개만 로드
        except FileNotFoundError:
            return []
    
    def analyze_user_profile(self, request: ProductRecommendationRequest) -> Dict[str, Any]:
        """사용자 프로필 분석"""
        total_spent = request.total_spent
        saving_potential = 0
        
        # 절약 가능 금액 계산
        if 'saving_suggestions' in request.dict() and request.saving_suggestions:
            for level, data in request.saving_suggestions.items():
                if isinstance(data, dict) and 'expected_saving' in data:
                    saving_potential = max(saving_potential, data['expected_saving'])
        
        # 수입 대비 지출 비율 계산
        spending_ratio = 0.0
        if request.monthly_income and request.monthly_income > 0:
            spending_ratio = total_spent / request.monthly_income
            
        # 위험 성향 분석
        risk_level = "보통"
        if request.risk_preference:
            risk_level = request.risk_preference
        elif len(request.risk_patterns) > 2:
            risk_level = "적극"
        elif request.spending_type == "안정형":
            risk_level = "안전"
            
        return {
            'total_spent': total_spent,
            'saving_potential': saving_potential,
            'spending_ratio': spending_ratio,
            'risk_level': risk_level,
            'financial_goals': request.financial_goals or [],
            'current_savings': request.current_savings or 0,
            'monthly_income': request.monthly_income or 0
        }
    
    def calculate_recommendation_score(self, product, user_profile: Dict[str, Any], product_type: str) -> float:
        """상품 추천 점수 계산"""
        score = 0.0
        
        # 기본 금리 점수 (40%)
        if product_type == "time_deposit":
            interest_rate = product.세전우대합계_num
        else:  # saving
            interest_rate = product.세전우대합계_num
        score += interest_rate * 400
        
        # 사용자 위험 성향 매칭 (20%)
        risk_level = user_profile['risk_level']
        if risk_level == "안전":
            # 저축은행이 아닌 경우 가점
            if "저축은행" not in product.금융회사:
                score += 20
            else:
                score += 10
        elif risk_level == "적극" and interest_rate > 0.04:
            score += 20
        else:
            score += 15
            
        # 가입 편의성 (15%)
        if product_type == "time_deposit":
            if "모바일" in product.가입채널:
                score += 10
            if "인터넷" in product.가입채널:
                score += 5
        else:  # saving
            if "인터넷뱅킹" in " ".join(product.가입채널) or "모바일" in " ".join(product.가입채널):
                score += 10
            elif "미확인" not in product.가입채널:
                score += 5
            
        # 우대 조건 접근성 (15%)
        accessible_conditions = 0
        for condition in product.우대금리세부내역:
            if any(keyword in condition for keyword in ["급여이체", "자동이체", "카드실적", "모바일", "앱", "결제", "페이", "첫거래"]):
                accessible_conditions += 1
        score += min(accessible_conditions * 3, 15)
        
        # 금액 적합성 (10%)
        if product_type == "time_deposit":
            if hasattr(product, '최소가입금액') and user_profile['current_savings'] >= product.최소가입금액:
                score += 10
        else:  # saving
            monthly_available = user_profile['saving_potential'] // 12 if user_profile['saving_potential'] > 0 else 100000
            if product.최소월적립액 <= monthly_available <= product.최대월적립액:
                score += 10
                
        return min(score, 100.0)
    
    def get_recommendation_reasons(self, product, user_profile: Dict[str, Any], product_type: str) -> List[ProductRecommendationReason]:
        """추천 이유 생성"""
        reasons = []
        
        # 높은 금리
        if product_type == "time_deposit":
            interest_rate = product.세전우대합계_num
        else:  # saving
            interest_rate = product.세전우대합계_num
            
        if interest_rate > 0.05:
            reasons.append(ProductRecommendationReason(
                reason_title="높은 금리 혜택",
                reason_detail=f"최대 연 {interest_rate*100:.2f}%의 우대금리로 높은 수익 기대",
                benefit_description=f"시중 평균보다 높은 금리로 안정적인 수익 창출 가능"
            ))
        
        # 우대 조건 접근성
        easy_conditions = [cond for cond in product.우대금리세부내역 
                          if any(keyword in cond for keyword in ["급여이체", "자동이체", "카드실적", "결제", "페이", "첫거래"])]
        if easy_conditions:
            reasons.append(ProductRecommendationReason(
                reason_title="접근 가능한 우대 조건",
                reason_detail="일상 생활에서 쉽게 충족할 수 있는 우대 조건",
                benefit_description=f"{len(easy_conditions)}개의 우대 조건으로 추가 금리 혜택 가능"
            ))
        
        # 예금자 보호 (정기예금만)
        if product_type == "time_deposit" and hasattr(product, '예금자보호여부') and product.예금자보호여부:
            reasons.append(ProductRecommendationReason(
                reason_title="안전한 투자",
                reason_detail="예금보험공사 보호로 원금 보장",
                benefit_description="최대 5천만원까지 예금자 보호로 안전한 투자"
            ))
        elif product_type == "saving":
            # 적금의 경우 안전성 관련 다른 메시지
            reasons.append(ProductRecommendationReason(
                reason_title="체계적 목돈 마련",
                reason_detail=f"{product.적립방식}으로 꾸준한 적립 가능",
                benefit_description="매월 일정액 적립으로 목표 달성에 효과적"
            ))
        
        # 편리한 가입 (정기예금만 - 적금은 가입채널 정보가 부정확할 수 있음)
        if product_type == "time_deposit" and "모바일" in product.가입채널:
            reasons.append(ProductRecommendationReason(
                reason_title="편리한 모바일 가입",
                reason_detail="언제 어디서나 모바일로 간편하게 가입",
                benefit_description="방문 없이도 간편하게 가입 가능"
            ))
        elif product_type == "saving" and "미확인" not in product.가입채널:
            reasons.append(ProductRecommendationReason(
                reason_title="편리한 가입 절차",
                reason_detail="다양한 채널을 통한 편리한 가입",
                benefit_description="본인에게 맞는 가입 방법 선택 가능"
            ))
            
        return reasons[:3]  # 최대 3개까지
    
    def recommend_time_deposits(self, request: ProductRecommendationRequest, user_profile: Dict[str, Any]) -> List[RecommendedTimeDeposit]:
        """정기예금 추천"""
        recommendations = []
        
        # 가용 예치 금액 계산
        available_amount = user_profile['current_savings'] or user_profile['saving_potential'] or 1000000
        
        for product in self.time_deposits:
            if product.판매상태 != "판매중":
                continue
                
            if available_amount < product.최소가입금액:
                continue
                
            score = self.calculate_recommendation_score(product, user_profile, "time_deposit")
            
            if score > 30:  # 최소 점수 기준
                recommended_amount = min(available_amount, product.권장예치금액)
                expected_interest = int(recommended_amount * product.세전우대합계_num * (product.기간개월 / 12))
                
                reasons = self.get_recommendation_reasons(product, user_profile, "time_deposit")
                
                fit_analysis = self.generate_fit_analysis(product, user_profile, "time_deposit")
                
                recommendations.append(RecommendedTimeDeposit(
                    product=product,
                    recommendation_score=score,
                    recommended_amount=recommended_amount,
                    expected_interest=expected_interest,
                    reasons=reasons,
                    fit_analysis=fit_analysis
                ))
        
        # 점수 순으로 정렬하여 상위 3개 반환
        recommendations.sort(key=lambda x: x.recommendation_score, reverse=True)
        return recommendations[:3]
    
    def recommend_savings(self, request: ProductRecommendationRequest, user_profile: Dict[str, Any]) -> List[RecommendedSaving]:
        """적금 추천"""
        recommendations = []
        
        # 월 납입 가능 금액 계산
        monthly_available = user_profile['saving_potential'] // 12 if user_profile['saving_potential'] > 0 else 200000
        
        for product in self.saving_products:
            if product.판매상태 != "판매중":
                continue
                
            if monthly_available < product.최소월적립액:
                continue
                
            score = self.calculate_recommendation_score(product, user_profile, "saving")
            
            if score > 30:  # 최소 점수 기준
                recommended_monthly = min(monthly_available, product.최대월적립액)
                
                # 기본 기간 사용
                period_months = product.기간개월_기본
                total_amount = recommended_monthly * period_months
                
                # 우대 금리 적용한 예상 이자 계산 (단순 계산)
                if product.이자계산방식 == "단리":
                    expected_interest = int(total_amount * product.세전우대합계_num * (period_months / 12))
                else:  # 복리
                    # 적금의 경우 월복리로 계산
                    monthly_rate = product.세전우대합계_num / 12
                    expected_interest = int(recommended_monthly * ((1 + monthly_rate) ** period_months - 1) / monthly_rate - total_amount)
                
                reasons = self.get_recommendation_reasons(product, user_profile, "saving")
                
                fit_analysis = self.generate_fit_analysis(product, user_profile, "saving")
                
                recommendations.append(RecommendedSaving(
                    product=product,
                    recommendation_score=score,
                    recommended_monthly_amount=recommended_monthly,
                    expected_total_amount=total_amount + expected_interest,
                    expected_interest=expected_interest,
                    reasons=reasons,
                    fit_analysis=fit_analysis
                ))
        
        # 점수 순으로 정렬하여 상위 3개 반환
        recommendations.sort(key=lambda x: x.recommendation_score, reverse=True)
        return recommendations[:3]
    
    def generate_fit_analysis(self, product, user_profile: Dict[str, Any], product_type: str) -> str:
        """개인 맞춤 분석 생성"""
        risk_level = user_profile['risk_level']
        
        if product_type == "time_deposit":
            if risk_level == "안전":
                return f"안전 지향적인 투자 성향에 적합한 {product.기간개월}개월 정기예금으로, 원금 보장과 안정적인 수익을 제공합니다."
            elif risk_level == "적극":
                return f"높은 수익률({product.세전우대합계_num*100:.2f}%)을 추구하는 성향에 맞는 상품으로, 우대 조건 충족 시 더 높은 수익 가능합니다."
            else:
                return f"균형 잡힌 투자 성향에 적합한 상품으로, 안정성과 수익성을 모두 고려한 선택입니다."
        else:  # saving
            monthly_amount = user_profile['saving_potential'] // 12 if user_profile['saving_potential'] > 0 else 200000
            return f"월 {monthly_amount:,}원 수준의 적립 계획에 적합한 {product.기간개월_기본}개월 {product.적립방식} 적금으로, 목돈 마련에 효과적입니다."
    
    def generate_portfolio_suggestion(self, user_profile: Dict[str, Any], time_deposits: List[RecommendedTimeDeposit], savings: List[RecommendedSaving]) -> str:
        """포트폴리오 제안 생성"""
        total_budget = user_profile['saving_potential'] or 1000000
        risk_level = user_profile['risk_level']
        
        if risk_level == "안전":
            return f"안전 중심 포트폴리오: 정기예금 70%, 적금 30%로 구성하여 원금 보장과 꾸준한 적립을 균형있게 진행하시기 바랍니다."
        elif risk_level == "적극":
            return f"수익 중심 포트폴리오: 고금리 상품 위주로 정기예금 60%, 적금 40%로 구성하여 높은 수익률을 추구하면서도 분산 투자 효과를 누리시기 바랍니다."
        else:
            return f"균형 포트폴리오: 정기예금과 적금을 50:50으로 구성하여 안정성과 수익성을 균형있게 추구하시기 바랍니다."
    
    def generate_recommendation(self, request: ProductRecommendationRequest) -> ProductRecommendationResponse:
        """전체 상품 추천 생성"""
        user_profile = self.analyze_user_profile(request)
        
        # 상품 추천
        recommended_time_deposits = self.recommend_time_deposits(request, user_profile)
        recommended_savings = self.recommend_savings(request, user_profile)
        
        # 프로필 분석
        spending_ratio = user_profile['spending_ratio']
        risk_level = user_profile['risk_level']
        
        user_profile_analysis = f"""
        사용자의 월 지출액은 {request.total_spent:,}원이며, 
        {"수입 대비 " + f"{spending_ratio*100:.1f}%" + " 지출하는" if request.monthly_income else ""}
        {risk_level} 성향의 투자자입니다.
        절약 가능 금액은 약 {user_profile['saving_potential']:,}원으로 분석되며,
        {'비상자금, 내집마련 등의 ' if user_profile['financial_goals'] else ''}목표를 위한 금융상품 가입을 권장합니다.
        """.strip()
        
        # 포트폴리오 제안
        portfolio_suggestion = self.generate_portfolio_suggestion(user_profile, recommended_time_deposits, recommended_savings)
        
        # 총 예상 수익 계산
        total_expected_benefit = 0
        for td in recommended_time_deposits:
            total_expected_benefit += td.expected_interest
        for sv in recommended_savings:
            total_expected_benefit += sv.expected_interest
            
        # 투자 전략
        investment_strategy = f"""
        현재 지출 패턴을 기반으로 한 분석 결과, 
        {risk_level} 성향에 맞는 상품 조합으로 연 평균 수익률 
        {(total_expected_benefit / max(user_profile['saving_potential'], 1000000) * 100):.2f}%를 기대할 수 있습니다.
        우대 조건을 충족하여 최대 금리 혜택을 받으시기 바랍니다.
        """
        
        # 주의사항
        cautions = [
            "금리는 시장 상황에 따라 변동될 수 있습니다.",
            "우대 조건을 충족하지 못할 경우 기본 금리가 적용됩니다.",
            "중도 해지 시 약정 금리보다 낮은 금리가 적용될 수 있습니다.",
            "예금자보호한도(5천만원)를 고려하여 분산 투자를 권장합니다."
        ]
        
        return ProductRecommendationResponse(
            user_profile_analysis=user_profile_analysis,
            recommended_time_deposits=recommended_time_deposits,
            recommended_savings=recommended_savings,
            portfolio_suggestion=portfolio_suggestion,
            total_expected_benefit=total_expected_benefit,
            investment_strategy=investment_strategy,
            cautions=cautions
        )
