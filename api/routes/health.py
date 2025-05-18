# api/routes/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Utility"])
def health_check():
    return {"status": "ok"}
