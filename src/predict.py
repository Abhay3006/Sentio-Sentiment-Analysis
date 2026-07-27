import joblib
import time

from pathlib import Path
from preprocessing import preprocess_text

# Load model and vectorizer once
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "Models" / "sentiment_model.pkl"
VECTORIZER_PATH = BASE_DIR / "Models" / "tfidf_vectorizer.pkl"

model = joblib.load(MODEL_PATH)
tfidf = joblib.load(VECTORIZER_PATH)


def predict_sentiment(review):

    # Apply the same preprocessing used during training
    cleaned_review = preprocess_text(review)

    if not cleaned_review.strip():
        raise ValueError(
            "Review is empty after preprocessing."
        )

    # Convert to TF-IDF
    review_tfidf = tfidf.transform([cleaned_review])

    # Predict sentiment
    prediction = model.predict(review_tfidf)[0]

    # Predict probabilities
    probabilities = model.predict_proba(review_tfidf)[0]

    return {
        "cleaned_review": cleaned_review,
        "prediction": prediction.capitalize(),
        "negative_probability": round(probabilities[0] * 100, 2),
        "positive_probability": round(probabilities[1] * 100, 2),
        "confidence": round(max(probabilities) * 100, 2)
    }

    

def predict_sentiment_batch(reviews, progress):

    total = len(reviews)
    chunk_size = max(50, total // 100)
       
    start_time = time.time()
    
    results = []

    for start in range(0, total, chunk_size):

        if progress["cancelled"]:
            return []

        end = min(start + chunk_size, total)

        chunk = [

            preprocess_text(review)

            for review in reviews[start:end]

        ]

        X = tfidf.transform(chunk)

        predictions = model.predict(X)

        probabilities = model.predict_proba(X)

        for cleaned_review, prediction, probability in zip(
            chunk,
            predictions,
            probabilities
        ):

            results.append({

                "cleaned_review": cleaned_review,
                "prediction": prediction.capitalize(),
                "negative_probability": round(probability[0] * 100, 2),
                "positive_probability": round(probability[1] * 100, 2),
                "confidence": round(max(probability) * 100, 2)

            })

        processed = end
                            
        progress["processed"] = processed       
        progress["progress"] = 30 + int((processed / total) * 60)
                            
        elapsed = time.time() - start_time
                            
        if processed > 0:
                            
            reviews_per_second = processed / elapsed

            if reviews_per_second > 0:                           
                remaining = total - processed         
                progress["eta"] = int(remaining / reviews_per_second)

    return results

def main():

    review = input("Enter Review: ")

    result = predict_sentiment(review)

    print(f"\nPrediction: {result['prediction']}")

    print(f"\nConfidence: {result['confidence']:.2f}%")

    print("\nProbabilities:")
    print(f"Negative: {result['negative_probability']:.2f}%")
    print(f"Positive: {result['positive_probability']:.2f}%")


if __name__ == "__main__":
    main()