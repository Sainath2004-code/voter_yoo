from fastapi import APIRouter
from app.api.v1.endpoints import biometrics

api_router = APIRouter()
api_router.include_router(biometrics.router, prefix="/biometrics", tags=["biometrics"])
