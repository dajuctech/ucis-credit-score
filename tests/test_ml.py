import os
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

def test_model_loading():
    model_path = os.path.join("ml", "models", "model.pkl")
    assert os.path.exists(model_path), "Model file not found."
    model = joblib.load(model_path)
    assert model is not None, "Model failed to load."

def test_model_prediction_shape():
    model = joblib.load(os.path.join("ml", "models", "model.pkl"))
    df = pd.read_csv("data/processed/credit_data_cleaned.csv")

    # Reconstruct target
    if all(col in df.columns for col in ['Credit_Score_Poor', 'Credit_Score_Standard']):
        y = df.apply(lambda row: 'Poor' if row['Credit_Score_Poor'] == 1 else ('Standard' if row['Credit_Score_Standard'] == 1 else 'Good'), axis=1)
        X = df.drop(columns=['Credit_Score_Poor', 'Credit_Score_Standard'])
        X = X.select_dtypes(include=["number"])
        preds = model.predict(X[:100])
        assert len(preds) == 100, "Prediction length mismatch"
