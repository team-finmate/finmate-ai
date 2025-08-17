from pydantic import BaseModel

# Pydantic 모델 정의
# API 요청 본문의 JSON 데이터 구조를 정의합니다.
class Transaction(BaseModel):
    transaction_id: str
    date: str
    time: str
    merchant: str
    category: str
    amount: int
    payment_method: str
    balance: int