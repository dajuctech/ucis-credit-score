import os
import joblib

MODEL_PATH = os.path.join("ml", "models", "model.pkl")
EXPECTED_FEATURES = 18  # Manually set or load dynamically if needed

def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded from: {MODEL_PATH}")
        return model
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return None
