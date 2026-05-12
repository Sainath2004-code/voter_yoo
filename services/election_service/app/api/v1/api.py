from fastapi import APIRouter
from app.api.v1.endpoints import elections

api_router = APIRouter()
api_router.include_router(elections.router, prefix="/elections", tags=["elections"])
