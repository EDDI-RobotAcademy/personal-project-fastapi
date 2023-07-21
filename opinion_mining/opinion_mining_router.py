import json
import time

from fastapi import FastAPI, APIRouter

from opinion_mining.board_crawler.board_crawler import BoardCrawler
from opinion_mining.senti_word_calculator.calculator import SentiWordCalculator
from opinion_mining.tokenize.kiwi_tokenize import KiwiTokenizer

app = FastAPI()
opinion_mining_router = APIRouter()
with open("SentiWord_info.json", "r", encoding='utf-8') as f:
    sentiment_dictionary = json.load(f)

class OpinionMiningResult:
    def __init__(self):
        self.total_sentiment_score = 0
        self.total_positive_count = 0
        self.total_negative_count = 0
        self.total_neutral_count = 0

    def update(self, sentiment_score):
        self.total_sentiment_score += sentiment_score.calculate_sentiment_score()
        self.total_positive_count += sentiment_score.positive_count
        self.total_negative_count += sentiment_score.negative_count
        self.total_neutral_count += sentiment_score.neutral_count

@opinion_mining_router.get("/opinion-mining/{ticker}")
async def opinion_mining(ticker: str):
    start_time = time.time()  # 시작 시간 저장

    senti_score_result = OpinionMiningResult()

    crawler = BoardCrawler(ticker)
    crawling_result = crawler.multi_thread_crawl()
    print("crawling_result: ", crawling_result)

    end_time = time.time()
    total_time = end_time - start_time  # 총 작동시간 계산
    total_time_int = int(total_time)  # 소수점 이하 자리수 탈락

    for item in crawling_result:
        tokens = KiwiTokenizer().kiwi_tokenize(item)
        print("tokens: ", tokens)

        sentiment_score = SentiWordCalculator(tokens, sentiment_dictionary)
        print("sentiment_score: ", sentiment_score)
        senti_score_result.update(sentiment_score)
        print("SentiScoreResult(): ", OpinionMiningResult())



    return {
        "total_sentiment_score": senti_score_result.total_sentiment_score,
        "total_positive_count": senti_score_result.total_positive_count,
        "total_negative_count": senti_score_result.total_negative_count,
        "total_neutral_count": senti_score_result.total_neutral_count,
        "total_time": total_time_int,  # 총 작동시간 추가
    }