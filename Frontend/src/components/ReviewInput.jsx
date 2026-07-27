import "./ReviewInput.css";

function ReviewInput({ review, setReview }) {
  return (
    <div className="review-input-wrap">
      <textarea
        className="review-input"
        placeholder="Paste or type a movie review here... e.g. 'The cinematography was breathtaking and the story kept me hooked from start to finish.'"
        value={review}
        onChange={(event) => setReview(event.target.value)}
      />
      <span className="review-input-meta">{review.length} chars</span>
    </div>
  );
}

export default ReviewInput;
