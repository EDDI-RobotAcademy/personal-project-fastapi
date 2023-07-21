import json

from fastapi import FastAPI, APIRouter

from opinion_mining.board_crawler.board_crawler import BoardCrawler
from opinion_mining.senti_word_calculator.calculator import SentiWordCalculator
from opinion_mining.tokenize.kiwi_tokenize import KiwiTokenizer

app = FastAPI()
opinion_mining_router = APIRouter()
with open("SentiWord_info.json", "r", encoding='utf-8') as f:
    sentiment_dictionary = json.load(f)

class SentiScoreResult:
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
    result = SentiScoreResult()

    crawling_result = BoardCrawler().board_crawler(ticker)

    for item in crawling_result:
        tokens = KiwiTokenizer().kiwi_tokenize(item)

        sentiment_score = SentiWordCalculator(tokens, sentiment_dictionary)
        result.update(sentiment_score)

    return {
        "total_sentiment_score": result.total_sentiment_score,
        "total_positive_count": result.total_positive_count,
        "total_negative_count": result.total_negative_count,
        "total_neutral_count": result.total_neutral_count,
    }