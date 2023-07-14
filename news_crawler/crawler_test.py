import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, APIRouter
from urllib.parse import unquote

app = FastAPI()

news_crawler_router = APIRouter()

@news_crawler_router.get("/article/{stock_name}")
async def news_crawler(stock_name: str):
    decoded_stock_name = unquote(stock_name)

    url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={decoded_stock_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_titles = soup.select("a.news_tit")
    news_companies = soup.select("a.info.press")

    # 배열 형식으로 구성
    data = [
      {
        "title": title['title'],
        "href": title['href'],
        "company": company.text
      }
      for title, company in zip(news_titles, news_companies)
    ]

    return data

app.include_router(news_crawler_router)
