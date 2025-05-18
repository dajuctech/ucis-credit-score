from fastapi import FastAPI
from api.routes.predict import router as predict_router

app = FastAPI(
    title="Credit Score Prediction API",
    version="1.0.0",
    description="API to predict creditworthiness using financial history."
)

# ✅ Health endpoint - must be inside `main.py` and tied to `app`
@app.get("/health", tags=["Utility"])
def health_check():
    return {"status": "ok"}

# ✅ Mount the prediction route from /api/routes/predict.py
#app.include_router(health_router)
app.include_router(predict_router, tags=["Prediction"])
