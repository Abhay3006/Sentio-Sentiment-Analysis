import pandas as pd
import time

from preprocessing import preprocess_text
from utils import format_time

def main():
    # Preprocessing Time Starts
    start_time = time.time()

    # Read CSV File
    df = pd.read_csv("../Dataset/IMDB_Dataset.csv")
    print(f"Original Dataset Shape: {df.shape}")

    # Delete Duplicate Rows
    print(f"Duplicate Rows: ", df.duplicated().sum())
    df = df.drop_duplicates().copy()
    print("Dataset Shape After Removing Duplicates:", df.shape)
    print(f"Duplicate Rows:", df.duplicated().sum())

    #Showing Review 1 Before Preprocessing
    print("\nOriginal Review:")
    print(df["review"].iloc[0])

    #Applying Preprocessing Pipeline
    df["review"] = df["review"].apply(preprocess_text)

    #Showing One Review 1 After Preprocessing
    print("\nPreprocessed Review:")
    print(df["review"].iloc[0])

    # Save Cleaned Dataset
    df.to_csv("../Dataset/IMDB_Cleaned.csv", index=False)

    #Confirmation Message
    print("Dataset preprocessing completed successfully!")
    print("Cleaned dataset saved as: ../Dataset/IMDB_Cleaned.csv")
    print(f"Cleaned Dataset Shape: {df.shape}")

    #Execution Time Ends
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nDataset Preprocessing Time: {format_time(elapsed_time)}")

if __name__ == "__main__":
    main()