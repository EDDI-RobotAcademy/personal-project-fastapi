from fastapi import APIRouter
import yfinance as yf

stock_test_router = APIRouter()
@stock_test_router.get("/stock/test")
async def stock_OHCL_test():

    result = yf.download('005930.KS', interval='1m', period='1d')
    minute_data = result[['Open', 'High', 'Close', 'Low']]
    json_data = minute_data.to_json(orient='records')

    return json_data


