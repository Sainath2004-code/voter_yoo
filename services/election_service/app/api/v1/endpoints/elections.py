from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.services.election_service import ElectionService
from shared.models.election import ElectionStatus, ElectionType
from shared.models.user import User, UserRole
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class ElectionCreate(BaseModel):
    title: str
    type: ElectionType
    notification_date: date

@router.post("/", response_model=dict)
def create_election(
    election_in: ElectionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RoleChecker([UserRole.CEC, UserRole.EC]))
):
    """
    Create a new election notification. Only CEC/EC can initiate.
    """
    election = ElectionService.create_election(
        db, title=election_in.title, election_type=election_in.type, notification_date=election_in.notification_date
    )
    return {"id": election.id, "status": election.status}

@router.post("/{election_id}/transition")
def transition_election(
    election_id: str,
    new_status: ElectionStatus,
    comments: str = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RoleChecker([UserRole.CEC, UserRole.EC, UserRole.CEO]))
):
    """
    Transition election to the next stage (e.g., NOMINATION, POLLING).
    """
    try:
        election = ElectionService.transition_status(
            db, election_id=election_id, new_status=new_status, officer_id=current_user.id, comments=comments
        )
        return {"id": election.id, "new_status": election.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
