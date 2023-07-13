import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter

news_crawler_router = APIRouter()
@news_crawler_router.get("/article/{stock_name}")
def news_crawler(stock_name: str):
    url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={stock_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_titles = soup.select("a.news_tit")
    news_companies = soup.select("a.info.press")
    news_images = soup.select("img.thumb.api_get")

    titles = [title['title'] for title in news_titles]
    hrefs = [title['href'] for title in news_titles]
    companies = [company.text for company in news_companies]
    images = [img['src'] for img in news_images]