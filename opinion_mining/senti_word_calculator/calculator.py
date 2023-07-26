class SentiWordCalculator:
    def __init__(self, tokens, sentiment_dictionary):
        self.tokens = tokens
        self.sentiment_dictionary = sentiment_dictionary
        self.sentiment_score = 0
        self.positive_count = 0
        self.negative_count = 0
        self.neutral_count = 0

    def calculate_sentiment_score(self):
        self.sentiment_score = 0
        self.positive_count = 0
        self.negative_count = 0
        self.neutral_count = 0

        for token in self.tokens:
            found = False
            for sentiment in self.sentiment_dictionary:
                if token in sentiment["word_root"]:
                    sentiment_score = int(sentiment["polarity"])
                    self.sentiment_score += sentiment_score
                    if sentiment_score > 0:
                        self.positive_count += 1
                    elif sentiment_score < 0:
                        self.negative_count += 1
                    else:
                        self.neutral_count += 1
                    found = True
                    break

            if not found:
                self.neutral_count += 1

        return self.sentiment_score

    def __str__(self):
        sentiment_score = self.calculate_sentiment_score()
        return f"감정 점수: {sentiment_score}, 양수 토큰 개수: {self.positive_count}, 음수 토큰 개수: {self.negative_count}, 중립 토큰 개수: {self.neutral_count}"

