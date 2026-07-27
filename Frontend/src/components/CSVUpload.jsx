import { useState, useRef, useEffect } from "react";
import { UploadCloud, FileSpreadsheet, Download, BarChart3, ThumbsUp, ThumbsDown, Sparkles } from "lucide-react";
import "./CSVUpload.css";

function CSVUpload({ setCsvLoading }) {

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [summary, setSummary] = useState(null);
  const [stage, setStage] = useState("Waiting...");
  const [processed, setProcessed] = useState(0);
  const [total, setTotal] = useState(0);
  const [eta, setEta] = useState(0);
  const [jobId, setJobId] = useState("");
  const pollingInterval = useRef(null);
  const [error, setError] = useState("");

  const fetchProgress = async (id) => {

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/progress/${id}`
        );

        if (!response.ok) {

          const err = await response.json();
          setError(err.detail);
          setLoading(false);
          setCsvLoading(false);
          return false;
        }

        const data = await response.json();

        setProgress(data.progress);
        setStage(data.stage);
        setProcessed(data.processed);
        setTotal(data.total);
        setEta(data.eta);

        if (data.error) {
          setError(data.error);
          setLoading(false);
          setCsvLoading(false);
        }

        if (data.summary) {
            setSummary(data.summary);
        }

        if (data.progress === 100) {
            return true;
        }

        return false;
    }

    catch (err) {
      setError("Unable to connect to the server.");
      setLoading(false);
      setCsvLoading(false);
      return false;
    }
  };

  function formatETA(seconds, progress) {

    if (progress === 100) {
        return "Completed";
    }

    if (seconds === null || seconds === undefined || Number.isNaN(seconds)) {
        return "--";
    }

    seconds = Number(seconds);

    if (seconds <= 0) {
        return '0 sec';
    }

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    if (hours > 0) {
        return `${hours} hr ${minutes} min ${remainingSeconds} sec`;
    }

    if (minutes > 0) {
        return `${minutes} min ${remainingSeconds} sec remaining`;
    }

    return `${remainingSeconds} sec`;

  }

  async function uploadCSV() {

    if (!file) {
      setError("Please select a CSV file.");
      return;
    }

    setLoading(true);
    setProgress(0);
    setSummary(null);
    setError("");
    setEta(0);
    setCsvLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/predict-csv",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {

        const error = await response.json();
        throw new Error(error.detail);

      }

      const data = await response.json();

      setJobId(data.job_id);

      if (pollingInterval.current) {
        clearInterval(pollingInterval.current);
      }

      pollingInterval.current = setInterval(async () => {

        const finished = await fetchProgress(data.job_id);

        if (finished) {

          clearInterval(pollingInterval.current);
          pollingInterval.current = null;
          setLoading(false);
          setCsvLoading(false);

        }

      }, 500);

    }
    catch (err) {

      if (err.message === "Failed to fetch") {
        setError("Unable to connect to the server.");
      }
      else {
        setError(err.message);
      }

      setLoading(false);
      setProgress(0);
      setEta(0);
      setCsvLoading(false);

    }

  }

  async function cancelAnalysis() {

    try {

        await fetch(
            `http://127.0.0.1:8000/cancel/${jobId}`,
            {
                method: "POST"
            }
        );

    }
    catch {}

    if (pollingInterval.current) {

        clearInterval(pollingInterval.current);
        pollingInterval.current = null;

    }

    setLoading(false);
    setCsvLoading(false);

    setProgress(0);
    setProcessed(0);
    setTotal(0);
    setEta(0);

    setSummary(null);

    setError("Analysis cancelled.");

  }

  function downloadCSV() {

    window.open(
      `http://127.0.0.1:8000/download/${jobId}`,
      "_blank"
    );

  }

  function clearAll() {

    if (pollingInterval.current) {

        clearInterval(pollingInterval.current);
        pollingInterval.current = null;

    }

    setJobId("");
    setFile(null);
    setLoading(false);
    setCsvLoading(false);
    setProgress(0);
    setSummary(null);
    setError("");
    setEta(0);

    document.getElementById("csvFileInput").value = "";

  }

  useEffect(() => {

    return () => {

        if (pollingInterval.current) {
            clearInterval(pollingInterval.current);
        }

    };

  }, []);

  return (
    <div>

      <h3 className="card-title">Bulk CSV Analysis</h3>

      <p className="card-subtitle">
        Upload a CSV with a <code style={{ color: "#c4b5fd" }}>'review'</code> column and get sentiment for every row.
      </p>

      <label className={`dropzone ${file ? "has-file" : ""}`}>
        <input
          id="csvFileInput"
          type="file"
          accept=".csv"
          disabled={loading}
          onChange={(event) => {
            setFile(event.target.files[0]);
            setSummary(null);
            setProgress(0);
            setEta(0);
            setError("");
          }}
        />

        <div className="dropzone-icon">
          <UploadCloud />
        </div>

        <div className="dropzone-title">
          {file ? "File ready to analyze" : "Drop your CSV here, or click to browse"}
        </div>

        <div className="dropzone-hint">Accepted format: .csv · Max recommended: 10MB</div>
        
        {file && (
          <div className="dropzone-file">
            <FileSpreadsheet size={14} />
            {file.name}
          </div>
        )}

      </label>

      <div className="button-row">

        <button className="btn btn-primary" onClick={uploadCSV} disabled={loading}>
          {loading ? (<><span className="spinner" />Analyzing...</>) : (<><Sparkles />Analyze CSV</>)}
        </button>
          
        {loading ? (

          <button
              className="btn btn-ghost"
              onClick={cancelAnalysis}
          >
              Cancel
          </button>

        ) : (

          <button
              className="btn btn-ghost"
              onClick={clearAll}
          >
              Clear
          </button>

        )}

      </div>

      {(loading || progress === 100) && (
        <div className="progress-wrap">

          <div className="progress-header">
            <span>{stage}</span>
            <span>{progress}%</span>
          </div>

          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>

          <br />

          <div className="progress-header">

            <span>
              Predicting {processed.toLocaleString()} / {total.toLocaleString()} Reviews
            </span>

            <span>
              Time Remaining: {formatETA(eta, progress)}
            </span>

          </div>
        </div>
      )}

      {error && (

        <div className="error-box">
          {error}
        </div>

      )}

      {summary && (
        <>
          <div className="summary-grid">

            <div className="summary-card">
              <div className="summary-label"><BarChart3 /> Total Reviews</div>
              <div className="summary-value">{summary.total_reviews}</div>
            </div>

            <div className="summary-card positive">
              <div className="summary-label"><ThumbsUp /> Positive</div>
              <div className="summary-value">{summary.positive_reviews}</div>
            </div>

            <div className="summary-card negative">
              <div className="summary-label"><ThumbsDown /> Negative</div>
              <div className="summary-value">{summary.negative_reviews}</div>
            </div>

          </div>

          <div className="button-row">

            <button className="btn btn-primary" onClick={downloadCSV}>
              <Download />
              Download Processed CSV
            </button>

          </div>
        </>
      )}
    </div>
  );
}

export default CSVUpload;
