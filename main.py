# main.py
from fastapi import FastAPI

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# 루트 경로 ("/")에 대한 GET 요청 핸들러
@app.get("/")
def read_root():
    return {"Hello": "World"}

# "/items/{item_id}" 경로에 대한 GET 요청 핸들러
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}