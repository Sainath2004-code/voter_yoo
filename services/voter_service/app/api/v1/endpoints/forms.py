from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class Form6Request(BaseModel):
    full_name: str
    father_name: str
    dob: str
    gender: str
    aadhaar_last4: str
    state_code: str
    district_code: str
    constituency: str
    pincode: str

class Form7Request(BaseModel):
    epic_number: str
    reason: str # death, shifted, duplicate
    proof_document_url: Optional[str]

class Form8Request(BaseModel):
    epic_number: str
    fields_to_correct: List[str] # ["name", "dob", "address"]
    new_values: dict

@router.post("/form-6")
async def submit_form_6(request: Form6Request):
    """Enrollment of new voter"""
    return {"message": "Form 6 submitted successfully", "reference_id": "ECI-F6-9921"}

@router.post("/form-7")
async def submit_form_7(request: Form7Request):
    """Deletion or objection to inclusion"""
    return {"message": "Form 7 submitted successfully", "reference_id": "ECI-F7-1102"}

@router.post("/form-8")
async def submit_form_8(request: Form8Request):
    """Correction of entries or shifting"""
    return {"message": "Form 8 submitted successfully", "reference_id": "ECI-F8-4432"}
