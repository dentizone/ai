from transformers import pipeline

class LanguageDetectionLayer:
    def __init__(self):
        self._lang_pipe = pipeline(
            "text-classification",
            model="papluca/xlm-roberta-base-language-detection",
            top_k=None
        )

    def is_english(self, text: str, threshold: float = 0.80) -> bool:
        for pred in self._lang_pipe(text, truncation=True)[0]:
            if pred["label"] == "en" and pred["score"] >= threshold:
                return True
        return False 