from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.article.news_crawler.crawler_test import news_crawler_router
from app.opinion_mining.opinion_mining_router import opinion_mining_router
from app.stock.save_ticker.save_ticker_router import save_ticker_router
from app.stock.stock_OHCL_response.stock_router import stock_response_router
from app.stock.stock_data_reponse.get_stock_data_router import get_stock_data_router

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:7777"
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


app.include_router(get_stock_data_router)
app.include_router(opinion_mining_router)
app.include_router(stock_response_router)
app.include_router(save_ticker_router)
app.include_router(news_crawler_router)
