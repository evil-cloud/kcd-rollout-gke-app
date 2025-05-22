from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.business_logic import process_data
from models.schemas import MessageResponse, VersionResponse, HealthResponse
import datetime
from core.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "ok", "service": "gitops-api"}


@router.get("/api/v1/rollout/version", response_model=VersionResponse)
async def get_version():
    return {"version": settings.VERSION}


@router.get("/api/v1/rollout/strategy", response_model=MessageResponse)
async def hello():
    return {"message": f"Version: {settings.ROLLOUT_STRATEGY} utilizando Argo Rollouts!"}


@router.get("/api/v1/rollout/external")
async def fetch_external_data():
    try:
        return process_data()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Fallo en la API externa",
                "status_code": 503,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "message": str(e),
            }
        )