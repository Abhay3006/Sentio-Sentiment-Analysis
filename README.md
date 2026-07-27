# Sentio - Sentiment Analysis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn)
![License](https://img.shields.io/badge/License-MIT-green)

An AI-powered Sentiment Analysis web application that predicts whether movie reviews are **Positive** or **Negative** using a machine learning model trained on the IMDB Movie Reviews dataset.

</div>

---

## Overview

Sentio is a full-stack machine learning web application that combines natural language processing, machine learning, and modern web technologies to perform real-time sentiment analysis on movie reviews.

The project includes:

- Single Review Prediction
- Bulk CSV Sentiment Analysis
- Real-time Progress Tracking
- Downloadable Prediction Reports
- RESTful FastAPI Backend
- React Frontend
- Logistic Regression Machine Learning Model
- TF-IDF Vectorization Pipeline

The application was developed to demonstrate an end-to-end machine learning workflow—from data preprocessing and model training to deployment-ready API development and an interactive user interface.

---

## Features

### Machine Learning

- Logistic Regression classifier trained on the IMDB Movie Reviews dataset.
- TF-IDF vectorization for text feature extraction.
- Automated text preprocessing pipeline.
- Confidence score for every prediction.
- Probability distribution for Positive and Negative classes.

### Backend

- FastAPI REST API.
- Single review prediction endpoint.
- Bulk CSV prediction endpoint.
- Background task processing.
- Real-time progress tracking.
- ETA estimation.
- CSV result download.
- Job cancellation support.
- Robust exception handling.

### Frontend

- Responsive React interface.
- Single review prediction.
- CSV upload support.
- Live progress bar.
- ETA display.
- Summary statistics.
- Download processed CSV.
- Clean modern UI.

---

## Technology Stack

### Frontend

- React.js
- JavaScript
- HTML5
- CSS3
- Axios
- Vite

### Backend

- FastAPI
- Uvicorn
- Pydantic
- Python

### Machine Learning

- Scikit-learn
- Logistic Regression
- TF-IDF Vectorizer
- Pandas
- NumPy
- NLTK
- BeautifulSoup
- Joblib

### Dataset

- IMDB Movie Reviews Dataset
- 50,000 labelled movie reviews

---

## Project Highlights

- Full-stack Machine Learning Application
- Real-time Sentiment Prediction
- Batch CSV Analysis
- Background Processing
- Downloadable Reports
- RESTful API Architecture
- Production-ready Folder Structure
- Modular Codebase
- Deployment Ready

---

## Project Structure

```text
Sentio - Sentiment Analysis/
├── Backend/
│   ├── __init__.py
│   ├── main.py
│   └── requirements.txt
│
├── Dataset/
│   ├── IMDB_Dataset.csv
│   └── IMDB_Cleaned.csv
│
├── Frontend/
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── Models/
│   ├── sentiment_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── src/
│   ├── predict.py
│   ├── prepare_dataset.py
│   ├── preprocessing.py
│   ├── train.py
│   └── utils.py
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## Getting Started

### Prerequisites

Ensure the following software is installed on your system:

- Python 3.10 or later
- Node.js 18 or later
- npm
- Git

---

## Clone the Repository

```bash
git clone https://github.com/Abhay3006/Sentio-Sentiment-Analysis.git
```

Move into the project directory:

```bash
cd Sentio-Sentiment-Analysis
```

---

# Backend Setup

Navigate to the backend folder.

```bash
cd Backend
```

Create a virtual environment.

### Windows

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```cmd
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install the required dependencies.

```bash
pip install -r requirements.txt
```

Start the FastAPI server.

```bash
uvicorn main:app --reload
```

The backend will be available at:

```
http://127.0.0.1:8000
```

Swagger API Documentation:

```
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Open a new terminal.

Navigate to the frontend folder.

```bash
cd Frontend
```

Install dependencies.

```bash
npm install
```

Run the development server.

```bash
npm run dev
```

The frontend will be available at:

```
http://localhost:5173
```

---

## Running the Application

1. Start the FastAPI backend.
2. Start the React frontend.
3. Open the application in your browser.
4. Enter a movie review or upload a CSV file.
5. View predictions in real time.
6. Download the processed CSV file.

---

## Input Format

### Single Prediction

Enter any movie review as plain text.

Example:

```text
This movie was absolutely amazing with brilliant acting.
```

---

### CSV Prediction

Upload a CSV file containing a column named:

```text
review
```

Example:

| review |
|---------|
| Amazing movie |
| Worst film ever |
| Highly recommended |

---

## Output

For each review, Sentio predicts:

- Sentiment
- Confidence Score
- Positive Probability
- Negative Probability

Bulk prediction additionally provides:

- Total Reviews
- Positive Reviews
- Negative Reviews
- Downloadable CSV Report

---

## API Endpoints

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
|  GET   |   `/`    | Verify that the API is running |

---

### Predict Sentiment

| Method | Endpoint |
|--------|----------|
| POST | `/predict` |

Predicts the sentiment of a single movie review.

#### Request

```json
{
    "review": "This movie was absolutely fantastic!"
}
```

#### Response

```json
{
    "sentiment": "Positive",
    "confidence": 98.74,
    "positive_probability": 0.9874,
    "negative_probability": 0.0126
}
```

---

### Bulk CSV Prediction

| Method | Endpoint |
|--------|----------|
|  POST  | `/predict-csv` |

Uploads a CSV file and starts background sentiment analysis.

---

### Progress Tracking

| Method | Endpoint |
|--------|----------|
|  GET   | `/progress` |

Returns:

- Processing progress
- Percentage completed
- Estimated remaining time
- Current processing status

---

### Download Results

| Method | Endpoint |
|--------|----------|
|  GET   | `/download` |

Downloads the processed CSV file containing predictions.

---

### Cancel Processing

| Method | Endpoint |
|--------|----------|
|  POST  | `/cancel` |

Cancels an ongoing CSV prediction task.

---

# Machine Learning Workflow

The sentiment analysis pipeline follows these stages:

### 1. Data Collection

- IMDB Movie Reviews Dataset
- 50,000 labelled movie reviews

### 2. Data Preprocessing

The preprocessing pipeline performs:

- Remove duplicate records
- Remove HTML tags
- Convert text to lowercase
- Remove URLs
- Expand contractions
- Remove punctuation
- Remove extra whitespace
- Remove stopwords
- Lemmatization

---

### 3. Feature Engineering

The cleaned text is converted into numerical vectors using:

- TF-IDF Vectorization

This transforms textual data into machine-readable features while preserving the importance of words.

---

### 4. Model Training

Model used:

- Logistic Regression

Training pipeline:

- Train-Test Split
- TF-IDF Feature Extraction
- Model Training
- Performance Evaluation
- Model Serialization using Joblib

---

### 5. Inference Pipeline

During prediction:

1. User submits text.
2. Text is preprocessed.
3. TF-IDF vector is generated.
4. Logistic Regression predicts sentiment.
5. Confidence scores are calculated.
6. Results are returned through the FastAPI API.

---

## Model Performance

The trained Logistic Regression model achieved the following performance on the test dataset:

| Metric | Score |
|--------|------:|
| Accuracy | 88.51% |
| Precision | 87.63% |
| Recall | 89.79% |
| F1 Score | 88.70% |

---

# Screenshots

> Screenshots will be added after deployment.

## Home Page

```
(Add Screenshot Here)
```

---

## Single Review Prediction

```
(Add Screenshot Here)
```

---

## CSV Upload

```
(Add Screenshot Here)
```

---

## Real-Time Progress Tracking

```
(Add Screenshot Here)
```

---

## Prediction Results

```
(Add Screenshot Here)
```

---

## Download Processed CSV

```
(Add Screenshot Here)
```

---

## Future Enhancements

The following features are planned for future releases:

- Support for multilingual sentiment analysis
- Additional sentiment classes (e.g., Neutral)
- Interactive analytics dashboard
- User authentication and prediction history
- Docker containerization
- CI/CD pipeline using GitHub Actions
- Cloud deployment with monitoring and logging
- Support for larger datasets and asynchronous job queues
- Model comparison with advanced deep learning architectures (e.g., LSTM, BERT)

---

## Contributing

Contributions, issues, and feature requests are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for more details.

---

## Author

**Abhayrajsingh Bopche**

- **GitHub:** https://github.com/Abhay3006
- **LinkedIn:** https://www.linkedin.com/in/abhayrajsingh-bopche

---

## Acknowledgements

Special thanks to the open-source community and the developers of the following tools and libraries:

- Python
- FastAPI
- React
- Scikit-learn
- Pandas
- NumPy
- NLTK
- BeautifulSoup
- Joblib
- Vite

The IMDB Movie Reviews Dataset was used for training and evaluating the sentiment analysis model.
Link: https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews

---

<div align="center">

**⭐ If you found this project useful, consider giving it a star on GitHub! ⭐**

</div>