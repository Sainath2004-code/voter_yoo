from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.grievance import Grievance, GrievanceStatus

class GrievanceService:
    """
    Manages grievance lifecycle, SLA calculation, and assignments.
    """
    
    # SLA mapping (Category: Days)
    SLA_RULES = {
        "Voter List": 7,
        "Booth Issue": 3,
        "MCC Violation": 2,
        "General": 10
    }

    @staticmethod
    def create_grievance(db: Session, user_id: str, data: dict) -> Grievance:
        category = data.get("category", "General")
        sla_days = GrievanceService.SLA_RULES.get(category, 10)
        
        sla_deadline = datetime.now(timezone.utc) + timedelta(days=sla_days)
        
        grievance = Grievance(
            user_id=user_id,
            category=category,
            subject=data.get("subject"),
            description=data.get("description"),
            scope_type=data.get("scope_type"),
            scope_id=data.get("scope_id"),
            sla_deadline=sla_deadline
        )
        
        db.add(grievance)
        db.commit()
        db.refresh(grievance)
        return grievance

    @staticmethod
    def assign_officer(db: Session, grievance_id: str, officer_id: str) -> Grievance:
        grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
        if not grievance:
            raise HTTPException(status_code=404, detail="Grievance not found")
            
        grievance.assigned_officer_id = officer_id
        grievance.status = GrievanceStatus.ASSIGNED
        db.commit()
        return grievance

    @staticmethod
    def resolve_grievance(db: Session, grievance_id: str, details: str) -> Grievance:
        grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
        if not grievance:
            raise HTTPException(status_code=404, detail="Grievance not found")
            
        grievance.resolution_details = details
        grievance.status = GrievanceStatus.RESOLVED
        db.commit()
        return grievance
