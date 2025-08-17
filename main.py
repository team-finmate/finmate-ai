
# main.py
from fastapi import FastAPI
from routers import transactions

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="FinMate AI",
    description="결제 내역 분석 API",
    version="1.0.0"
)

# 라우터 연결
app.include_router(transactions.router)

# 루트 경로 ("/")에 대한 GET 요청 핸들러
@app.get("/")
def read_root():
    return {"Hello": "World", "message": "FinMate AI API"}

# "/items/{item_id}" 경로에 대한 GET 요청 핸들러
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}