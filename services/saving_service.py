# services/saving_service.py
from core.config import (
    SAVING_LEVELS, 
    SAVING_STRATEGIES, 
    SAVING_CALCULATION_RULES,
    CATEGORY_PRIORITY_SCORES,
    calculate_saving_amount,
    get_difficulty_level,
    generate_saving_method
)

class SavingService:
    """절약 제안 생성 서비스"""
    
    def generate_saving_suggestions(self, category_breakdown, total_spent):
        """
        카테고리별 지출 분석을 바탕으로 3단계 절약 제안 생성
        
        Args:
            category_breakdown: 카테고리별 지출 분석 데이터
            total_spent: 총 지출 금액
            
        Returns:
            dict: 3단계 절약 제안 데이터
        """
        suggestions = {}
        
        for level_key, level_config in SAVING_LEVELS.items():
            suggestions[level_key] = self._generate_level_suggestion(
                level_key, level_config, category_breakdown, total_spent
            )
        
        return suggestions
    
    def _generate_level_suggestion(self, level_key, level_config, category_breakdown, total_spent):
        """특정 레벨에 대한 절약 제안 생성"""
        
        # 레벨별 적용 가능한 카테고리 필터링
        applicable_categories = self._filter_applicable_categories(
            level_key, category_breakdown
        )
        
        # 우선순위에 따라 카테고리 정렬
        sorted_categories = self._sort_categories_by_priority(applicable_categories)
        
        # 절약 전략 생성 (최대 3-5개)
        strategies = []
        total_saving = 0
        max_strategies = 5 if level_key == "강한절약" else 3
        
        for category, data in sorted_categories[:max_strategies]:
            strategy = self._create_strategy(category, data, level_key)
            if strategy:
                strategies.append(strategy)
                total_saving += strategy["saving_amount"]
        
        # 전체 절약률 계산
        reduction_rate_range = f"{int(SAVING_CALCULATION_RULES[level_key]['min_target_reduction']*100)}-{int(SAVING_CALCULATION_RULES[level_key]['max_target_reduction']*100)}%"
        
        return {
            "level": level_config["name"],
            "description": level_config["description"],
            "expected_saving": total_saving,
            "reduction_rate": reduction_rate_range,
            "strategies": strategies
        }
    
    def _filter_applicable_categories(self, level_key, category_breakdown):
        """레벨에 따라 적용 가능한 카테고리 필터링"""
        rules = SAVING_CALCULATION_RULES[level_key]
        applicable = []
        
        for category, data in category_breakdown.items():
            # 제외 카테고리 체크
            if "exclude_categories" in rules and category in rules["exclude_categories"]:
                continue
            
            # 최소 금액 조건 (너무 작은 금액은 제외)
            min_amount = 5000 if level_key == "약한절약" else 10000
            if data["amount"] < min_amount:
                continue
                
            applicable.append((category, data))
        
        return applicable
    
    def _sort_categories_by_priority(self, categories):
        """카테고리를 우선순위와 금액에 따라 정렬"""
        return sorted(
            categories,
            key=lambda x: (
                CATEGORY_PRIORITY_SCORES.get(x[0], 0),  # 우선순위 점수
                x[1]["amount"]  # 지출 금액
            ),
            reverse=True
        )
    
    def _create_strategy(self, category, data, level_key):
        """개별 절약 전략 생성"""
        current_amount = data["amount"]
        transaction_count = data.get("transaction_count", 1)
        
        # 절약 금액 계산
        saving_amount = calculate_saving_amount(
            category, current_amount, level_key, transaction_count
        )
        
        # 목표 금액 계산
        target_amount = current_amount - saving_amount
        
        # 절약 방법 생성
        method = generate_saving_method(
            category, level_key, current_amount, transaction_count
        )
        
        # 실행 난이도 계산
        difficulty = get_difficulty_level(category, level_key, current_amount)
        
        return {
            "category": category,
            "current_amount": current_amount,
            "target_amount": target_amount,
            "saving_amount": saving_amount,
            "method": method,  # 이미 format된 문자열이므로 추가 format 불필요
            "difficulty": difficulty
        }
    
    def get_saving_summary(self, suggestions):
        """절약 제안 요약 정보 생성"""
        summary = {}
        
        for level_key, suggestion in suggestions.items():
            summary[level_key] = {
                "total_saving": suggestion["expected_saving"],
                "category_count": len(suggestion["strategies"]),
                "avg_difficulty": self._calculate_avg_difficulty(suggestion["strategies"]),
                "top_category": suggestion["strategies"][0]["category"] if suggestion["strategies"] else None
            }
        
        return summary
    
    def _calculate_avg_difficulty(self, strategies):
        """전략들의 평균 난이도 계산"""
        if not strategies:
            return "하"
        
        difficulty_scores = {"하": 1, "중": 2, "상": 3}
        avg_score = sum(difficulty_scores[s["difficulty"]] for s in strategies) / len(strategies)
        
        if avg_score <= 1.5:
            return "하"
        elif avg_score <= 2.5:
            return "중"
        else:
            return "상"

# 사용 예시
def example_usage():
    """절약 서비스 사용 예시"""
    
    # 예시 데이터
    sample_category_breakdown = {
        "배달음식": {"amount": 180000, "ratio": 0.25, "transaction_count": 12, "avg_amount": 15000},
        "카페/간식": {"amount": 120000, "ratio": 0.17, "transaction_count": 24, "avg_amount": 5000},
        "온라인쇼핑": {"amount": 95000, "ratio": 0.13, "transaction_count": 8, "avg_amount": 12000},
        "구독서비스": {"amount": 45000, "ratio": 0.06, "transaction_count": 5, "avg_amount": 9000},
        "교통/자동차": {"amount": 80000, "ratio": 0.11, "transaction_count": 15, "avg_amount": 5300}
    }
    
    total_spent = 720000
    
    # 절약 서비스 인스턴스 생성
    saving_service = SavingService()
    
    # 절약 제안 생성
    suggestions = saving_service.generate_saving_suggestions(
        sample_category_breakdown, total_spent
    )
    
    # 요약 정보 생성
    summary = saving_service.get_saving_summary(suggestions)
    
    return suggestions, summary

if __name__ == "__main__":
    suggestions, summary = example_usage()
    print("절약 제안 생성 완료!")
    print(f"강한절약 예상 절약액: {suggestions['강한절약']['expected_saving']:,}원")
    print(f"보통절약 예상 절약액: {suggestions['보통절약']['expected_saving']:,}원")
    print(f"약한절약 예상 절약액: {suggestions['약한절약']['expected_saving']:,}원")
