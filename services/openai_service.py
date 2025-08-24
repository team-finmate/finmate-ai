# services/openai_service.py
import json
from openai import OpenAI
from typing import List, Dict, Any
from core.config import OPENAI_API_KEY, SYSTEM_INSTRUCTIONS
from services.saving_service import SavingService


class OpenAIService:
    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.saving_service = SavingService()
    
    def analyze_transactions(self, enriched_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        보강된 거래 데이터를 OpenAI API로 분석하여 패턴 추출 + 3단계 절약 제안 생성
        
        Args:
            enriched_data: 보강된 거래 내역 리스트
            
        Returns:
            분석 결과 딕셔너리 (기존 분석 + 3단계 절약 제안 포함)
        """
        try:
            # OpenAI API 호출 (기존 분석)
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
            
            # JSON 응답 파싱
            result = json.loads(response.choices[0].message.content)
            
            # 3단계 절약 제안 생성 및 통합
            if "category_breakdown" in result and "total_spent" in result:
                saving_suggestions = self.saving_service.generate_saving_suggestions(
                    result["category_breakdown"], 
                    result["total_spent"]
                )
                
                # 기존 단순 절약 제안을 3단계 구조화된 제안으로 교체
                result["saving_suggestions"] = saving_suggestions
                
                # 추가 메타정보
                result["saving_summary"] = self.saving_service.get_saving_summary(saving_suggestions)
            
            return result
            
        except (json.JSONDecodeError, IndexError, Exception) as e:
            return {
                "error": "Failed to analyze transactions",
                "details": str(e)
            }
