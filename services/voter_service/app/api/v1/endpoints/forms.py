from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api import deps
from app.services.registration_service import RegistrationService
from shared.models.voter_application import ApplicationType
from shared.models.user import User

router = APIRouter()

class Form6Request(BaseModel):
    first_name: str
    last_name: str
    father_name: str
    date_of_birth: str
    gender: str
    aadhaar_last4: str
    state_id: str
    district_id: str
    ac_id: str
    booth_id: str
    pincode: str
    address_line1: str

@router.post("/form-6")
def submit_form_6(
    request: Form6Request, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Enrollment of new voter"""
    application = RegistrationService.submit_form(
        db, 
        current_user.id, 
        ApplicationType.FORM_6, 
        request.model_dump()
    )
    return {
        "message": "Form 6 submitted successfully", 
        "application_id": application.id,
        "status": application.status
    }

@router.post("/form-7")
def submit_form_7(
    epic_number: str, 
    reason: str, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Deletion or objection to inclusion"""
    # Logic for Form 7...
    return {"message": "Form 7 submitted successfully"}

@router.post("/form-8")
def submit_form_8(
    epic_number: str, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Correction of entries or shifting"""
    # Logic for Form 8...
    return {"message": "Form 8 submitted successfully"}
