# API 엔드포인트 세분화 설계

## 현재 문제점
- `/analyze` 엔드포인트가 너무 많은 기능을 담당
- 단일 책임 원칙(SRP) 위배
- 응답 데이터가 너무 크고 복잡
- 클라이언트에서 필요한 부분만 요청하기 어려움

## 제안하는 세분화 구조

### 1. 기본 분석 엔드포인트
**`POST /transactions/analysis/basic`**
- 총 지출액, 카테고리별 분석, 평균 거래액
- 지출 트렌드, 상위 지출 내역
- 소비 패턴 타입, 위험 패턴 감지

### 2. 월간 비교 분석 엔드포인트  
**`POST /transactions/analysis/monthly-comparison`**
- 이전 달 대비 카테고리별 증감 분석
- 변동률 기준 정렬된 전체 카테고리 비교
- 월간 변화 트렌드 분석

### 3. 절약 제안 엔드포인트 (목표 분석 포함)
**`POST /transactions/suggestions/saving`**
- 3단계 레벨별 절약 전략 제안
- 카테고리별 구체적 절약 방법
- 예상 절약 금액 계산
- **NEW**: 사용자 목표 달성 가능성 분석
- **NEW**: 목표별 권장 절약 수준 제안

### 4. 소비습관 피드백 엔드포인트
**`POST /transactions/feedback/habits`**
- 개인화된 소비 관리 팁
- 목표 달성 진행률 평가
- 긍정적 변화 칭찬 및 개선 가이드

### 5. 종합 분석 엔드포인트 (기존 유지)
**`POST /transactions/analyze`**
- 모든 분석 결과를 한 번에 제공 (기존과 동일)
- 레거시 지원 및 전체 분석이 필요한 경우

## 장점
1. **단일 책임**: 각 엔드포인트가 명확한 목적 가짐
2. **성능 최적화**: 필요한 분석만 요청 가능
3. **유지보수성**: 기능별 독립적 수정/테스트 가능
4. **확장성**: 새로운 분석 기능 추가 용이
5. **캐싱**: 각 분석 결과를 독립적으로 캐싱 가능

## 구현 방식
- 공통 로직은 서비스 계층에서 분리
- 각 엔드포인트는 해당 분석만 수행
- 응답 스키마도 기능별로 세분화
- **NEW**: 목표 달성 분석 서비스 추가
- **NEW**: 데이터베이스 연동을 위한 Goal 스키마 정의

## 목표 달성 분석 기능
### 데이터베이스 스키마
```sql
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    type VARCHAR(20) NOT NULL, -- TRAVEL, HOUSE, MARRIAGE, CAR, EMERGENCY, EDUCATION, CUSTOM
    name VARCHAR(100) NOT NULL, -- 자동생성 이름
    custom_name VARCHAR(100), -- CUSTOM일 때만 사용
    target_amount DECIMAL(15,2) NOT NULL,
    current_amount DECIMAL(15,2) DEFAULT 0,
    target_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE', -- ACTIVE, COMPLETED, PAUSED, CANCELLED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL
);
```

### 분석 기능
1. **달성 가능성 계산**: 현재 절약 수준으로 목표 달성 가능한지 분석
2. **권장 절약 수준**: 목표 달성을 위한 최적 절약 레벨 제안
3. **확률 계산**: 절약 수준과 기간을 고려한 달성 확률 (0-100%)
4. **부족/여유 금액**: 월간 필요 금액 대비 절약 가능 금액 비교
5. **우선순위 정렬**: 목표 유형별 중요도에 따른 정렬

### API 요청/응답 예시
```json
// 요청
{
  "transactions": [...],
  "goals": [
    {
      "type": "TRAVEL",
      "name": "제주도 여행", 
      "target_amount": 2000000,
      "current_amount": 500000,
      "target_date": "2024-12-31"
    }
  ],
  "current_monthly_surplus": 200000
}

// 응답
{
  "saving_suggestions": {...},
  "saving_summary": {...},
  "goal_achievement_analysis": [
    {
      "goal_name": "제주도 여행",
      "is_achievable": true,
      "achievement_probability": 85.0,
      "recommended_saving_level": "보통절약",
      "required_monthly_saving": 250000,
      "shortfall_amount": -50000,
      "analysis_message": "보통절약으로 월 100만원 절약하면 목표 달성 가능합니다."
    }
  ]
}
```
