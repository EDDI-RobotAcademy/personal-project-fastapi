import datetime

from fastapi import APIRouter
from pykrx import stock

# OHCLVA "시가", "종가", "변동폭", "등락률", "거래량", "거래대금"
# ascending: True, False

class Top30Stock(APIRouter):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_top_stock_data(cls, OHCLVA: str, ascending: bool):

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
        return selected_df.head(30)

top30_router = Top30Stock()

@top30_router.get("/stock/list/{OHCLVA}/{ascending}")
async def change_stock_price(OHCLVA: str, ascending: bool):
    selected_df = Top30Stock.get_top_stock_data(OHCLVA, ascending)
    return selected_df.to_dict(orient="index")
