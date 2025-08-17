# services/openai_service.py
import json
from openai import OpenAI
from typing import List, Dict, Any
from core.config import OPENAI_API_KEY, SYSTEM_INSTRUCTIONS


class OpenAIService:
    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def analyze_transactions(self, enriched_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        보강된 거래 데이터를 OpenAI API로 분석하여 패턴 추출
        
        Args:
            enriched_data: 보강된 거래 내역 리스트
            
        Returns:
            분석 결과 딕셔너리 (시간대별 패턴, 금액 패턴 포함)
        """
        try:
            # OpenAI API 호출
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
            return result
            
        except (json.JSONDecodeError, IndexError, Exception) as e:
            return {
                "error": "Failed to analyze transactions",
                "details": str(e)
            }
