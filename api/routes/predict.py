from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
from api.services.model_loader import load_model, EXPECTED_FEATURES

router = APIRouter()

model = load_model()

class PredictionInput(BaseModel):
    features: List[float]

@router.post("/predict")
def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    if len(input_data.features) != EXPECTED_FEATURES:
        raise HTTPException(
            status_code=400,
            detail=f"Model expects {EXPECTED_FEATURES} features, received {len(input_data.features)}"
        )

    try:
        input_df = pd.DataFrame([input_data.features])
        prediction = model.predict(input_df)[0]
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
