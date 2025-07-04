from transformers import pipeline

class SentimentLayer:
    _LABEL_MAP = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}

    def __init__(self):
        self._sentiment_pipe = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment"
        )

    def classify_sentiment(self, text: str) -> str:
        raw = self._sentiment_pipe(text, truncation=True)[0]["label"]
        return self._LABEL_MAP.get(raw, raw) 