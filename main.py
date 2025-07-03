from layers.models import review_layer
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/all")
def analyze_all(text: str = Query(..., description="Input text to analyze")):
    engine = review_layer.ReviewLayerBuilder().build()
    result = engine.analyze_review(text)
    return result

@app.get("/sentiment")
def analyze_sentiment(text: str = Query(..., description="Input text to analyze")):
    engine = review_layer.ReviewLayerBuilder().with_sentiment_layer("default").build()
    result = engine.analyze_review(text)
    return result

@app.get("/lang")
def analyze_language(text: str = Query(..., description="Input text to analyze")):
    engine = review_layer.ReviewLayerBuilder().with_language_layer("default").build()
    result = engine.analyze_review(text)
    return result

@app.get("/toxic")
def analyze_toxicity(text: str = Query(..., description="Input text to analyze")):
    engine = review_layer.ReviewLayerBuilder().with_toxicity_layer("default").build()
    result = engine.analyze_review(text)
    return result

@app.get("/contact-toxic")
def analyze_contact_and_toxicity(text: str = Query(..., description="Input text to analyze")):
    engine = review_layer.ReviewLayerBuilder().with_agent("nfea").with_toxicity_layer("default").build()
    result = engine.analyze_review(text)
    # Only return contact_info and is_insult fields
    filtered_result = {}
    if "contact_info" in result:
        filtered_result["contact_info"] = result["contact_info"]
    if "is_insult" in result:
        filtered_result["is_insult"] = result["is_insult"]
    return filtered_result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
