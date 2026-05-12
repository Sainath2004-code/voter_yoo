from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from shared.models.election import Election, ElectionStatus
from datetime import date

class ElectionWorkflowManager:
    """
    Manages state transitions for elections based on ECI lifecycle rules.
    """
    
    # Valid transitions map
    VALID_TRANSITIONS = {
        ElectionStatus.NOTIFICATION: [ElectionStatus.NOMINATION],
        ElectionStatus.NOMINATION: [ElectionStatus.SCRUTINY, ElectionStatus.WITHDRAWAL],
        ElectionStatus.SCRUTINY: [ElectionStatus.WITHDRAWAL, ElectionStatus.CAMPAIGN],
        ElectionStatus.WITHDRAWAL: [ElectionStatus.CAMPAIGN],
        ElectionStatus.CAMPAIGN: [ElectionStatus.POLLING],
        ElectionStatus.POLLING: [ElectionStatus.COUNTING],
        ElectionStatus.COUNTING: [ElectionStatus.RESULTS],
        ElectionStatus.RESULTS: [ElectionStatus.ARCHIVED],
        ElectionStatus.ARCHIVED: []
    }

    @staticmethod
    def transition_to(db: Session, election_id: str, next_status: ElectionStatus) -> Election:
        election = db.query(Election).filter(Election.id == election_id).first()
        if not election:
            raise HTTPException(status_code=404, detail="Election not found")

        current_status = election.status
        
        # Validate transition
        if next_status not in ElectionWorkflowManager.VALID_TRANSITIONS.get(current_status, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid transition: Cannot move from {current_status.value} to {next_status.value}"
            )

        # Business Logic Validations
        if next_status == ElectionStatus.POLLING and not election.polling_date:
            raise HTTPException(status_code=400, detail="Cannot start polling without a defined date.")
            
        if next_status == ElectionStatus.RESULTS and election.polling_date > date.today():
             raise HTTPException(status_code=400, detail="Cannot declare results before polling is complete.")

        # Execute transition
        election.status = next_status
        db.commit()
        db.refresh(election)
        
        # Log transition in Audit (to be implemented in Phase 4)
        
        return election

    @staticmethod
    def get_allowed_actions(status: ElectionStatus) -> List[ElectionStatus]:
        return ElectionWorkflowManager.VALID_TRANSITIONS.get(status, [])
