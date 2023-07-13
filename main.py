from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from save_ticker.save_ticker_router import save_ticker_router
from stock_test.stock_test_router import stock_test_router

app = FastAPI()

origins = [
    "http://localhost:8080",  # 허용하려는 프론트엔드 도메인 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(stock_test_router)
app.include_router(save_ticker_router)

