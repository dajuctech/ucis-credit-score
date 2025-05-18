from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import pandas as pd
from api.services.model_loader import load_model, EXPECTED_FEATURES

router = APIRouter()
model = load_model()

# ✅ Updated with proper example
class PredictionInput(BaseModel):
    features: List[float] = Field(
        ...,
        example=[5000, 3, 2, 1.5, 5, 0.2, 12, 250.0, 50.0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
    )

@router.post("/predict")
def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    if len(input_data.features) != EXPECTED_FEATURES:
        raise HTTPException(status_code=400, detail=f"Model expects {EXPECTED_FEATURES} features.")
    try:
        input_df = pd.DataFrame([input_data.features])
        prediction = model.predict(input_df)[0]
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
