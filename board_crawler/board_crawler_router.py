import re

from PyKomoran import *
from fastapi import FastAPI
from fastapi import APIRouter
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

app = FastAPI()
board_crawler_router = APIRouter()

@board_crawler_router.get("/board-crawler/{ticker}")
async def board_crawler(ticker:str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    driver = webdriver.Chrome(executable_path='D:/project/personal-project-fastapi/board_crawler/chromedriver.exe', chrome_options=chrome_options)

    code = ticker

    for i in range(1, 2):
        URL = f"https://finance.naver.com/item/board.naver?code={code}&page={i}"

        driver.get(URL)
        wait = WebDriverWait(driver, 1)

        titles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "title")))

        title_list = []
        link_list = []

        for title in titles:
            a_tag = title.find_element(By.TAG_NAME, "a")
            link = a_tag.get_attribute("href")
            link_list.append(link)

            title_text = title.text
            title_text = re.sub(r'[-=+,#/\?:^.\@*\"※~ㆍ!』‘\|\(\)\[\]`\'…》\”\“\’·a-zA-Z0-9\n]', '', title_text)
            title_list.append(title_text)

        contents = []
        for link in link_list:
            original_url = driver.current_url
            driver.get(link)

            content = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "scr01"))).text
            content = re.sub(r'[-=+,#/\?:^.\@*\"※~ㆍ!』‘\|\(\)\[\]`\'…》\”\“\’·a-zA-Z0-9\n]', '', content)
            contents.append(content)
            driver.get(original_url)

        print("title_list: ", title_list)
        print("contents: ",contents)
    driver.quit()
