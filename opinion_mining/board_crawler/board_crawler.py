import concurrent.futures
import re
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BoardCrawler():
    def __init__(self, ticker):

        self.ticker = ticker
        self.url_list = []

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36")
        self.driver = webdriver.Chrome(
            executable_path='D:/project/personal-project-fastapi/opinion_mining/board_crawler/chromedriver.exe',
            options=chrome_options)

        code = ticker
        self.crawling_result = []

        self.wait = WebDriverWait(self.driver, 1)

        for i in range(1, 6):
            URL = f"https://finance.naver.com/item/board.naver?code={code}&page={i}"
            self.url_list.append(URL)
    def multi_thread_crawl(self):
        with ThreadPoolExecutor(max_workers=12) as executor:
            result = list(executor.map(self.board_crawler, self.url_list))

        self.driver.quit()
        return result
    def board_crawler(self, url):
        self.driver.get(url)

        titles = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "title")))

        link_list = []

        for title in titles:
            a_tag = title.find_element(By.TAG_NAME, "a")
            link = a_tag.get_attribute("href")
            link_list.append(link)

            title_text = title.text
            title_text = re.sub(r'[-=+,#/\?:^.\@*\"※~ㆍ!』‘\|\(\)\[\]`\'…》\”\“\’·a-zA-Z0-9\n]', '', title_text)
            self.crawling_result.append(title_text)

        for link in link_list:
            self.driver.get(link)

            content = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "scr01"))).text
            content = re.sub(r'[-=+,#/\?:^.\@*\"※~ㆍ!』‘\|\(\)\[\]`\'…》\”\“\’·a-zA-Z0-9\n]', '', content)
            self.crawling_result.append(content)
            # self.driver.get(url)

        return self.crawling_result

