from layers.agent.nfea_agent import NFEAAgent
from layers.models.language_layer import LanguageDetectionLayer
from layers.models.sentiment_layer import SentimentLayer
from layers.models.toxicity_layer import ToxicityLayer

class ReviewLayer:
    _LABEL_MAP = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}

    def __init__(self, agent=None, language_layer=None, sentiment_layer=None, toxicity_layer=None):
        self.agent = agent
        self.language_layer = language_layer
        self.sentiment_layer = sentiment_layer
        self.toxicity_layer = toxicity_layer
        # If all are None, use all defaults
        if all(x is None for x in [agent, language_layer, sentiment_layer, toxicity_layer]):
            self.agent = NFEAAgent()
            self.language_layer = LanguageDetectionLayer()
            self.sentiment_layer = SentimentLayer()
            self.toxicity_layer = ToxicityLayer()

    def analyze_review(self, text: str) -> dict:
        result = {}
        contact_info = None
        if self.agent is not None:
            contact_info = self.agent.process(text)
            result["contact_info"] = contact_info
        if self.language_layer is not None:
            if not self.language_layer.is_english(text):
                result["error"] = "This review is not in English. Please write your review in English."
        if self.toxicity_layer is not None:
            result["is_insult"] = self.toxicity_layer.is_insult(text)
        if self.sentiment_layer is not None and ("error" not in result):
            result["sentiment"] = self.sentiment_layer.classify_sentiment(text)
        return result

class ReviewLayerBuilder:
    _AGENT_OPTIONS = {
        'nfea': NFEAAgent
    }
    _LANGUAGE_LAYER_OPTIONS = {
        'default': LanguageDetectionLayer
    }
    _SENTIMENT_LAYER_OPTIONS = {
        'default': SentimentLayer
    }
    _TOXICITY_LAYER_OPTIONS = {
        'default': ToxicityLayer
    }

    def __init__(self):
        self._agent_key = None
        self._language_layer_key = None
        self._sentiment_layer_key = None
        self._toxicity_layer_key = None

    def with_agent(self, agent_key):
        if agent_key not in self._AGENT_OPTIONS:
            raise ValueError(f"Unknown agent: {agent_key}")
        self._agent_key = agent_key
        return self

    def with_language_layer(self, language_layer_key):
        if language_layer_key not in self._LANGUAGE_LAYER_OPTIONS:
            raise ValueError(f"Unknown language layer: {language_layer_key}")
        self._language_layer_key = language_layer_key
        return self

    def with_sentiment_layer(self, sentiment_layer_key):
        if sentiment_layer_key not in self._SENTIMENT_LAYER_OPTIONS:
            raise ValueError(f"Unknown sentiment layer: {sentiment_layer_key}")
        self._sentiment_layer_key = sentiment_layer_key
        return self

    def with_toxicity_layer(self, toxicity_layer_key):
        if toxicity_layer_key not in self._TOXICITY_LAYER_OPTIONS:
            raise ValueError(f"Unknown toxicity layer: {toxicity_layer_key}")
        self._toxicity_layer_key = toxicity_layer_key
        return self

    def build(self):
        # If all are None, ReviewLayer will use all defaults
        agent = self._AGENT_OPTIONS[self._agent_key]() if self._agent_key is not None else None
        language_layer = self._LANGUAGE_LAYER_OPTIONS[self._language_layer_key]() if self._language_layer_key is not None else None
        sentiment_layer = self._SENTIMENT_LAYER_OPTIONS[self._sentiment_layer_key]() if self._sentiment_layer_key is not None else None
        toxicity_layer = self._TOXICITY_LAYER_OPTIONS[self._toxicity_layer_key]() if self._toxicity_layer_key is not None else None
        return ReviewLayer(
            agent=agent,
            language_layer=language_layer,
            sentiment_layer=sentiment_layer,
            toxicity_layer=toxicity_layer
        ) 