import os
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
RAW_PATH = os.path.join(ROOT_DIR, "data", "raw", "credit_data.csv")
CLEANED_PATH = os.path.join(ROOT_DIR, "data", "processed", "credit_data_cleaned.csv")

def load_data(path):
    df = pd.read_csv(path, low_memory=False)
    print(f"✅ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def preprocess_data(df):
    # 1. Drop duplicates
    df.drop_duplicates(inplace=True)

    # 2. Drop irrelevant columns if present
    drop_cols = ['ID', 'Name', 'SSN']  # Add/remove based on your dataset
    df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)

    # 3. Fix data types
    for col in df.columns:
        if 'Date' in col or 'date' in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 4. Convert time periods (e.g., "2 years and 3 months") into months
    def convert_period(value):
        if pd.isna(value):
            return None
        value = str(value).lower()
        years = 0
        months = 0
        if 'year' in value:
            parts = value.split('year')[0].strip()
            years = int(parts) if parts.isdigit() else 0
        if 'month' in value:
            months = int(''.join(filter(str.isdigit, value.split('month')[0].split()[-1]))) if 'month' in value else 0
        return years * 12 + months

    if 'Credit_History_Age' in df.columns:
        df['Credit_History_Age'] = df['Credit_History_Age'].apply(convert_period)

    # 5. Fill missing numeric values
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    imputer = SimpleImputer(strategy='median')
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

    # 6. Encode categorical variables
    categorical_cols = df.select_dtypes(include=['object']).columns
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    return df

def save_data(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Cleaned data saved to: {path}")

if __name__ == "__main__":
    df_raw = load_data(RAW_PATH)
    df_clean = preprocess_data(df_raw)
    save_data(df_clean, CLEANED_PATH)
