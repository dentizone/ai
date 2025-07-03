from layers.models import ReviewLayerBuilder

if __name__ == "__main__":
    samples = [
     "a7a aybn el metnaka",
     "ana 7mar w 5ara",
     "How are you, friend?",
     "Good product, but the price is too high."
    ]

    engine = ReviewLayerBuilder().with_toxicity_layer("default").build()
    for s in samples:
        print(f"\nReview: {s}")
        print("Result:", engine.analyze_review(s))
