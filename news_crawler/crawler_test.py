from fastapi import FastAPI
from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

app = FastAPI()
news_crawler_router = APIRouter()


@news_crawler_router.get("/article/{stock_name}")
async def news_crawler(stock_name: str):
    decoded_stock_name = unquote(stock_name)
    all_data = []

    # for page_number in range(1, 192, 10):
    for page_number in range(1, 12, 10):
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={decoded_stock_name}&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:all,a:all&start={page_number}"
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

        all_data.extend(data)

    return all_data


app.include_router(news_crawler_router)
