from fastapi import FastAPI
from pykrx import stock
from datetime import datetime, timedelta
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/stock/save-data")
async def save_stock_ticker_name_to_spring():
    class MarketTicker():
        today = datetime.today().strftime("%Y%m%d")
        ticker = stock.get_market_ticker_list(date=today, market="KOSPI")
        stockName = []

        for i in ticker:
            symbol = stock.get_market_ticker_name(i)
            stockName.append(symbol)

    response_data = {
        "ticker": MarketTicker.ticker,
        "stockName": MarketTicker.stockName
    }
    print(response_data)
    return response_data



# print(df.head(10))
# @app.get("/market_ticker")
# async def get_market_ticker():
#     return df.head(10)



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
