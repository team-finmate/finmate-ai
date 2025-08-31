# core/config.py
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# OpenAI API 키
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 1) 규칙 정의 -----------------------------------------------------------------
WEEKEND_DAYS = {5, 6}

WEEKDAY_BUCKETS = [
    ("07:00", "09:00", "출근길_아침"),
    ("09:00", "12:00", "오전_업무시간"),
    ("12:00", "14:00", "점심시간"),
    ("14:00", "18:00", "오후_업무시간"),
    ("18:00", "21:00", "저녁_퇴근후"),
    ("21:00", "24:00", "밤_휴식시간"),
    ("00:00", "07:00", "새벽_심야"),
]

WEEKEND_BUCKETS = [
    ("07:00", "10:00", "주말_아침"),
    ("10:00", "14:00", "주말_오전_활동"),
    ("14:00", "18:00", "주말_오후_활동"),
    ("18:00", "22:00", "주말_저녁"),
    ("22:00", "24:00", "주말_밤"),
    ("00:00", "07:00", "주말_새벽"),
]

# 금액 패턴 범위(원)을 16개 카테고리에 맞게 조정
AMOUNT_HINTS = [
    ("카페/간식", 3000, 8000),
    ("식비", 8000, 35000),  # 배달음식 포함
    ("편의점/마트/잡화", 2000, 15000),
    ("교통/자동차", 1000, 50000),
    ("취미/여가", 10000, 100000),
    ("술/유흥", 20000, 200000),
    ("쇼핑", 10000, 150000),  # 온라인쇼핑 대체
    ("주거/통신", 30000, 200000),  # 구독서비스 포함
    ("의료/건강/피트니스", 10000, 100000),
    ("여행/숙박", 50000, 500000),
    ("보험/세금/기타금융", 50000, 1000000),
    ("이체", 10000, 5000000),
    ("생활", 5000, 50000),
    ("교육", 30000, 500000),
    ("미용", 10000, 100000),
    ("카테고리 없음", 1000, 1000000),
]

# 상점/카테고리 키워드 → 라벨 힌트 (16개 카테고리 반영)
KEYWORD_HINTS = {
    # 식비 (배달/외식 포함)
    "배달의민족": "식비", "요기요": "식비", "배민": "식비",
    "쿠팡이츠": "식비", "위메프오": "식비", "맥도날드": "식비",
    "버거킹": "식비", "KFC": "식비", "롯데리아": "식비",
    "김밥천국": "식비", "백반": "식비", "한식": "식비",
    
    # 카페/간식
    "스타벅스": "카페/간식", "이디야": "카페/간식", "커피": "카페/간식",
    "투썸": "카페/간식", "빽다방": "카페/간식", "메가커피": "카페/간식",
    "베이커리": "카페/간식", "도넛": "카페/간식", "아이스크림": "카페/간식",
    
    # 편의점/마트/잡화
    "편의점": "편의점/마트/잡화", "CU": "편의점/마트/잡화", 
    "GS25": "편의점/마트/잡화", "세븐일레븐": "편의점/마트/잡화",
    "이마트": "편의점/마트/잡화", "홈플러스": "편의점/마트/잡화", 
    "롯데마트": "편의점/마트/잡화", "다이소": "편의점/마트/잡화",
    "올리브영": "편의점/마트/잡화", "왓슨스": "편의점/마트/잡화",
    
    # 쇼핑 (온라인/오프라인)
    "쿠팡": "쇼핑", "11번가": "쇼핑", "G마켓": "쇼핑",
    "옥션": "쇼핑", "위메프": "쇼핑", "티몬": "쇼핑",
    "무신사": "쇼핑", "29CM": "쇼핑", "브랜디": "쇼핑",
    "신세계": "쇼핑", "현대백화점": "쇼핑", "롯데백화점": "쇼핑",
    
    # 취미/여가
    "CGV": "취미/여가", "롯데시네마": "취미/여가", "메가박스": "취미/여가",
    "PC방": "취미/여가", "노래방": "취미/여가", "볼링": "취미/여가",
    "당구": "취미/여가", "게임": "취미/여가", "책": "취미/여가",
    
    # 주거/통신 (구독서비스 포함)
    "넷플릭스": "주거/통신", "유튜브": "주거/통신", "디즈니플러스": "주거/통신",
    "스포티파이": "주거/통신", "멜론": "주거/통신", "웨이브": "주거/통신",
    "통신비": "주거/통신", "인터넷": "주거/통신", "전기료": "주거/통신",
    "가스비": "주거/통신", "수도료": "주거/통신", "관리비": "주거/통신",
    "SK텔레콤": "주거/통신", "KT": "주거/통신", "LG유플러스": "주거/통신",
    
    # 교통/자동차
    "택시": "교통/자동차", "카카오택시": "교통/자동차", "우버": "교통/자동차",
    "주유": "교통/자동차", "지하철": "교통/자동차", "버스": "교통/자동차",
    "톨게이트": "교통/자동차", "주차": "교통/자동차", "렌터카": "교통/자동차",
    
    # 술/유흥
    "소주": "술/유흥", "맥주": "술/유흥", "와인": "술/유흥",
    "클럽": "술/유흥", "호프": "술/유흥", "바": "술/유흥",
    "치킨": "술/유흥", "술집": "술/유흥", "포차": "술/유흥",
    
    # 여행/숙박
    "여행": "여행/숙박", "호텔": "여행/숙박", "에어비앤비": "여행/숙박",
    "모텔": "여행/숙박", "펜션": "여행/숙박", "게스트하우스": "여행/숙박",
    "항공": "여행/숙박", "기차": "여행/숙박", "고속버스": "여행/숙박",
    
    # 의료/건강/피트니스
    "병원": "의료/건강/피트니스", "약국": "의료/건강/피트니스", "치과": "의료/건강/피트니스",
    "피트니스": "의료/건강/피트니스", "헬스장": "의료/건강/피트니스",
    "요가": "의료/건강/피트니스", "필라테스": "의료/건강/피트니스",
    "마사지": "의료/건강/피트니스", "사우나": "의료/건강/피트니스",
    
    # 교육
    "학원": "교육", "온라인강의": "교육", "책": "교육",
    "학용품": "교육", "강의": "교육", "세미나": "교육",
    
    # 미용
    "미용실": "미용", "네일": "미용", "피부관리": "미용",
    "성형외과": "미용", "화장품": "미용", "향수": "미용",
    
    # 생활
    "세탁소": "생활", "청소": "생활", "수리": "생활",
    "택배": "생활", "우체국": "생활", "은행": "생활",
    
    # 보험/세금/기타금융
    "보험": "보험/세금/기타금융", "세금": "보험/세금/기타금융", 
    "국민연금": "보험/세금/기타금융", "건강보험": "보험/세금/기타금융",
    "증권": "보험/세금/기타금융", "투자": "보험/세금/기타금융",
    
    # 이체
    "송금": "이체", "계좌이체": "이체", "입금": "이체",
    "출금": "이체", "ATM": "이체", "현금인출": "이체",
}

# 위험 패턴 감지 기준
RISK_PATTERNS = {
    "새벽_소비": ["새벽_심야", "주말_새벽"],  # 새벽 시간대 소비
    "고액_단건": 100000,  # 10만원 이상 단건 결제
    "반복_배달": {"category": "배달음식", "threshold": 3},  # 일정 기간 내 반복 배달
    "구독_과다": {"category": "구독서비스", "threshold": 5},  # 다수 구독 서비스
}

# 절약 제안 레벨별 구성 (16개 카테고리 반영)
SAVING_LEVELS = {
    "강한절약": {
        "name": "🔥 강한 절약",
        "description": "고정비를 포함한 전면적 지출 절약",
        "reduction_rate": 0.3,  # 30% 절약
        "includes_fixed_costs": True,
        "priority_categories": ["주거/통신", "보험/세금/기타금융", "식비", "쇼핑", "취미/여가"]
    },
    "보통절약": {
        "name": "💪 보통 절약", 
        "description": "주요 지출 카테고리 중심 절약",
        "reduction_rate": 0.2,  # 20% 절약
        "includes_fixed_costs": False,
        "priority_categories": ["식비", "카페/간식", "쇼핑", "교통/자동차", "취미/여가"]
    },
    "약한절약": {
        "name": "🌱 약한 절약",
        "description": "빈번하고 불필요한 소비 점진적 절약",
        "reduction_rate": 0.1,  # 10% 절약
        "includes_fixed_costs": False,
        "priority_categories": ["카페/간식", "편의점/마트/잡화", "술/유흥", "생활"]
    }
}

# 카테고리별 절약 전략 템플릿 (16개 카테고리)
SAVING_STRATEGIES = {
    # 고정비 관련
    "주거/통신": {
        "강한절약": "통신요금제 재검토 + 구독서비스 정리 + 불필요한 옵션 해지로 월 {amount:,}원 절약",
        "보통절약": "통신요금제 다운그레이드 + 사용하지 않는 구독 해지로 월 {amount:,}원 절약",
        "약한절약": "사용하지 않는 부가서비스 해지로 월 {amount:,}원 절약"
    },
    "보험/세금/기타금융": {
        "강한절약": "보험 상품 재검토 + 불필요한 금융상품 정리로 월 {amount:,}원 절약",
        "보통절약": "보험료 할인 혜택 적용으로 월 {amount:,}원 절약",
        "약한절약": "금융 수수료 최소화로 월 {amount:,}원 절약"
    },
    
    # 변동비 관련 - 주요 지출
    "식비": {
        "강한절약": "외식/배달을 주 {current_count}회에서 {target_count}회로 줄이고 직접 요리로 월 {amount:,}원 절약",
        "보통절약": "외식/배달 주문을 주 {reduce_count}회 줄여서 월 {amount:,}원 절약",
        "약한절약": "배달음식 대신 간편식 이용으로 주 1회 줄여서 월 {amount:,}원 절약"
    },
    "카페/간식": {
        "강한절약": "카페 이용을 하루 {current_count}회에서 {target_count}회로 줄이고 홈카페 활용으로 월 {amount:,}원 절약",
        "보통절약": "카페 방문을 주 {reduce_count}회 줄여서 월 {amount:,}원 절약",
        "약한절약": "간식 구매를 주 {reduce_count}회 줄여서 월 {amount:,}원 절약"
    },
    "쇼핑": {
        "강한절약": "충동구매 금지 + 필수품목만 구매 리스트 작성으로 월 {amount:,}원 절약",
        "보통절약": "쇼핑 빈도를 월 {current_count}회에서 {target_count}회로 줄여서 월 {amount:,}원 절약",
        "약한절약": "쿠폰 적극 활용 + 할인 시기 구매로 월 {amount:,}원 절약"
    },
    "교통/자동차": {
        "강한절약": "택시 이용을 대중교통으로 완전 대체하여 월 {amount:,}원 절약",
        "보통절약": "택시 이용을 주 {reduce_count}회 줄이고 대중교통 활용으로 월 {amount:,}원 절약",
        "약한절약": "가까운 거리는 도보/자전거 이용으로 월 {amount:,}원 절약"
    },
    "취미/여가": {
        "강한절약": "유료 여가활동을 무료/저렴한 대안으로 대체하여 월 {amount:,}원 절약",
        "보통절약": "여가 지출을 월 {budget:,}원 예산으로 제한하여 월 {amount:,}원 절약",
        "약한절약": "할인 혜택 적극 활용으로 월 {amount:,}원 절약"
    },
    
    # 변동비 관련 - 소액 지출
    "편의점/마트/잡화": {
        "강한절약": "편의점 이용을 마트 대량구매로 대체하여 월 {amount:,}원 절약",
        "보통절약": "편의점 방문을 주 {reduce_count}회 줄여서 월 {amount:,}원 절약",
        "약한절약": "필요한 것만 구매 리스트 작성으로 월 {amount:,}원 절약"
    },
    "술/유흥": {
        "강한절약": "유흥비를 월 {budget:,}원 예산으로 제한하여 월 {amount:,}원 절약",
        "보통절약": "술자리 빈도를 주 {reduce_count}회 줄여서 월 {amount:,}원 절약",
        "약한절약": "집에서 간단히 마시기로 월 {amount:,}원 절약"
    },
    "생활": {
        "강한절약": "생활 서비스를 직접 처리하거나 저렴한 대안으로 월 {amount:,}원 절약",
        "보통절약": "생활비 지출을 월 {budget:,}원 예산으로 제한하여 월 {amount:,}원 절약",
        "약한절약": "할인 서비스 적극 활용으로 월 {amount:,}원 절약"
    },
    
    # 기타 카테고리
    "여행/숙박": {
        "강한절약": "여행 횟수를 줄이고 국내 여행으로 대체하여 월 {amount:,}원 절약",
        "보통절약": "여행 예산을 월 {budget:,}원으로 제한하여 월 {amount:,}원 절약",
        "약한절약": "여행 예약 시 할인 혜택 적극 활용으로 월 {amount:,}원 절약"
    },
    "의료/건강/피트니스": {
        "강한절약": "헬스장을 홈트레이닝으로 대체하여 월 {amount:,}원 절약",
        "보통절약": "건강 관리 예산을 월 {budget:,}원으로 제한하여 월 {amount:,}원 절약",
        "약한절약": "건강보험 할인 혜택 적극 활용으로 월 {amount:,}원 절약"
    },
    "교육": {
        "강한절약": "온라인 강의로 대체하여 월 {amount:,}원 절약",
        "보통절약": "교육 예산을 월 {budget:,}원으로 제한하여 월 {amount:,}원 절약",
        "약한절약": "무료 교육 자료 적극 활용으로 월 {amount:,}원 절약"
    },
    "미용": {
        "강한절약": "미용실 방문 횟수를 줄이고 셀프케어로 월 {amount:,}원 절약",
        "보통절약": "미용 예산을 월 {budget:,}원으로 제한하여 월 {amount:,}원 절약",
        "약한절약": "미용 할인 혜택 적극 활용으로 월 {amount:,}원 절약"
    }
}

# 절약 계산 기준 (16개 카테고리 반영)
SAVING_CALCULATION_RULES = {
    "강한절약": {
        "min_target_reduction": 0.25,  # 최소 25% 절약
        "max_target_reduction": 0.4,   # 최대 40% 절약
        "include_categories": ["모든카테고리"],
        "strategy_focus": "구조적 변화"
    },
    "보통절약": {
        "min_target_reduction": 0.15,  # 최소 15% 절약
        "max_target_reduction": 0.25,  # 최대 25% 절약
        "exclude_categories": ["주거/통신", "의료/건강/피트니스", "교육", "보험/세금/기타금융", "이체"],
        "strategy_focus": "습관 개선"
    },
    "약한절약": {
        "min_target_reduction": 0.05,  # 최소 5% 절약
        "max_target_reduction": 0.15,  # 최대 15% 절약
        "exclude_categories": ["주거/통신", "의료/건강/피트니스", "교육", "교통/자동차", "보험/세금/기타금융", "이체"],
        "strategy_focus": "점진적 변화"
    }
}

# OpenAI 모델 시스템 지시문 (16개 카테고리 반영)
SYSTEM_INSTRUCTIONS = """
너는 개인의 결제내역을 분석하여 종합적인 소비 패턴 인사이트를 제공하는 금융 분석가다.

[분석 대상 카테고리 (16개)]
1. 쇼핑 2. 식비 3. 여행/숙박 4. 보험/세금/기타금융 5. 카페/간식 6. 취미/여가 
7. 이체 8. 교통/자동차 9. 술/유흥 10. 생활 11. 의료/건강/피트니스 
12. 편의점/마트/잡화 13. 주거/통신 14. 교육 15. 미용 16. 카테고리 없음

[분석 요구사항]
1) 전체 지출 집계 및 16개 카테고리별 분석
2) 소비 패턴과 트렌드 분석 (시간대, 요일별 특성 고려)
3) 위험 패턴 및 과소비 영역 식별
4) 3단계 레벨별 맞춤 절약 제안

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
  "spending_type": "소비 패턴 요약 (예: 외식·배달 중심, 주말 지출 집중)",
  "risk_patterns": ["위험 패턴 목록"],
  "overspending_categories": ["과소비 카테고리 목록"],
  "spending_feedback": {
    "spending_tips": ["실용적인 지출 관리 팁 목록"],
    "goal_progress": "목표 달성 속도 및 진행 상황 평가",
    "positive_changes": ["이전 달 대비 잘한 점 칭찬 목록"],
    "improvement_guide": ["소비 습관 개선을 위한 구체적 가이드"]
  },
  "monthly_comparison": {
    "all_categories": [
      {"category": "카테고리명", "current_amount": 0, "previous_amount": 0, "change_amount": 0, "change_rate": 0.0}
    ]
  },
  "saving_suggestions": {
    "강한절약": {
      "level": "🔥 강한 절약",
      "description": "고정비를 포함한 전면적 지출 절약",
      "expected_saving": 0,
      "reduction_rate": "25-40%",
      "strategies": [
        {
          "category": "카테고리명",
          "current_amount": 0,
          "target_amount": 0,
          "saving_amount": 0,
          "method": "구체적인 절약 방법",
          "difficulty": "상|중|하"
        }
      ]
    },
    "보통절약": {
      "level": "💪 보통 절약",
      "description": "주요 지출 카테고리 중심 절약",
      "expected_saving": 0,
      "reduction_rate": "15-25%",
      "strategies": [
        {
          "category": "카테고리명",
          "current_amount": 0,
          "target_amount": 0,
          "saving_amount": 0,
          "method": "구체적인 절약 방법",
          "difficulty": "상|중|하"
        }
      ]
    },
    "약한절약": {
      "level": "🌱 약한 절약",
      "description": "빈번하고 불필요한 소비 점진적 절약",
      "expected_saving": 0,
      "reduction_rate": "5-15%",
      "strategies": [
        {
          "category": "카테고리명",
          "current_amount": 0,
          "target_amount": 0,
          "saving_amount": 0,
          "method": "구체적인 절약 방법",
          "difficulty": "상|중|하"
        }
      ]
    }
  }
}

[절약 제안 가이드라인]
강한절약 (25-40% 절약):
- 고정비(주거/통신, 보험/세금/기타금융) 포함 전면적 절약
- 구조적 변화 요구 (요금제 변경, 구독 해지, 생활패턴 변경 등)
- 높은 절약 효과, 높은 실행 난이도

보통절약 (15-25% 절약):
- 주요 변동비 카테고리(식비, 쇼핑, 카페/간식) 중심 절약
- 습관 개선 중심 (빈도 줄이기, 대안 찾기 등)
- 중간 절약 효과, 중간 실행 난이도

약한절약 (5-15% 절약):
- 빈번하고 소액인 불필요 소비(카페/간식, 편의점, 생활) 중심
- 점진적 변화 (할인 활용, 일부 줄이기 등)
- 낮은 절약 효과, 낮은 실행 난이도

[카테고리별 절약 우선순위]
높음: 식비, 쇼핑, 카페/간식, 취미/여가, 술/유흥
중간: 편의점/마트/잡화, 주거/통신, 교통/자동차, 생활, 미용
낮음: 여행/숙박, 의료/건강/피트니스, 교육, 보험/세금/기타금융
제외: 이체, 카테고리 없음

[소비습관 피드백 가이드라인]
spending_tips:
- 현재 소비 패턴에 맞는 실용적 관리 방법 제시
- "가계부 앱 활용", "예산 한도 설정", "할인 혜택 활용" 등 구체적 팁
- 3-5개의 실행 가능한 조언

goal_progress:
- 절약 목표 대비 현재 진행 상황 평가
- "목표 달성까지 XX개월", "현재 XX% 달성" 등 구체적 수치
- 격려와 동기부여 포함

positive_changes:
- 이전 달 대비 개선된 소비 습관 칭찬
- "XX 카테고리 XX원 절약", "새벽 소비 XX% 감소" 등
- 2-3개의 긍정적 변화 강조

improvement_guide:
- 단계별 소비 습관 개선 방법 제시
- "1단계: XX, 2단계: XX" 형태로 구조화
- 3-4개의 점진적 개선 방안

[월간 비교 분석 가이드라인]
all_categories:
- 현재 달에 지출이 있는 모든 카테고리를 포함 (금액이 0인 카테고리 제외)
- 이전 달 데이터가 있는 경우: 실제 증감 금액과 증감율(%) 정확히 계산
- 이전 달 데이터가 없는 경우: previous_amount=0, change_amount=current_amount, change_rate=100.0으로 설정
- change_rate 기준 오름차순 정렬 (가장 감소한 카테고리부터 가장 증가한 카테고리 순)
- 최소 3개 이상의 카테고리 포함 (지출이 있는 모든 카테고리)
- 증감 구분 없이 전체 지출 변동 패턴을 한눈에 파악 가능하도록 구성

[분석 기준]
- category_breakdown: 'keyword_hints'와 'amount_hints'를 종합하여 16개 카테고리별 금액과 비율 계산
- spending_type: 'weekday_type', 'time_bucket' 정보를 활용한 소비 특성 요약
- risk_patterns: 새벽 시간대 소비, 고액 결제, 반복적 소비 패턴 등 식별
- overspending_categories: 평균 대비 과도한 지출 카테고리
- spending_feedback: 개인화된 소비습관 피드백 제공
  * spending_tips: 현재 소비 패턴에 맞는 실용적 관리 팁 (3-5개)
  * goal_progress: 절약 목표 달성도 및 속도 평가
  * positive_changes: 이전 달 대비 개선된 점 격려 (2-3개)
  * improvement_guide: 단계별 소비 습관 개선 방법 (3-4개)
- monthly_comparison: 이전 달 대비 지출 변동 분석
  * all_categories: 지출이 있는 전체 카테고리의 증감 정보를 change_rate 기준 오름차순 정렬
    - 현재 달 지출이 있는 모든 카테고리 포함 (amount > 0)
    - 이전 달 데이터가 없으면 previous_amount=0, change_rate=100.0으로 설정
    - 최소 3개 이상 카테고리 포함하여 전체 지출 패턴 분석 가능
- saving_suggestions: 각 레벨별로 실제 금액과 구체적인 방법을 포함한 맞춤 절약 전략

[주의사항]
- 반드시 유효한 JSON만 출력
- 16개 카테고리 중 해당하는 카테고리만 분석
- 금액은 정수로 반올림
- 비율은 소수점 첫째 자리까지
- 각 절약 레벨별로 현실적이고 실행 가능한 제안 작성
- 절약 금액 계산 시 현재 지출 패턴과 빈도를 고려
- 데이터가 부족한 경우 보수적으로 분석
- 이체, 보험/세금/기타금융은 절약 제안에서 제외
- spending_feedback은 긍정적이고 격려하는 톤으로 작성
- monthly_comparison의 all_categories는 현재 달 지출이 있는 모든 카테고리 필수 포함
  * 이전 달 데이터가 없는 경우에도 current_amount > 0인 모든 카테고리 포함
  * 카테고리 개수가 적어도 전체 지출 패턴 파악을 위해 모든 지출 카테고리 표시
- 모든 피드백과 가이드는 구체적이고 실행 가능한 내용으로 작성
"""

# 절약 제안 계산 헬퍼 함수들
def calculate_saving_amount(category, current_amount, level, transaction_count=1):
    """
    카테고리별 절약 금액 계산
    """
    rules = SAVING_CALCULATION_RULES[level]
    
    # 기본 절약률 적용
    base_reduction = rules["min_target_reduction"]
    max_reduction = rules["max_target_reduction"]
    
    # 카테고리별 가중치 적용
    if category in ["구독서비스", "주거/통신"] and level == "강한절약":
        reduction_rate = max_reduction  # 고정비는 강한절약에서 최대 절약
    elif category in ["배달음식", "카페/간식"] and transaction_count > 10:
        reduction_rate = (base_reduction + max_reduction) / 2  # 빈번한 소비는 중간 절약률
    else:
        reduction_rate = base_reduction
    
    return int(current_amount * reduction_rate)

def get_difficulty_level(category, level, current_amount):
    """
    절약 난이도 계산
    """
    # 고정비는 구조적 변경이 필요하므로 난이도 높음
    if category in ["구독서비스", "주거/통신"]:
        if level == "강한절약":
            return "상"
        else:
            return "중"
    
    # 높은 금액 카테고리는 절약 난이도 높음
    if current_amount > 100000:
        return "상" if level == "강한절약" else "중"
    
    # 일반적인 경우
    difficulty_map = {
        "강한절약": "중",
        "보통절약": "중", 
        "약한절약": "하"
    }
    return difficulty_map[level]

def generate_saving_method(category, level, current_amount, transaction_count):
    """
    카테고리와 레벨에 맞는 절약 방법 생성
    """
    if category not in SAVING_STRATEGIES:
        return f"{level} 수준에서 {category} 지출을 줄여 절약하세요"
    
    strategy_template = SAVING_STRATEGIES[category][level]
    
    # 템플릿에 필요한 값들 계산
    values = {}
    
    # 절약 금액 계산
    saving_amount = calculate_saving_amount(category, current_amount, level, transaction_count)
    values["amount"] = saving_amount
    
    if "{current_count}" in strategy_template:
        values["current_count"] = max(1, transaction_count // 4)  # 주간 평균
    
    if "{target_count}" in strategy_template:
        reduction_rate = SAVING_CALCULATION_RULES[level]["min_target_reduction"]
        values["target_count"] = max(1, int(values.get("current_count", 1) * (1 - reduction_rate)))
    
    if "{reduce_count}" in strategy_template:
        values["reduce_count"] = max(1, values.get("current_count", 1) - values.get("target_count", 1))
    
    if "{unused_count}" in strategy_template:
        values["unused_count"] = min(3, max(1, transaction_count // 10))
    
    if "{downgrade_count}" in strategy_template:
        values["downgrade_count"] = min(2, max(1, transaction_count // 15))
    
    if "{budget}" in strategy_template:
        values["budget"] = int(current_amount * 0.7)  # 30% 예산 감축
    
    try:
        return strategy_template.format(**values)
    except KeyError as e:
        # 누락된 키가 있는 경우 기본 메시지 반환
        return f"{category}에서 월 {saving_amount:,}원 절약 가능"

# 카테고리별 우선순위 점수 (높을수록 절약 효과 큼) - 16개 카테고리
CATEGORY_PRIORITY_SCORES = {
    "식비": 10,                    # 가장 높은 절약 효과
    "쇼핑": 9,
    "카페/간식": 8,
    "취미/여가": 8,
    "술/유흥": 7,
    "편의점/마트/잡화": 6,
    "주거/통신": 5,               # 고정비이지만 절약 가능
    "교통/자동차": 5,
    "생활": 4,
    "미용": 4,
    "여행/숙박": 3,
    "의료/건강/피트니스": 2,      # 필수적이지만 일부 절약 가능
    "교육": 2,
    "보험/세금/기타금융": 1,      # 필수 고정비
    "이체": 0,                    # 절약 대상 아님
    "카테고리 없음": 0            # 분류되지 않은 항목
}
