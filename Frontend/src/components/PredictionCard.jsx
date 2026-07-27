import { ThumbsUp, ThumbsDown, Gauge, Sparkles, FileText } from "lucide-react";
import "./PredictionCard.css";

function PredictionCard({ result }) {
  const isPositive = /pos/i.test(result.prediction);
  const isNegative = /neg/i.test(result.prediction);
  const hasResult = isPositive || isNegative;

  const badgeClass = isPositive ? "positive" : isNegative ? "negative" : "neutral";

  return (
    <div className="prediction">
      <div className="prediction-header">
        <div>
          <h3 className="card-title" style={{ marginBottom: 4 }}>Prediction</h3>
          <p className="card-subtitle" style={{ margin: 0 }}>
            {hasResult ? "Model analysis complete" : "Run a prediction to see results"}
          </p>
        </div>
        <div className={`prediction-badge ${badgeClass}`}>
          {isPositive && <ThumbsUp size={16} />}
          {isNegative && <ThumbsDown size={16} />}
          {!hasResult && <Sparkles size={16} />}
          {result.prediction}
        </div>
      </div>

      <div className="stat-grid">
        <div className="stat">
          <div className="stat-label"><Gauge /> Confidence</div>
          <div className="stat-value">{result.confidence}%</div>
        </div>
        <div className="stat positive">
          <div className="stat-label"><ThumbsUp /> Positive</div>
          <div className="stat-value">{result.positive_probability}%</div>
        </div>
        <div className="stat negative">
          <div className="stat-label"><ThumbsDown /> Negative</div>
          <div className="stat-value">{result.negative_probability}%</div>
        </div>
      </div>

      {result.cleaned_review && (
        <div className="cleaned-review">
          <span className="cleaned-review-label">
            <FileText size={12} style={{ display: "inline", marginRight: 6, verticalAlign: -2 }} />
            Preprocessed Review
          </span>
          {result.cleaned_review}
        </div>
      )}
    </div>
  );
}

export default PredictionCard;
