from pykrx import stock
from datetime import datetime, timedelta
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class MarketTicker(BaseModel):
    ticker: int

today = datetime.today().strftime("%Y%m%d")
yesterday = datetime.today() - timedelta(1)
yesterday = yesterday.strftime("%Y%m%d")

ticker_list = stock.get_market_ticker_list(date=today, market="KOSPI")
symbol_list = []

for ticker in ticker_list:
    symbol = stock.get_market_ticker_name(ticker)
    symbol_list.append(symbol)

df = stock.get_market_price_change_by_ticker(yesterday, today)
# print(df.head(10))
@app.get("/market_ticker")
async def get_market_ticker():
    return df.head(10)



# class MarketTicker(BaseModel):
#     ticker: int
#     change: float
#
#
# @app.get("/market_ticker")
# async def get_market_ticker():
#     today = datetime.today().strftime("%Y%m%d")
#     yesterday = datetime.today() - timedelta(1)
#     yesterday = yesterday.strftime("%Y%m%d")
#     ticker_list = stock.get_market_ticker_list(date=today, market="KOSPI")
#     price_changes = stock.get_market_price_change_by_ticker(yesterday, today)
#
#     market_ticker_list = []
#
#     # for ticker in ticker_list:
#     #     name = stock.get_market_ticker_name(ticker)
#     #     price_change = float(price_changes.loc[ticker]["등락률"])
#     #     market_ticker_list.append(MarketTicker(ticker=ticker, change=price_change))
#
#     return price_changes
