from layers.language_layer import LanguageDetectionLayer
from layers.sentiment_layer import SentimentLayer
from layers.toxicity_layer import ToxicityLayer

class ReviewLayer:
    _LABEL_MAP = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}

    def __init__(self):
        self.language_layer = LanguageDetectionLayer()
        self.sentiment_layer = SentimentLayer()
        self.toxicity_layer = ToxicityLayer()

    def analyze_review(self, text: str) -> dict:
        if not self.language_layer.is_english(text):
            return {
                "error": "This review is not in English. Please write your review in English.",
                "is_insult": self.toxicity_layer.is_insult(text)
            }
        return {
            "sentiment": self.sentiment_layer.classify_sentiment(text),
            "is_insult": self.toxicity_layer.is_insult(text)
        } 