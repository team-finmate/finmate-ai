# services/analysis_service.py
import json
from openai import OpenAI
from typing import List, Dict, Any
from core.config import OPENAI_API_KEY, SYSTEM_INSTRUCTIONS
from services.saving_service import SavingService


class AnalysisService:
    """거래 내역 분석을 담당하는 서비스 클래스"""
    
    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.saving_service = SavingService()
    
    def get_basic_analysis(self, enriched_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        기본 거래 분석 (소비 패턴, 카테고리 분석, 위험 패턴)
        
        Args:
            enriched_data: 보강된 거래 내역 리스트
            
        Returns:
            기본 분석 결과
        """
        try:
            # 기본 분석에 특화된 시스템 프롬프트
            basic_analysis_prompt = self._get_basic_analysis_prompt()
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": basic_analysis_prompt},
                    {
                        "role": "user",
                        "content": f"다음 결제내역의 기본 분석을 수행해줘:\n{json.dumps(enriched_data, ensure_ascii=False)}"
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"기본 분석 실패: {str(e)}"}
    
    def get_monthly_comparison(self, enriched_data: List[Dict[str, Any]], previous_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        월간 비교 분석
        
        Args:
            enriched_data: 현재 달 거래 데이터 또는 전체 거래 데이터
            previous_data: 이전 달 거래 데이터 (선택사항, 없으면 자동 분리)
            
        Returns:
            월간 비교 분석 결과
        """
        try:
            # 이전 달 데이터가 없으면 자동으로 월별 분리
            if previous_data is None:
                from services.data_processor import separate_transactions_by_month
                current_data, previous_data = separate_transactions_by_month(enriched_data)
                
                # 분리된 데이터에 대해 보강 처리
                from services.data_processor import enrich_transactions
                current_enriched = enrich_transactions(current_data)
                previous_enriched = enrich_transactions(previous_data) if previous_data else []
                
            else:
                current_enriched = enriched_data
                previous_enriched = previous_data
            
            monthly_comparison_prompt = self._get_monthly_comparison_prompt()
            
            user_content = f"현재 달 데이터:\n{json.dumps(current_enriched, ensure_ascii=False)}"
            if previous_enriched:
                user_content += f"\n\n이전 달 데이터:\n{json.dumps(previous_enriched, ensure_ascii=False)}"
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": monthly_comparison_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return result
            
        except Exception as e:
            return {"error": f"월간 비교 분석 실패: {str(e)}"}
    
    def get_spending_feedback(self, enriched_data: List[Dict[str, Any]], analysis_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        소비습관 피드백 생성
        
        Args:
            enriched_data: 보강된 거래 내역
            analysis_context: 기본 분석 결과 (선택사항)
            
        Returns:
            소비습관 피드백
        """
        try:
            feedback_prompt = self._get_spending_feedback_prompt()
            
            user_content = f"거래 데이터:\n{json.dumps(enriched_data, ensure_ascii=False)}"
            if analysis_context:
                user_content += f"\n\n분석 컨텍스트:\n{json.dumps(analysis_context, ensure_ascii=False)}"
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": feedback_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"소비습관 피드백 생성 실패: {str(e)}"}
    
    def get_full_analysis(self, enriched_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        전체 종합 분석 (기존 analyze와 동일)
        
        Args:
            enriched_data: 보강된 거래 내역 리스트
            
        Returns:
            전체 분석 결과
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                    {
                        "role": "user",
                        "content": f"다음 결제내역(버킷팅/힌트 포함)을 집계해줘. 반드시 유효한 JSON만 출력:\n{json.dumps(enriched_data, ensure_ascii=False)}"
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # 절약 제안 통합
            if "category_breakdown" in result and "total_spent" in result:
                saving_suggestions = self.saving_service.generate_saving_suggestions(
                    result["category_breakdown"], 
                    result["total_spent"]
                )
                result["saving_suggestions"] = saving_suggestions
                result["saving_summary"] = self.saving_service.get_saving_summary(saving_suggestions)
            
            return result
            
        except Exception as e:
            return {"error": f"전체 분석 실패: {str(e)}"}
    
    def _get_basic_analysis_prompt(self) -> str:
        """기본 분석용 시스템 프롬프트"""
        return """
너는 개인의 결제내역을 분석하여 기본적인 소비 패턴을 제공하는 금융 분석가다.

[분석 대상 카테고리 (16개)]
1. 쇼핑 2. 식비 3. 여행/숙박 4. 보험/세금/기타금융 5. 카페/간식 6. 취미/여가 
7. 이체 8. 교통/자동차 9. 술/유흥 10. 생활 11. 의료/건강/피트니스 
12. 편의점/마트/잡화 13. 주거/통신 14. 교육 15. 미용 16. 카테고리 없음

[출력 형식(JSON만)]
{
  "total_spent": 0,
  "category_breakdown": {
    "카테고리명": {"amount": 0, "ratio": 0.0, "transaction_count": 0, "avg_amount": 0}
  },
  "spending_trend": "상승|하락|안정",
  "avg_transaction": 0,
  "top_expenses": [
    {"merchant": "상점명", "amount": 0, "category": "카테고리"}
  ],
  "spending_type": "소비 패턴 요약",
  "risk_patterns": ["위험 패턴 목록"],
  "overspending_categories": ["과소비 카테고리 목록"]
}

기본적인 지출 집계와 패턴 분석에만 집중하여 결과를 제공하세요.
"""
    
    def _get_monthly_comparison_prompt(self) -> str:
        """월간 비교 분석용 시스템 프롬프트"""
        return """
너는 월간 지출 변동을 분석하는 금융 분석가다.

[출력 형식(JSON만)]
{
  "monthly_comparison": {
    "all_categories": [
      {"category": "카테고리명", "current_amount": 0, "previous_amount": 0, "change_amount": 0, "change_rate": 0.0}
    ]
  }
}

[분석 가이드라인]
- 현재 달에 지출이 있는 모든 카테고리를 포함 (금액이 0인 카테고리 제외)
- 이전 달 데이터가 있는 경우: 실제 증감 금액과 증감율(%) 정확히 계산
- 이전 달 데이터가 없는 경우: previous_amount=0, change_amount=current_amount, change_rate=100.0으로 설정
- change_rate 기준 오름차순 정렬 (가장 감소한 카테고리부터 가장 증가한 카테고리 순)
- 모든 카테고리 포함 (지출이 있는 카테고리와 관계 없이 전체 16개 카테고리를 모두 표시)
- 증감 구분 없이 전체 지출 변동 패턴을 한눈에 파악 가능하도록 구성

"""
    
    def _get_spending_feedback_prompt(self) -> str:
        """소비습관 피드백용 시스템 프롬프트"""
        return """
너는 개인화된 소비습관 피드백을 제공하는 금융 코치다.

[출력 형식(JSON만)]
{
  "spending_feedback": {
    "spending_tips": ["실용적인 지출 관리 팁 목록"],
    "goal_progress": "목표 달성 속도 및 진행 상황 평가",
    "positive_changes": ["이전 달 대비 잘한 점 칭찬 목록"],
    "improvement_guide": ["소비 습관 개선을 위한 구체적 가이드"]
  }
}

[피드백 가이드라인]
- spending_tips: 현재 소비 패턴에 맞는 실용적 관리 방법 (3-5개)
- goal_progress: 절약 목표 대비 현재 진행 상황 평가
- positive_changes: 이전 달 대비 개선된 소비 습관 칭찬 (2-3개)
- improvement_guide: 단계별 소비 습관 개선 방법 (3-4개)

긍정적이고 격려하는 톤으로 구체적이고 실행 가능한 피드백을 제공하세요.
"""
