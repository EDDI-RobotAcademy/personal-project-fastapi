import datetime
from fastapi import APIRouter
from pykrx import stock
import asyncio

class GetStockDataOCVA(APIRouter):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_stock_data(cls, OHCLVA: str, ascending: bool):
        today = datetime.date.today()
        weekday = today.weekday()

        if weekday == 0:
            yesterday = today - datetime.timedelta(days=3)
        elif weekday == 6:
            yesterday = today - datetime.timedelta(days=2)
        else:
            yesterday = today - datetime.timedelta(days=1)

        today = today.strftime('%Y%m%d')
        yesterday = yesterday.strftime('%Y%m%d')

        df = stock.get_market_price_change_by_ticker(yesterday, today)
        selected_df = df[["시가", "종가", "변동폭", "등락률", "거래량", "거래대금"]].sort_values(by=OHCLVA, ascending=ascending)

        # '티커'를 인덱스에서 추출하여 열로 추가
        selected_df.reset_index(inplace=True)

        return selected_df.to_dict(orient="records") if not selected_df.empty else {}


async def async_get_stock_data(OHCLVA: str, ascending: bool):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, GetStockDataOCVA.get_stock_data, OHCLVA, ascending)
    return result

get_stock_data_router = GetStockDataOCVA()

@get_stock_data_router.get("/stock/list/{OHCLVA}/{ascending}")
async def change_stock_price(OHCLVA: str, ascending: bool):
    selected_data = await async_get_stock_data(OHCLVA, ascending)
    return selected_data
