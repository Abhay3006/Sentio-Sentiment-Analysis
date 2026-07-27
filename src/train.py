import pandas as pd
import joblib
import time

from utils import format_time, format_percentage
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


def main():
    # Read cleaned dataset
    df = pd.read_csv("../Dataset/IMDB_Cleaned.csv")

    # Verify dataset
    print("Dataset Shape:", df.shape)
    print("\nColumns:")
    print(df.columns)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nClass Distribution:")
    print(df["sentiment"].value_counts())

    # Split dataset into features (X) and labels (y)
    X = df["review"]
    y = df["sentiment"]

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Verify train-test split
    print("\nTraining Set Shape:", X_train.shape)
    print("Testing Set Shape:", X_test.shape)

    print("\nTraining Labels Distribution:")
    print(y_train.value_counts())

    print("\nTesting Labels Distribution:")
    print(y_test.value_counts())

    # Convert text into TF-IDF feature vectors
    tfidf = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True
    )

    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    print("\nTF-IDF Training Shape:", X_train_tfidf.shape)
    print("TF-IDF Testing Shape:", X_test_tfidf.shape)

    # Define hyperparameter grid
    param_grid = {
    "C": [0.001, 0.01, 0.1, 1, 10, 100],
    "solver": ["liblinear", "lbfgs"],
    "penalty": ["l2"]
    }

    # Create base Logistic Regression model
    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    # Perform hyperparameter tuning using Grid Search with 5-fold cross validation
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=10,
        scoring="accuracy",
        n_jobs=-1
    )

    # Train Grid Search and measure training time
    start_time = time.time()

    grid_search.fit(X_train_tfidf, y_train)

    end_time = time.time()

    best_model = grid_search.best_estimator_

    elapsed_time = end_time - start_time
    print(f"\nTraining Time: {format_time(elapsed_time)}")
    print("Model Trained Successfully.")

    print("\nBest Parameters:")
    for key, value in grid_search.best_params_.items():
        print(f"{key}: {value}")

    print(f"\nBest Cross Validation Accuracy: {format_percentage(grid_search.best_score_)}")

    # Make predictions on the training and testing sets
    y_train_pred = best_model.predict(X_train_tfidf)
    y_test_pred = best_model.predict(X_test_tfidf)

    print("\nFirst 10 Predictions:")
    print(y_test_pred[:10])

    print("\nActual Labels:")
    print(y_test.iloc[:10].values)

    # Calculate evaluation metrics
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)

    precision = precision_score(
        y_test,
        y_test_pred,
        pos_label="positive"
    )

    recall = recall_score(
        y_test,
        y_test_pred,
        pos_label="positive"
    )

    f1 = f1_score(
        y_test,
        y_test_pred,
        pos_label="positive"
    )

    # Display model performance
    print(f"\nTraining Accuracy: {format_percentage(train_accuracy)}")
    print(f"Testing Accuracy: {format_percentage(test_accuracy)}")
    print(f"\nPrecision: {format_percentage(precision)}")
    print(f"Recall: {format_percentage(recall)}")
    print(f"F1 Score: {format_percentage(f1)}")

    # Generate confusion matrix
    cm = confusion_matrix(y_test, y_test_pred)

    print("\nConfusion Matrix:")
    print(cm)

    # Generate classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_test_pred))

    # Save Model and TF-IDF Vectorizer
    joblib.dump(best_model, "../Models/sentiment_model.pkl")
    joblib.dump(tfidf, "../Models/tfidf_vectorizer.pkl")

    print("\nModel Saved Successfully.")
    print("TF-IDF Vectorizer Saved Successfully.")


if __name__ == "__main__":
    main()