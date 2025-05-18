from fastapi import FastAPI
from api.routes.predict import router as predict_router

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(predict_router)
