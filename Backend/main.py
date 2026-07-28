import sys
import uuid
import pandas as pd
import traceback
import io

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from predict import predict_sentiment, predict_sentiment_batch


# Folder to store processed CSV files
DOWNLOAD_FOLDER = Path("downloads")
DOWNLOAD_FOLDER.mkdir(exist_ok=True)

jobs = {}

app = FastAPI(
    title="Sentiment Analysis API",
    description="Predicts movie review sentiment using Logistic Regression and TF-IDF",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://sentio-sentiment-analysis.vercel.app",
        "https://sentio-sentiment-analysis-5j2ol9mz5-abhayrajsingh-bopche.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewRequest(BaseModel):
    review: str


class PredictionResponse(BaseModel):
    cleaned_review: str 
    prediction: str
    confidence: float
    positive_probability: float
    negative_probability: float

@app.get("/")
def home():
    return {
        "message": "Sentiment Analysis API is running successfully!"
    }

@app.get("/progress/{job_id}")
def get_progress(job_id: str):

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return jobs[job_id]

@app.post("/predict", response_model=PredictionResponse)
def predict(request: ReviewRequest):

    try:
        result = predict_sentiment(request.review)
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Model files not found."
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed."
        )

def process_csv(job_id: str, file_bytes: bytes):

    progress = jobs[job_id]

    try:
        progress["stage"] = "File Uploaded"
        progress["progress"] = 5

        progress["stage"] = "Reading CSV"
        progress["progress"] = 10

        df = None

        encodings = [
            "utf-8",
            "utf-8-sig",
            "cp1252",
            "latin1"
        ]

        for enc in encodings:

            try:
                df = pd.read_csv(
                    io.BytesIO(file_bytes),
                    encoding=enc
                )
                break

            except UnicodeDecodeError:
                continue

        if df is None:
            raise Exception(
                "Unsupported file encoding."
            )

        if df.empty:
            raise Exception(
                "CSV file is empty."
            )

        if "review" not in df.columns:
            raise Exception(
                "CSV must contain 'review' column."
            )

        progress["stage"] = "Cleaning Text"
        progress["progress"] = 20

        df = df.dropna(subset=["review"])
        df["review"] = df["review"].astype(str)
        df = df[df["review"].str.strip() != ""]

        if df.empty:
            raise Exception(
                "No valid reviews found."
            )

        progress["total"] = len(df)

        progress["stage"] = "Predicting Sentiment"
        progress["progress"] = 30

        results = predict_sentiment_batch(
            df["review"].tolist(),
            progress
        )

        if progress["cancelled"]:

            progress["stage"] = "Cancelled"
            progress["progress"] = 0
            progress["eta"] = 0

            return

        df["cleaned_review"] = [
            r["cleaned_review"]
            for r in results
        ]

        df["sentiment"] = [
            r["prediction"]
            for r in results
        ]

        df["confidence"] = [
            r["confidence"]
            for r in results
        ]

        df["positive_probability"] = [
            r["positive_probability"]
            for r in results
        ]

        df["negative_probability"] = [
            r["negative_probability"]
            for r in results
        ]

        total_reviews = len(df)
        positive_reviews = (df["sentiment"] == "Positive").sum()
        negative_reviews = (total_reviews - positive_reviews)

        filename = f"{job_id}.csv"
        filepath = DOWNLOAD_FOLDER / filename

        progress["stage"] = "Saving Results"
        progress["progress"] = 95

        df.to_csv(
            filepath,
            index=False
        )

        progress["stage"] = "Ready to Download"
        progress["progress"] = 100

        progress["processed"] = progress["total"]

        progress["eta"] = 0

        progress["summary"] = {

            "total_reviews": total_reviews,
            "positive_reviews": int(positive_reviews),
            "negative_reviews": int(negative_reviews)

        }

    except ValueError as e:
        progress["stage"] = "Failed"
        progress["error"] = str(e)
        progress["progress"] = 100
        progress["eta"] = 0

    except Exception:
        progress["stage"] = "Failed"
        progress["error"] = "An unexpected error occurred while processing the file."
        progress["progress"] = 100
        progress["eta"] = 0
        traceback.print_exc()

@app.post("/predict-csv")
async def predict_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    job_id = uuid.uuid4().hex

    jobs[job_id] = {

        "stage": "Waiting",
        "progress": 0,
        "processed": 0,
        "total": 0,
        "eta": 0,
        "summary": None,
        "error": None,
        "cancelled": False

    }

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    background_tasks.add_task(

        process_csv,
        job_id,
        file_bytes

    )

    return {
        "job_id": job_id
    }



@app.post("/cancel/{job_id}")
def cancel_job(job_id: str):

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    jobs[job_id]["cancelled"] = True

    return {
        "message": "Job cancelled."
    }

@app.get("/download/{job_id}")
def download_csv(job_id: str):

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    filename = f"{job_id}.csv"

    filepath = DOWNLOAD_FOLDER / filename

    if not filepath.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return FileResponse(

        path=filepath,
        filename="sentiment_results.csv",
        media_type="text/csv"

    )