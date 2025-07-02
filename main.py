from layers.review_layer import ReviewLayer

if __name__ == "__main__":
    samples = [
        "Mahmoud Nasr",
        "enta 7mar w 5ara",
        "How are you, friend?"
    ]

    engine = ReviewLayer()
    for s in samples:
        print(f"\nReview: {s}")
        print("Result:", engine.analyze_review(s))
