from fastapi import FastAPI
from fastapi import APIRouter
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import urllib

app = FastAPI()
board_crawler_router = APIRouter()

@app.board_crawler("/board-crawler}")
async def board_crawler():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"')
    driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
    URL = "https://finance.naver.com/item/board.naver?code=950210"
    driver.get(URL)
    time.sleep(2)

    driver.switch_to_frame(driver.find_element())