from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from board_crawler.board_crawler_router import board_crawler_router
from news_crawler.crawler_test import news_crawler_router
from save_ticker.save_ticker_router import save_ticker_router
from stock_response.stock_router import stock_response_router

app = FastAPI()

origins = [
    "http://localhost:8080",
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


app.include_router(board_crawler_router)
app.include_router(stock_response_router)
app.include_router(save_ticker_router)
app.include_router(news_crawler_router)
