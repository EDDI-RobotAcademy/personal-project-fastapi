from fastapi import APIRouter
import yfinance as yf
import asyncio

stock_response_router = APIRouter()

def fetch_yfinance_data(ticker, interval, period):
    result = yf.download(ticker, interval=interval, period=period)

    minute_data = []
    for index, row in result.iterrows():
        date = index.strftime('%Y-%m-%d %H:%M')
        open_value = row['Open']
        high_value = row['High']
        low_value = row['Low']
        close_value = row['Close']

        minute_data.append({
            'Date': date,
            'Open': open_value,
            'High': high_value,
            'Low': low_value,
            'Close': close_value
        })

    return minute_data

async def fetch_async_yfinance_data(ticker, interval, period):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch_yfinance_data, ticker, interval, period)

@stock_response_router.get("/stock/{ticker}/{period}/{interval}")
async def stock_response_OHCL(ticker: str, period: str, interval: str):
    ticker = ticker + '.KS'
    minute_data = await fetch_async_yfinance_data(ticker, interval, period)
    return minute_data
