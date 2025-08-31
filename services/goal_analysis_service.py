# services/goal_analysis_service.py
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from schemas.transactions import Goal, GoalAchievementAnalysis
import calendar


class GoalAnalysisService:
    """목표 달성 가능성 분석 서비스"""
    
    def __init__(self):
        # 목표 유형별 기본 정보
        self.goal_types = {
            "TRAVEL": {"name": "여행 자금", "priority": "중간", "flexibility": "높음"},
            "HOUSE": {"name": "주택 자금", "priority": "높음", "flexibility": "낮음"},
            "MARRIAGE": {"name": "결혼 자금", "priority": "높음", "flexibility": "중간"},
            "CAR": {"name": "자동차 구입", "priority": "중간", "flexibility": "중간"},
            "EMERGENCY": {"name": "비상금", "priority": "높음", "flexibility": "낮음"},
            "EDUCATION": {"name": "교육비", "priority": "높음", "flexibility": "낮음"},
            "CUSTOM": {"name": "기타 목표", "priority": "중간", "flexibility": "높음"}
        }
    
    def analyze_goals_achievement(self, 
                                goals: List[Goal], 
                                saving_suggestions: Dict[str, Any],
                                current_monthly_surplus: float = 0) -> List[GoalAchievementAnalysis]:
        """
        사용자의 목표들에 대한 달성 가능성 분석
        
        Args:
            goals: 사용자 목표 리스트
            saving_suggestions: 절약 제안 데이터
            current_monthly_surplus: 현재 월간 여유 자금
            
        Returns:
            목표별 달성 분석 결과
        """
        analyses = []
        
        for goal in goals:
            if goal.status == "ACTIVE":
                analysis = self._analyze_single_goal(goal, saving_suggestions, current_monthly_surplus)
                analyses.append(analysis)
        
        # 우선순위 순으로 정렬
        analyses.sort(key=lambda x: self._get_priority_score(x.goal_type), reverse=True)
        
        return analyses
    
    def _analyze_single_goal(self, 
                           goal: Goal, 
                           saving_suggestions: Dict[str, Any],
                           current_surplus: float) -> GoalAchievementAnalysis:
        """단일 목표에 대한 달성 분석"""
        
        # 기본 계산
        remaining_amount = goal.target_amount - goal.current_amount
        months_remaining = self._calculate_months_remaining(goal.target_date)
        required_monthly_saving = remaining_amount / months_remaining if months_remaining > 0 else remaining_amount
        
        # 절약 수준별 가능한 월간 절약 금액
        available_savings = {
            "강한절약": saving_suggestions.get("강한절약", {}).get("expected_saving", 0),
            "보통절약": saving_suggestions.get("보통절약", {}).get("expected_saving", 0),
            "약한절약": saving_suggestions.get("약한절약", {}).get("expected_saving", 0)
        }
        
        # 달성 가능성 분석
        achievement_analysis = self._calculate_achievement_probability(
            required_monthly_saving, available_savings, current_surplus, months_remaining
        )
        
        return GoalAchievementAnalysis(
            goal_id=goal.id or "unknown",
            goal_name=goal.custom_name or self.goal_types.get(goal.type, {}).get("name", goal.name),
            goal_type=goal.type,
            target_amount=goal.target_amount,
            current_amount=goal.current_amount,
            target_date=goal.target_date,
            required_monthly_saving=required_monthly_saving,
            is_achievable=achievement_analysis["is_achievable"],
            achievement_probability=achievement_analysis["probability"],
            recommended_saving_level=achievement_analysis["recommended_level"],
            months_remaining=months_remaining,
            shortfall_amount=achievement_analysis["shortfall"],
            analysis_message=achievement_analysis["message"]
        )
    
    def _calculate_months_remaining(self, target_date: date) -> int:
        """목표일까지 남은 개월 수 계산"""
        today = date.today()
        if target_date <= today:
            return 0
        
        # 년도와 월 차이 계산
        months = (target_date.year - today.year) * 12 + (target_date.month - today.month)
        
        # 일수 고려하여 조정
        if target_date.day > today.day:
            months += 1
        
        return max(1, months)  # 최소 1개월
    
    def _calculate_achievement_probability(self, 
                                        required_monthly: float,
                                        available_savings: Dict[str, float],
                                        current_surplus: float,
                                        months_remaining: int) -> Dict[str, Any]:
        """달성 확률 및 권장 절약 수준 계산"""
        
        # 현재 여유자금만으로 달성 가능한지 확인
        if current_surplus >= required_monthly:
            return {
                "is_achievable": True,
                "probability": 95.0,
                "recommended_level": "현재_여유자금",
                "shortfall": 0,
                "message": f"현재 여유자금({current_surplus:,.0f}원)만으로도 목표 달성 가능합니다."
            }
        
        # 절약 수준별 달성 가능성 체크
        for level, saving_amount in available_savings.items():
            total_available = current_surplus + saving_amount
            
            if total_available >= required_monthly:
                probability = self._calculate_probability_by_level(level, months_remaining)
                shortfall = required_monthly - total_available
                
                return {
                    "is_achievable": True,
                    "probability": probability,
                    "recommended_level": level,
                    "shortfall": shortfall,
                    "message": f"{level}으로 월 {saving_amount:,.0f}원 절약하면 목표 달성 가능합니다."
                }
        
        # 모든 절약 수준으로도 달성 불가능한 경우
        max_available = current_surplus + max(available_savings.values())
        shortfall = required_monthly - max_available
        
        return {
            "is_achievable": False,
            "probability": 20.0,
            "recommended_level": "강한절약",
            "shortfall": shortfall,
            "message": f"현재 절약으로는 월 {shortfall:,.0f}원 부족합니다. 목표 기간 연장이나 목표 금액 조정을 고려해보세요."
        }
    
    def _calculate_probability_by_level(self, level: str, months_remaining: int) -> float:
        """절약 수준과 기간에 따른 달성 확률 계산"""
        
        base_probabilities = {
            "강한절약": 70.0,  # 높은 절약이지만 실행 난이도 높음
            "보통절약": 85.0,  # 중간 절약, 적당한 실행 가능성
            "약한절약": 90.0   # 낮은 절약이지만 실행 용이
        }
        
        base_prob = base_probabilities.get(level, 50.0)
        
        # 기간에 따른 확률 조정
        if months_remaining <= 6:
            # 단기 목표: 확률 감소 (급하게 모으기 어려움)
            base_prob *= 0.8
        elif months_remaining <= 12:
            # 중기 목표: 확률 유지
            base_prob *= 1.0
        elif months_remaining <= 24:
            # 장기 목표: 확률 증가 (충분한 시간)
            base_prob *= 1.1
        else:
            # 초장기 목표: 확률 소폭 감소 (목표 변경 가능성)
            base_prob *= 0.95
        
        return min(95.0, max(10.0, base_prob))
    
    def _get_priority_score(self, goal_type: str) -> int:
        """목표 유형별 우선순위 점수"""
        priority_scores = {
            "EMERGENCY": 100,  # 비상금 (최우선)
            "HOUSE": 90,       # 주택자금
            "EDUCATION": 80,   # 교육비
            "MARRIAGE": 70,    # 결혼자금
            "CAR": 50,         # 자동차
            "TRAVEL": 30,      # 여행
            "CUSTOM": 40       # 기타
        }
        return priority_scores.get(goal_type, 40)
    
    def get_goal_recommendations(self, analyses: List[GoalAchievementAnalysis]) -> List[str]:
        """목표 기반 추가 권장사항 생성"""
        
        recommendations = []
        
        # 달성 불가능한 목표가 있는 경우
        unachievable_goals = [a for a in analyses if not a.is_achievable]
        if unachievable_goals:
            recommendations.append("일부 목표의 달성이 어려울 수 있습니다. 목표 기간 연장이나 금액 조정을 고려해보세요.")
        
        # 단기 목표가 여러 개인 경우
        short_term_goals = [a for a in analyses if a.months_remaining <= 12]
        if len(short_term_goals) > 2:
            recommendations.append("단기 목표가 많습니다. 우선순위를 정해 순차적으로 달성하는 것을 권장합니다.")
        
        # 높은 절약 수준이 필요한 목표가 많은 경우
        high_saving_needed = [a for a in analyses if a.recommended_saving_level == "강한절약"]
        if len(high_saving_needed) > 1:
            recommendations.append("여러 목표가 강한 절약을 요구합니다. 현실적인 목표 조정을 고려해보세요.")
        
        return recommendations
