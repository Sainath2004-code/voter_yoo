from fastapi import APIRouter
from app.api.v1.endpoints import tasks, grievances

api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(grievances.router, prefix="/grievances", tags=["grievances"])
