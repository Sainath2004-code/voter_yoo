from fastapi import APIRouter
from app.api.v1.endpoints import voter

api_router = APIRouter()
api_router.include_router(voter.router, prefix="/voters", tags=["voters"])
