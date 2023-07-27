import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup


class BoardCrawler():
    def __init__(self, ticker):

        self.ticker = ticker
        self.url_list = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }

        code = ticker

        for i in range(1, 6):
            URL = f"https://finance.naver.com/item/board.naver?code={code}&page={i}"
            self.url_list.append(URL)

    async def fetch(self, session, url):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()

    async def async_crawl(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in urls]
            return await asyncio.gather(*tasks)

    async def multi_thread_crawl(self):
        crawling_result = []
        htmls = await self.async_crawl(self.url_list)

        for html in htmls:
            soup = BeautifulSoup(html, 'html.parser')
            titles = soup.select('.title')
            link_list = []

            for title in titles:
                a_tag = title.find('a')
                link = 'https://finance.naver.com' + a_tag.get('href')
                link_list.append(link)

                title_text = title.text
                title_text = re.sub(r'[-=+,#/\?:^.\@*\"※~ㆍ!』‘\|\(\)\[\]`\'…》\”\“\’·a-zA-Z0-9\n]', '', title_text)
                crawling_result.append(title_text)

            content_htmls = await self.async_crawl(link_list)
            for content_html in content_htmls:
                soup = BeautifulSoup(content_html, 'html.parser')
                content = soup.find('div', class_='view_se').text  # 수정된 부분
                content = re.sub(r'[-=+,#/\?:^.\@*\"※~ㆍ!』‘\|\(\)\[\]`\'…》\”\“\’·a-zA-Z0-9\n]', '', content)
                crawling_result.append(content)

        return crawling_result