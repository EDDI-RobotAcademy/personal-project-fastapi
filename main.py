from fastapi import FastAPI

from save_ticker.save_ticker_router import save_ticker_router
from stock_test.stock_test_router import stock_test_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(stock_test_router)
app.include_router(save_ticker_router)

# @app.get("/stock/{ticker}")
# async def stock_ticker(ticker:str):
#     return {'ticker' : ticker}
