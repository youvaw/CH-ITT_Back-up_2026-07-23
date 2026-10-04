from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["dashboard_api"])

@router.get("/status")
async def get_dashboard_status():
    return {
        "running": True,
        "host": "127.0.0.1",
        "port": 8000
    }

