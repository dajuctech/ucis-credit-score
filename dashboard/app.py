import streamlit as st
import pandas as pd
import joblib
import os

# === Load model and get feature names ===
MODEL_PATH = os.path.join("ml", "models", "model.pkl")
DATA_PATH = os.path.join("data", "processed", "credit_data_cleaned.csv")

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# Drop target columns and keep only features
X = df.drop(columns=["Credit_Score_Poor", "Credit_Score_Standard"], errors='ignore')
X = X.select_dtypes(include=["number"])  # use only numeric columns

feature_names = X.columns.tolist()
EXPECTED_FEATURES = len(feature_names)

# === Streamlit UI ===
st.set_page_config(page_title="Credit Score Dashboard", layout="wide")
st.title("📊 Credit Score Prediction Dashboard")

st.sidebar.header("Enter Features")

def get_user_input():
    inputs = {}
    for col in feature_names:
        inputs[col] = st.sidebar.number_input(col, value=0.0)
    return pd.DataFrame([inputs])

input_df = get_user_input()

# === Make Prediction ===
if st.button("Predict"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"Predicted Credit Score: **{prediction}**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")

# === Optional: Show EDA Images ===
st.subheader("📈 EDA Visualizations")
report_dir = "reports"
for img in ["eda_histograms.png", "eda_correlation_heatmap.png", "pca_scatter_plot.png"]:
    path = os.path.join(report_dir, img)
    if os.path.exists(path):
        st.image(path, caption=img.replace("_", " ").title())
