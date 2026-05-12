from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.services.task_service import TaskService
from shared.models.user import User, UserRole
from pydantic import BaseModel

router = APIRouter()

class TaskProcessRequest(BaseModel):
    action: str # approve, reject
    comments: str = None
    payload: dict = None

@router.get("/my-tasks")
def list_my_tasks(
    status: str = "pending",
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    List all pending tasks for the current officer.
    """
    tasks = TaskService.get_officer_tasks(db, officer_id=current_user.id, status=status)
    return tasks

@router.post("/{task_id}/process")
def process_task(
    task_id: str,
    request: TaskProcessRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Approve or Reject a verification task.
    """
    try:
        task = TaskService.process_task(
            db, 
            task_id=task_id, 
            officer_id=current_user.id, 
            action=request.action, 
            comments=request.comments,
            payload=request.payload
        )
        return {"status": "success", "task_id": task.id, "new_status": task.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
