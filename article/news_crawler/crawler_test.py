from fastapi import FastAPI
from fastapi import APIRouter
import httpx
from bs4 import BeautifulSoup
from urllib.parse import unquote

app = FastAPI()
news_crawler_router = APIRouter()


async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response


@news_crawler_router.get("/article/{stock_name}/{now_page}")
async def news_crawler(stock_name: str, now_page: str):
    all_data = []

    url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={stock_name}&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:all,a:all&start={now_page}"
    response = await fetch_url(url)

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
