from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.api import deps
from app.services.grievance_service import GrievanceService
from shared.models.grievance import GrievanceCategory, GrievanceStatus
from shared.models.user import User

router = APIRouter()


class GrievanceSubmit(BaseModel):
    category: GrievanceCategory
    subject: str
    description: str
    state_id: str
    district_id: Optional[str] = None
    ac_id: Optional[str] = None
    priority: str = "medium"
    attachment_urls: Optional[List[str]] = None


class GrievanceTransition(BaseModel):
    new_status: GrievanceStatus
    notes: Optional[str] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_grievance(
    body: GrievanceSubmit,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Citizen submits a grievance. System auto-assigns the appropriate officer.
    """
    grievance = GrievanceService.submit(
        db,
        user_id=current_user.id,
        category=body.category,
        subject=body.subject,
        description=body.description,
        state_id=body.state_id,
        district_id=body.district_id,
        ac_id=body.ac_id,
        priority=body.priority,
        attachment_urls=body.attachment_urls,
    )
    return {
        "id": grievance.id,
        "status": grievance.status,
        "sla_deadline": grievance.sla_deadline,
        "assigned_officer_id": grievance.assigned_officer_id,
    }


@router.get("/my")
def list_my_grievances(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Citizen views their own grievances."""
    from shared.models.grievance import Grievance
    grievances = db.query(Grievance).filter(Grievance.user_id == current_user.id).all()
    return grievances


@router.post("/{grievance_id}/transition")
def transition_grievance(
    grievance_id: str,
    body: GrievanceTransition,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Officer advances the grievance status."""
    try:
        g = GrievanceService.transition(
            db,
            grievance_id=grievance_id,
            new_status=body.new_status,
            officer_id=current_user.id,
            notes=body.notes,
        )
        return {"id": g.id, "new_status": g.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
