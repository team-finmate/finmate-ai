"""
월별 자동 분리 API 테스트 스크립트
"""

import requests
import json
from datetime import date, timedelta

def test_monthly_comparison_api():
    """월별 비교 분석 API 테스트"""
    
    base_url = "http://localhost:8000"
    endpoint = "/transactions/analysis/monthly-comparison"
    
    # 테스트 데이터 - 2개월치 거래
    test_data = {
        "transactions": [
            # 2025년 1월 거래
            {
                "transaction_id": "TXN202501001",
                "date": "2025-01-15",
                "time": "12:30:00",
                "merchant": "스타벅스",
                "category": "카페",
                "amount": 5000,
                "payment_method": "신용카드",
                "balance": 500000
            },
            {
                "transaction_id": "TXN202501002",
                "date": "2025-01-20",
                "time": "19:00:00",
                "merchant": "CGV",
                "category": "문화/여가",
                "amount": 15000,
                "payment_method": "신용카드",
                "balance": 485000
            },
            {
                "transaction_id": "TXN202501003",
                "date": "2025-01-25",
                "time": "13:00:00",
                "merchant": "배달의민족",
                "category": "배달음식",
                "amount": 25000,
                "payment_method": "신용카드",
                "balance": 460000
            },
            # 2025년 2월 거래
            {
                "transaction_id": "TXN202502001",
                "date": "2025-02-05",
                "time": "10:30:00",
                "merchant": "이마트",
                "category": "마트",
                "amount": 50000,
                "payment_method": "신용카드",
                "balance": 410000
            },
            {
                "transaction_id": "TXN202502002",
                "date": "2025-02-10",
                "time": "14:00:00",
                "merchant": "스타벅스",
                "category": "카페",
                "amount": 6500,
                "payment_method": "신용카드",
                "balance": 403500
            },
            {
                "transaction_id": "TXN202502003",
                "date": "2025-02-15",
                "time": "18:30:00",
                "merchant": "올리브영",
                "category": "편의점",
                "amount": 30000,
                "payment_method": "신용카드",
                "balance": 373500
            }
        ]
    }
    
    print("🚀 월별 자동 분리 API 테스트")
    print("=" * 60)
    print(f"📍 엔드포인트: {base_url}{endpoint}")
    print(f"📊 테스트 데이터: {len(test_data['transactions'])}건의 거래")
    
    try:
        # API 호출
        response = requests.post(
            f"{base_url}{endpoint}",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n📤 응답 상태: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # 결과 분석
            monthly_comparison = result.get("monthly_comparison", {})
            all_categories = monthly_comparison.get("all_categories", [])
            
            print(f"✅ API 호출 성공!")
            print(f"\n📊 월별 비교 결과:")
            print(f"   전체 카테고리: {len(all_categories)}개")
            
            # 주요 카테고리 변화
            print(f"\n📈 주요 카테고리 변화:")
            for i, category in enumerate(all_categories[:5], 1):
                name = category.get('category', '미분류')
                current = category.get('current_amount', 0)
                previous = category.get('previous_amount', 0)
                change_rate = category.get('change_rate', 0)
                
                print(f"   {i}. {name}: {current:,}원 → {previous:,}원 ({change_rate:+.1f}%)")
            
            print(f"\n🎉 월별 자동 분리 기능 정상 작동!")
            return True
            
        else:
            error_detail = response.text
            print(f"❌ API 호출 실패: {error_detail}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ 서버 연결 실패. FastAPI 서버가 실행 중인지 확인해주세요.")
        print(f"💡 서버 시작: uvicorn main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False

def create_curl_command():
    """curl 명령어 생성"""
    
    print(f"\n🔧 curl 테스트 명령어:")
    print("=" * 60)
    
    curl_command = '''curl -X POST "http://localhost:8000/transactions/analysis/monthly-comparison" \\
     -H "Content-Type: application/json" \\
     -d '{
       "transactions": [
         {
           "transaction_id": "TXN001",
           "date": "2025-01-15",
           "time": "12:30:00",
           "merchant": "스타벅스",
           "category": "카페",
           "amount": 5000,
           "payment_method": "신용카드",
           "balance": 500000
         },
         {
           "transaction_id": "TXN002",
           "date": "2025-02-10",
           "time": "14:00:00",
           "merchant": "이마트",
           "category": "마트",
           "amount": 50000,
           "payment_method": "신용카드",
           "balance": 450000
         }
       ]
     }'
'''
    
    print(curl_command)
    
    print(f"\n📋 기능 요약:")
    features = [
        "✅ 하나의 거래 리스트만 전달",
        "✅ 자동으로 최신 2개월 분리",
        "✅ 단순한 응답 구조",
        "✅ 전체 카테고리 변화 분석",
        "✅ 기존 API 구조 호환"
    ]
    
    for feature in features:
        print(f"   {feature}")

if __name__ == "__main__":
    print("🎯 FinMate AI - 월별 자동 분리 API 테스트\n")
    
    # API 테스트 시도
    success = test_monthly_comparison_api()
    
    # curl 명령어 제공
    create_curl_command()
    
    if not success:
        print(f"\n🔧 서버를 시작한 후 다시 테스트해주세요:")
        print(f"   cd /Users/hwangsunbeom/Documents/GitHub/finmate-ai")
        print(f"   uvicorn main:app --reload --port 8000")
        print(f"   python api_test.py")
