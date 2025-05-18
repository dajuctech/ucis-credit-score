from fastapi import FastAPI
from api.routes.predict import router as predict_router
from api.routes.health import router as health_router

app = FastAPI(
    title="Credit Score Prediction API",
    version="1.0.0",
    description="API to predict creditworthiness using financial history."
)

@app.get("/", tags=["Utility"])
def root():
    return {"message": "Welcome to the Credit Score Prediction API"}

app.include_router(health_router)
app.include_router(predict_router)
