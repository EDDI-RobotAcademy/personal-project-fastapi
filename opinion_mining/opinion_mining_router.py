import json
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from timeit import timeit

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

def process_item(item):
    kiwi_tokenizer = KiwiTokenizer()
    tokens = kiwi_tokenizer.kiwi_tokenize(item)
    sentiment_score = SentiWordCalculator(tokens, sentiment_dictionary)
    return sentiment_score

@opinion_mining_router.get("/opinion-mining/{ticker}")
async def opinion_mining(ticker: str):

    senti_score_result = OpinionMiningResult()

    crawler = BoardCrawler(ticker)
    crawling_result = crawler.multi_thread_crawl()

    with ThreadPoolExecutor(max_workers=12) as executor:
        for items in crawling_result:
            sentiment_scores = list(executor.map(process_item, items))
            for sentiment_score in sentiment_scores:
                senti_score_result.update(sentiment_score)

    return {
        "total_sentiment_score": senti_score_result.total_sentiment_score,
        "total_positive_count": senti_score_result.total_positive_count,
        "total_negative_count": senti_score_result.total_negative_count,
        "total_neutral_count": senti_score_result.total_neutral_count,
    }