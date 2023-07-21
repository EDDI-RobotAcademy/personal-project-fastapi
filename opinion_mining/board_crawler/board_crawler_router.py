import re
import json

from fastapi import FastAPI
from fastapi import APIRouter
from kiwipiepy import Kiwi
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from opinion_mining.senti_word_calculator.calculator import SentiWordCalculator

app = FastAPI()
board_crawler_router = APIRouter()
kiwi = Kiwi(model_type='knlm')
with open("SentiWord_info.json", "r", encoding='utf-8') as f:
    sentiment_dictionary = json.load(f)


@board_crawler_router.get("/board-crawler/{ticker}")
async def board_crawler(ticker:str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    driver = webdriver.Chrome(executable_path='D:/project/personal-project-fastapi/opinion_mining/board_crawler/chromedriver.exe', chrome_options=chrome_options)

    code = ticker

    crawling_result = []

    total_sentiment_score = 0
    total_positive_count = 0
    total_negative_count = 0
    total_neutral_count = 0

    for i in range(1, 2):
        URL = f"https://finance.naver.com/item/board.naver?code={code}&page={i}"

        driver.get(URL)
        wait = WebDriverWait(driver, 1)

        titles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "title")))

        link_list = []

        for title in titles:
            a_tag = title.find_element(By.TAG_NAME, "a")
            link = a_tag.get_attribute("href")
            link_list.append(link)

            title_text = title.text
            title_text = re.sub(r'[-=+,#/\?:^.\@*\"※~ㆍ!』‘\|\(\)\[\]`\'…》\”\“\’·a-zA-Z0-9\n]', '', title_text)
            crawling_result.append(title_text)

        for link in link_list:
            original_url = driver.current_url
            driver.get(link)

            content = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "scr01"))).text
            content = re.sub(r'[-=+,#/\?:^.\@*\"※~ㆍ!』‘\|\(\)\[\]`\'…》\”\“\’·a-zA-Z0-9\n]', '', content)
            crawling_result.append(content)
            driver.get(original_url)

    for item in crawling_result:
        result = kiwi.tokenize(item)

        tokens = []

        for token in result:
            if token.tag in ['NNG', 'NNP', 'VA', 'VV', 'MAG', 'XR', 'SL']:
                tokens.append(token.form)

        sentiment_score = SentiWordCalculator(tokens, sentiment_dictionary)
        total_sentiment_score += sentiment_score.calculate_sentiment_score()
        total_positive_count += sentiment_score.positive_count
        total_negative_count += sentiment_score.negative_count
        total_neutral_count += sentiment_score.neutral_count
        print(f"Tokens: {tokens}, {sentiment_score}")

        print(
                f"감정 점수: {total_sentiment_score}, "
                f"양수 토큰 개수: {total_positive_count}, "
                f"음수 토큰 개수: {total_negative_count}, "
                f"중립 토큰 개수: {total_neutral_count}")

    driver.quit()

