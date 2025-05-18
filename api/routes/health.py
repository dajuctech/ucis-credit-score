from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Utility"])

@router.get("/")
def health_check():
    return {"status": "ok"}
