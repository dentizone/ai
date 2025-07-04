from transformers import pipeline

class ToxicityLayer:
    def __init__(self):
        self._toxicity_pipe = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            top_k=None
        )

    def is_insult(self, text: str, threshold: float = 0.51) -> bool:
        for pred in self._toxicity_pipe(text, truncation=True)[0]:
            if pred["label"].lower() != "neutral" and pred["score"] >= threshold:
                return True
        return False 