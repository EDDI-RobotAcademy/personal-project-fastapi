from fastapi import APIRouter
from pykrx import stock
from datetime import datetime

save_ticker_router = APIRouter()
@save_ticker_router.get("/stock/save-data")
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
    return response_data