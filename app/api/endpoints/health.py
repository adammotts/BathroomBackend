from fastapi import APIRouter

router = APIRouter()

@router.get("/health", status_code=200)
async def health_check():
    """Health check endpoint to verify API status"""
    return {"status": "ok", "message": "API is running"}
