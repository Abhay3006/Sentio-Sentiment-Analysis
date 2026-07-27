import { Sparkles } from "lucide-react";
import "./PredictButton.css";

function PredictButton({ onClick, loading }) {
  return (
    <button className="btn btn-primary" onClick={onClick} disabled={loading}>
      {loading ? (
        <>
          <span className="spinner" />
          Predicting...
        </>
      ) : (
        <>
          <Sparkles />
          Predict Sentiment
        </>
      )}
    </button>
  );
}

export default PredictButton;
