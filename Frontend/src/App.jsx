import { useState } from "react";

import Header from "./components/Header";
import ReviewInput from "./components/ReviewInput";
import PredictButton from "./components/PredictButton";
import PredictionCard from "./components/PredictionCard";
import CSVUpload from "./components/CSVUpload";
import ModeToggle from "./components/ModeToggle";
import "./App.css";

function App() {
  const [csvLoading, setCsvLoading] = useState(false);
  const [error, setError] = useState("");
  const [review, setReview] = useState("");
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("review");
  const [result, setResult] = useState({
    prediction: "Not Predicted Yet",
    confidence: 0,
    positive_probability: 0,
    negative_probability: 0,
  });

  async function predictSentiment() {

    if (!review.trim()) {
        setError("Please enter a review.");
        return;
    }

    setError("");
    setLoading(true);

    try {

        const response = await fetch(
          "http://127.0.0.1:8000/predict",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              review: review,
            }),
          }
        );

        if (!response.ok) {
          const err = await response.json();
          throw new Error(err.detail);
        }

        const data = await response.json();
        setResult(data);

    }
    catch (error) {

        setResult({
            prediction: "Error",
            confidence: 0,
            positive_probability: 0,
            negative_probability: 0
        });

        if (err.message === "Failed to fetch") {
          setError("Unable to connect to the server.");
        }
        else {
          setError(err.message);
        }

    }
    finally {
        setLoading(false);
    }

  }

  function clearReview() {

    setReview("");
    setError("");

    setResult({
        prediction: "Not Predicted Yet",
        confidence: 0,
        positive_probability: 0,
        negative_probability: 0
    });

  }

  return (
    <div className="app-shell">
      <Header
        title="Sentiment intelligence for text"
        tagline="Sentio is an AI-powered engine that analyzes movie reviews at scale — instant predictions, confidence scores, and bulk CSV insights."
      />

      <main className="app-main">
        <ModeToggle
          mode={mode}
          setMode={setMode}
          disabled={loading || csvLoading}
        />

        {mode === "review" && (
          <>
            <section className="card animate-scale-in">
              <h3 className="card-title">Analyze a Review</h3>
              <p className="card-subtitle">Type or paste a movie review to see how our model interprets its sentiment.</p>

              <ReviewInput review={review} setReview={setReview} />

              <div className="button-row">
                <PredictButton onClick={predictSentiment} loading={loading} />
                <button className="btn btn-ghost" onClick={clearReview}>
                  Clear
                </button>
              </div>

              {error && (
                <div className="error-box">
                    {error}
                </div>
              )}
            </section>

            <section className="card">
              <PredictionCard result={result} />
            </section>
          </>
        )}

        {mode === "csv" && (
          <section className="card animate-scale-in">
            <CSVUpload
              setCsvLoading={setCsvLoading}
            />
          </section>
        )}
      </main>

      <footer className="footer">
        Built with <strong>Sentio</strong> · Logistic Regression · TF-IDF · FastAPI
      </footer>
    </div>
  );
}

export default App;
