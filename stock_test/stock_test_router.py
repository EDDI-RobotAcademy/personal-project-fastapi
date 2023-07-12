from fastapi import APIRouter
import yfinance as yf

stock_test_router = APIRouter()

# @app.get("/stock/{ticker}")
# async def stock_ticker(ticker:str):
#     return {'ticker' : ticker}

@stock_test_router.get("/stock/{ticker}/{period}/{interval}")
async def stock_OHCL_test(ticker:str, period:str, interval:str):

    ticker = ticker + '.KS'

    result = yf.download(ticker, interval=interval, period=period)
    minute_data = []
    for index, row in result.iterrows():
        date = index.strftime('%Y-%m-%d %H:%M')  # 날짜, 시간, 분을 문자열로 변환
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

    return (minute_data)


