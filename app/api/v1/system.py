
from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/status")
async def api_status() -> dict[str, str]:
    return {
        "status": "available",
        "api_version": "v1",
    }
