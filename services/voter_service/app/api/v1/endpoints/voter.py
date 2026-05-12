from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.voter import VoterProfile
from app.schemas.voter import VoterCreate, VoterResponse

router = APIRouter()

@router.post("/register", response_model=VoterResponse)
def register_voter(
    *,
    db: Session = Depends(deps.get_db),
    voter_in: VoterCreate,
    # current_user_id: str = Depends(deps.get_current_user_id) # Should be injected from Gateway or Auth header
) -> Any:
    """
    Register a new voter profile.
    """
    # Check if voter profile already exists for this user
    existing_profile = db.query(VoterProfile).filter(VoterProfile.user_id == voter_in.user_id).first()
    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="A voter profile already exists for this user.",
        )
    
    # Check if national ID already registered
    existing_id = db.query(VoterProfile).filter(VoterProfile.national_id == voter_in.national_id).first()
    if existing_id:
        raise HTTPException(
            status_code=400,
            detail="This National ID is already registered.",
        )
    
    db_obj = VoterProfile(
        user_id=voter_in.user_id,
        first_name=voter_in.first_name,
        last_name=voter_in.last_name,
        date_of_birth=voter_in.date_of_birth,
        gender=voter_in.gender,
        address_line1=voter_in.address_line1,
        address_line2=voter_in.address_line2,
        city=voter_in.city,
        state=voter_in.state,
        zip_code=voter_in.zip_code,
        national_id=voter_in.national_id,
        constituency_id=voter_in.constituency_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    # Trigger AI fraud detection event (via Kafka - to be implemented)
    # await producer.send_and_wait("voter_registration_events", {"voter_id": db_obj.id, "action": "created"})
    
    return db_obj
