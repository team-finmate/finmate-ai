# 💰 FinMate AI

> **개인 결제내역 분석과 맞춤형 절약 제안을 제공하는 AI 기반 금융 분석 서비스**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)

---

## 🎯 프로젝트 개요

FinMate AI는 개인의 결제내역을 **16개 카테고리**로 분석하고, **3단계 맞춤형 절약 제안**을 제공하는 스마트 금융 분석 도구입니다. 사용자는 자신의 상황에 맞는 절약 수준을 선택하여 체계적으로 지출을 관리할 수 있습니다.

### 🌟 핵심 가치
- **개인화된 분석**: 16개 세분화된 카테고리별 소비 패턴 분석
- **선택의 자유**: 3단계 절약 레벨로 사용자 맞춤 제안
- **실용성**: 구체적인 금액과 실행 방법 제시
- **지능형 AI**: OpenAI GPT-4 기반 고도화된 분석

---

## ✨ 주요 기능

### 📊 **스마트 소비 패턴 분석**

| 분석 항목 | 세부 내용 |
|---------|-----------|
| **16개 카테고리 분석** | 식비, 쇼핑, 카페/간식, 주거/통신 등 상세 분류 |
| **시간대별 패턴** | 평일/주말, 시간대별 소비 특성 분석 |
| **위험 패턴 감지** | 새벽 소비, 고액 결제, 반복 소비 등 |
| **트렌드 분석** | 상승/하락/안정 트렌드 및 예측 |
| **🆕 소비습관 피드백** | 개인화된 지출 팁, 목표 달성도, 개선 가이드 |
| **🆕 월간 비교 분석** | 이전 달 대비 증가/감소 상위 카테고리 |

### 🏦 **금융상품 추천 시스템** 🆕

사용자의 소비 패턴과 재정 상황을 분석하여 **정기예금**과 **적금** 상품을 추천합니다.

| 추천 기능 | 세부 내용 |
|---------|-----------|
| **맞춤형 상품 추천** | 위험 성향, 절약 능력, 투자 목표 기반 추천 |
| **수익률 계산** | 실제 예상 이자 및 수익률 제공 |
| **포트폴리오 제안** | 정기예금/적금 최적 비율 제안 |
| **AI 기반 분석** | OpenAI 활용한 개인화된 투자 전략 |

#### 🎯 **추천 알고리즘**
- **위험 성향 분석**: 소비 패턴 기반 안전/보통/적극 성향 분류
- **절약 능력 평가**: 3단계 절약 제안에서 도출된 가용 자금 계산
- **상품 점수화**: 금리, 접근성, 우대 조건 등 종합 평가
- **맞춤 추천**: 개인 상황에 최적화된 상위 3개 상품 선별

### 💡 **3단계 절약 제안 시스템**

사용자가 자신의 상황에 맞게 **선택할 수 있는** 3가지 절약 레벨을 제공합니다.

<table>
<tr>
<th width="25%">🔥 강한 절약</th>
<th width="25%">💪 보통 절약</th>
<th width="25%">🌱 약한 절약</th>
<th width="25%">비교</th>
</tr>
<tr>
<td>

**절약률**: 25-40%<br>
**대상**: 고정비 포함<br>
**특징**: 구조적 변화<br>
**난이도**: 상<br>
**효과**: 높음

</td>
<td>

**절약률**: 15-25%<br>
**대상**: 주요 변동비<br>
**특징**: 습관 개선<br>
**난이도**: 중<br>
**효과**: 중간

</td>
<td>

**절약률**: 5-15%<br>
**대상**: 소액 빈번 소비<br>
**특징**: 점진적 변화<br>
**난이도**: 하<br>
**효과**: 낮음

</td>
<td>

📈 **월 100만원 지출 기준**<br>
🔥 **25-40만원 절약**<br>
💪 **15-25만원 절약**<br>
🌱 **5-15만원 절약**

</td>
</tr>
</table>

### 🎯 **절약 제안의 특별함**

| 특징 | 설명 | 예시 |
|-----|------|------|
| **구체적 금액** | 정확한 절약 예상 금액 제시 | "월 81,250원 절약" |
| **실행 방법** | 구체적이고 실현 가능한 방법 | "배달음식을 주 4회→3회로 줄이고 직접 요리" |
| **난이도 표시** | 각 전략의 실행 난이도 | 상/중/하 |
| **우선순위** | 절약 효과가 큰 카테고리부터 | 식비(10점) > 쇼핑(9점) > 카페(8점) |

### 🆕 **개인화된 소비습관 피드백**

FinMate AI는 단순한 분석을 넘어 **개인화된 피드백**을 제공합니다:

#### 📝 **지출 관리 팁**
- 현재 소비 패턴에 맞는 실용적 관리 방법
- 가계부 앱 활용, 예산 한도 설정 등 구체적 조언
- 3-5개의 실행 가능한 팁 제공

#### 📊 **목표 달성 진행상황**
- 절약 목표 대비 현재 진행 상황 평가
- "목표 달성까지 X개월", "현재 X% 달성" 등 구체적 수치
- 격려와 동기부여 메시지 포함

#### 👏 **긍정적 변화 칭찬**
- 이전 달 대비 개선된 소비 습관 인정
- "XX 카테고리 XX원 절약", "새벽 소비 XX% 감소" 등
- 2-3개의 긍정적 변화 강조

#### 📈 **단계별 개선 가이드**
- 점진적이고 실현 가능한 개선 방법 제시
- "1단계: XX, 2단계: XX" 형태로 구조화
- 3-4개의 체계적 개선 방안

### 📊 **월간 비교 분석**

이전 달과 비교하여 **지출 변동을 한눈에** 파악할 수 있습니다:

#### 📈 **증가 카테고리 (상위 2개)**
- 이전 달 대비 지출이 증가한 카테고리
- 증가 금액과 증가율(%) 정확히 표시
- 증가 원인 분석 및 주의 메시지

#### 📉 **감소 카테고리 (상위 2개)**
- 이전 달 대비 지출이 감소한 카테고리
- 감소 금액과 감소율(%) 정확히 표시
- 절약 성과 칭찬 및 격려 메시지

---

## 🏗️ 시스템 아키텍처

```mermaid
graph TB
    A[결제내역 입력] --> B[데이터 전처리]
    B --> C[16개 카테고리 분류]
    C --> D[OpenAI 분석]
    D --> E[패턴 분석]
    E --> F[3단계 절약 제안]
    F --> G[사용자 선택]
    G --> H[맞춤 절약 계획]
```

### 📁 **프로젝트 구조**

```
finmate-ai/
├── 📁 core/
│   └── config.py              # 16개 카테고리 & 절약 규칙 설정
├── 📁 services/
│   ├── data_processor.py      # 거래 데이터 전처리 & 카테고리 분류
│   ├── openai_service.py      # OpenAI GPT-4 연동 & 분석
│   ├── saving_service.py      # 3단계 절약 제안 생성 엔진
│   ├── product_recommendation_service.py  # 🆕 금융상품 추천 엔진
│   └── ai_product_service.py  # 🆕 AI 기반 상품 추천
├── 📁 routers/
│   ├── transactions.py        # 소비 분석 API 엔드포인트
│   └── products.py           # 🆕 금융상품 추천 API
├── 📁 schemas/
│   ├── transactions.py        # 소비 분석 데이터 모델
│   └── products.py           # 🆕 금융상품 데이터 모델
├── 📁 data/
│   ├── time_deposits.json     # 🆕 정기예금 상품 데이터
│   └── saving_products.json  # 🆕 적금 상품 데이터
├── 🔧 main.py                 # FastAPI 앱 실행
├── 📋 requirements.txt        # 의존성 패키지
└── 📖 README.md              # 프로젝트 문서
```

---

## 🚀 빠른 시작하기

### 1️⃣ **환경 준비**

```bash
# 1. 저장소 클론
git clone https://github.com/team-finmate/finmate-ai.git
cd finmate-ai

# 2. 가상환경 생성
python -m venv venv

# 3. 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 4. 패키지 설치
pip install -r requirements.txt
```

### 2️⃣ **환경변수 설정**

`.env` 파일을 생성하고 OpenAI API 키를 설정합니다:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3️⃣ **서버 실행**

```bash
uvicorn main:app --reload
```

서버가 실행되면 `http://localhost:8000`에서 API를 사용할 수 있습니다.

### 4️⃣ **API 문서 확인**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API 사용법

### **분석 요청**

```http
POST /transactions/analyze/
Content-Type: application/json

[
  {
    "transaction_id": "txn_001",
    "date": "2024-01-15",
    "time": "12:30",
    "merchant": "스타벅스 강남점",
    "category": "카페/간식",
    "amount": 5500,
    "payment_method": "카드",
    "balance": 1500000
  }
]
```

### **응답 예시**

<details>
<summary>📋 <strong>전체 응답 보기</strong></summary>

```json
{
  "total_spent": 900000,
  "category_breakdown": {
    "식비": {
      "amount": 320000,
      "ratio": 0.32,
      "transaction_count": 20,
      "avg_amount": 16000
    },
    "카페/간식": {
      "amount": 150000,
      "ratio": 0.15,
      "transaction_count": 30,
      "avg_amount": 5000
    }
  },
  "spending_trend": "상승",
  "avg_transaction": 12500,
  "top_expenses": [
    {
      "merchant": "배달의민족",
      "amount": 25000,
      "category": "식비"
    }
  ],
  "spending_type": "외식·배달 중심, 주말 지출 집중",
  "risk_patterns": ["새벽 시간대 소비", "고액 단건 결제"],
  "overspending_categories": ["식비", "카페/간식"],
  "spending_feedback": {
    "spending_tips": [
      "가계부 앱을 활용하여 일일 지출 한도를 설정해보세요",
      "배달음식 주문 전 10분 대기 시간을 두어 충동구매를 방지하세요"
    ],
    "goal_progress": "현재 월 90만원 지출로 목표 대비 10% 초과, 절약 목표 달성까지 2개월 예상",
    "positive_changes": [
      "이전 달 대비 편의점 지출 15% 감소로 월 25,000원 절약 성공",
      "새벽 시간대 소비가 30% 줄어 충동구매 패턴 개선"
    ],
    "improvement_guide": [
      "1단계: 주 3회 배달음식을 2회로 줄이기 (월 5만원 절약)",
      "2단계: 카페 방문을 홈카페로 대체하기 (월 3만원 절약)"
    ]
  },
  "monthly_comparison": {
    "increased_categories": [
      {
        "category": "식비",
        "current_amount": 320000,
        "previous_amount": 280000,
        "change_amount": 40000,
        "change_rate": 14.3
      }
    ],
    "decreased_categories": [
      {
        "category": "교통/자동차",
        "current_amount": 60000,
        "previous_amount": 80000,
        "change_amount": -20000,
        "change_rate": -25.0
      }
    ]
  },
  "saving_suggestions": {
    "강한절약": {
      "level": "🔥 강한 절약",
      "description": "고정비를 포함한 전면적 지출 절약",
      "expected_saving": 225000,
      "reduction_rate": "25-40%",
      "strategies": [
        {
          "category": "식비",
          "current_amount": 320000,
          "target_amount": 240000,
          "saving_amount": 80000,
          "method": "외식/배달을 주 5회에서 3회로 줄이고 직접 요리로 월 80,000원 절약",
          "difficulty": "상"
        }
      ]
    },
    "보통절약": {
      "level": "💪 보통 절약",
      "description": "주요 지출 카테고리 중심 절약",
      "expected_saving": 135000,
      "reduction_rate": "15-25%",
      "strategies": [
        {
          "category": "식비",
          "current_amount": 320000,
          "target_amount": 272000,
          "saving_amount": 48000,
          "method": "외식/배달 주문을 주 1회 줄여서 월 48,000원 절약",
          "difficulty": "중"
        }
      ]
    },
    "약한절약": {
      "level": "🌱 약한 절약",
      "description": "빈번하고 불필요한 소비 점진적 절약",
      "expected_saving": 47000,
      "reduction_rate": "5-15%",
      "strategies": [
        {
          "category": "카페/간식",
          "current_amount": 150000,
          "target_amount": 135000,
          "saving_amount": 15000,
          "method": "간식 구매를 주 1회 줄여서 월 15,000원 절약",
          "difficulty": "하"
        }
      ]
    }
  }
}
```

</details>

---

## 🏦 금융상품 추천 API 🆕

사용자의 소비 분석 결과를 바탕으로 정기예금과 적금 상품을 추천합니다.

### **요청 방법**

```bash
curl -X POST "http://localhost:8000/recommend-products" \
     -H "Content-Type: application/json" \
     -d '{
       "total_spent": 2500000,
       "category_breakdown": {...},
       "saving_suggestions": {...},
       "monthly_income": 4000000,
       "current_savings": 10000000,
       "investment_period_preference": "중기",
       "risk_preference": "보통",
       "financial_goals": ["비상자금", "내집마련"]
     }'
```

### **응답 예시**

<details>
<summary>🏦 <strong>금융상품 추천 응답 보기</strong></summary>

```json
{
  "user_profile_analysis": "사용자의 월 지출액은 2,500,000원이며, 수입 대비 62.5% 지출하는 보통 성향의 투자자입니다. 절약 가능 금액은 약 750,000원으로 분석되며, 비상자금, 내집마련 등의 목표를 위한 금융상품 가입을 권장합니다.",
  "recommended_time_deposits": [
    {
      "product": {
        "금융회사": "동양저축은행",
        "상품명": "정기예금(비대면)",
        "기간개월": 12,
        "세전우대합계_num": 0.0652,
        "최소가입금액": 100000,
        "권장예치금액": 50000000
      },
      "recommendation_score": 73.1,
      "recommended_amount": 10000000,
      "expected_interest": 652000,
      "reasons": [
        {
          "reason_title": "높은 금리 혜택",
          "reason_detail": "최대 연 6.52%의 우대금리로 높은 수익 기대",
          "benefit_description": "시중 평균보다 높은 금리로 안정적인 수익 창출 가능"
        }
      ],
      "fit_analysis": "균형 잡힌 투자 성향에 적합한 상품으로, 안정성과 수익성을 모두 고려한 선택입니다."
    }
  ],
  "recommended_savings": [
    {
      "product": {
        "금융회사": "KB국민은행",
        "상품명": "KB Star 적금",
        "기간개월": 24,
        "세전우대합계_num": 0.072,
        "최소납입금액": 50000,
        "권장월납입금액": 500000
      },
      "recommendation_score": 75.8,
      "recommended_monthly_amount": 62500,
      "expected_total_amount": 1554000,
      "expected_interest": 54000,
      "reasons": [
        {
          "reason_title": "높은 금리 혜택",
          "reason_detail": "최대 연 7.20%의 우대금리로 높은 수익 기대",
          "benefit_description": "시중 평균보다 높은 금리로 안정적인 수익 창출 가능"
        }
      ],
      "fit_analysis": "월 62,500원 수준의 적립 계획에 적합한 24개월 적금으로, 목돈 마련에 효과적입니다."
    }
  ],
  "portfolio_suggestion": "균형 포트폴리오: 정기예금과 적금을 50:50으로 구성하여 안정성과 수익성을 균형있게 추구하시기 바랍니다.",
  "total_expected_benefit": 706000,
  "investment_strategy": "현재 지출 패턴을 기반으로 한 분석 결과, 보통 성향에 맞는 상품 조합으로 연 평균 수익률 7.06%를 기대할 수 있습니다.",
  "cautions": [
    "금리는 시장 상황에 따라 변동될 수 있습니다.",
    "우대 조건을 충족하지 못할 경우 기본 금리가 적용됩니다."
  ]
}
```

</details>

### **추가 API 엔드포인트**

| 엔드포인트 | 메소드 | 설명 |
|-----------|--------|------|
| `/products/time-deposits` | GET | 모든 정기예금 상품 목록 조회 |
| `/products/savings` | GET | 모든 적금 상품 목록 조회 |
| `/ai-recommend` | POST | AI 전용 상품 추천 (OpenAI 기반) |

---

## 📊 16개 지원 카테고리

<div align="center">

| 순위 | 카테고리 | 절약 우선순위 | 주요 키워드 |
|:---:|---------|:----------:|-----------|
| 🥇 | **식비** | ⭐⭐⭐⭐⭐ | 배달의민족, 맥도날드, 김밥천국 |
| 🥈 | **쇼핑** | ⭐⭐⭐⭐⭐ | 쿠팡, 11번가, 무신사 |
| 🥉 | **카페/간식** | ⭐⭐⭐⭐ | 스타벅스, 이디야, 베이커리 |
| 4 | **취미/여가** | ⭐⭐⭐⭐ | CGV, PC방, 노래방 |
| 5 | **술/유흥** | ⭐⭐⭐ | 소주, 클럽, 치킨 |
| 6 | **편의점/마트/잡화** | ⭐⭐⭐ | CU, 이마트, 다이소 |
| 7 | **주거/통신** | ⭐⭐ | 넷플릭스, SK텔레콤, 전기료 |
| 8 | **교통/자동차** | ⭐⭐ | 카카오택시, 주유, 지하철 |
| 9 | **생활** | ⭐⭐ | 세탁소, 택배, 은행 |
| 10 | **미용** | ⭐⭐ | 미용실, 네일, 화장품 |
| 11 | **여행/숙박** | ⭐ | 항공, 호텔, 에어비앤비 |
| 12 | **의료/건강/피트니스** | ⭐ | 병원, 헬스장, 요가 |
| 13 | **교육** | ⭐ | 학원, 온라인강의, 세미나 |
| 14 | **보험/세금/기타금융** | ➖ | 보험, 국민연금, 증권 |
| 15 | **이체** | ➖ | 송금, 계좌이체, ATM |
| 16 | **카테고리 없음** | ➖ | 분류되지 않은 항목 |

</div>

> **⭐ 우선순위 설명**: 높을수록 절약 효과가 크며, ➖ 표시는 절약 제안에서 제외되는 카테고리입니다.

---

## 🧪 테스트 실행

프로젝트에는 다양한 테스트 파일이 포함되어 있습니다:

```bash
# 16개 카테고리 절약 제안 테스트
python test_16_categories.py

# 통합 시스템 테스트
python test_saving_integration.py
```

---

## 🤝 기여하기

1. 이 저장소를 Fork 합니다
2. 새로운 브랜치를 만듭니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 Push 합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

---

## 📞 지원 및 문의

- **Issues**: [GitHub Issues](https://github.com/team-finmate/finmate-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/team-finmate/finmate-ai/discussions)
- **Email**: [team-finmate@example.com](mailto:team-finmate@example.com)

---

## 📄 라이선스

이 프로젝트는 **MIT 라이선스**를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

<div align="center">

**💰 FinMate AI로 스마트한 가계부 관리를 시작하세요! 💰**

[![Star](https://img.shields.io/github/stars/team-finmate/finmate-ai?style=social)](https://github.com/team-finmate/finmate-ai)
[![Fork](https://img.shields.io/github/forks/team-finmate/finmate-ai?style=social)](https://github.com/team-finmate/finmate-ai)
[![Watch](https://img.shields.io/github/watchers/team-finmate/finmate-ai?style=social)](https://github.com/team-finmate/finmate-ai)

</div>