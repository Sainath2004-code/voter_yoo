from sqlalchemy.orm import Session
from shared.models.election import Election, ElectionStatus, ElectionType
from shared.models.workflow import ApprovalHistory
import uuid
from datetime import date

class ElectionService:
    @staticmethod
    def create_election(db: Session, title: str, election_type: ElectionType, notification_date: date):
        election = Election(
            id=str(uuid.uuid4()),
            title=title,
            type=election_type,
            status=ElectionStatus.NOTIFICATION,
            notification_date=notification_date
        )
        db.add(election)
        db.commit()
        db.refresh(election)
        return election

    @staticmethod
    def transition_status(db: Session, election_id: str, new_status: ElectionStatus, officer_id: str, comments: str = None):
        election = db.query(Election).filter(Election.id == election_id).first()
        if not election:
            raise ValueError("Election not found")
        
        # Basic state machine validation
        valid_transitions = {
            ElectionStatus.NOTIFICATION: [ElectionStatus.NOMINATION],
            ElectionStatus.NOMINATION: [ElectionStatus.SCRUTINY],
            ElectionStatus.SCRUTINY: [ElectionStatus.WITHDRAWAL],
            ElectionStatus.WITHDRAWAL: [ElectionStatus.CAMPAIGN],
            ElectionStatus.CAMPAIGN: [ElectionStatus.POLLING],
            ElectionStatus.POLLING: [ElectionStatus.COUNTING],
            ElectionStatus.COUNTING: [ElectionStatus.RESULTS],
            ElectionStatus.RESULTS: [ElectionStatus.ARCHIVED]
        }
        
        if new_status not in valid_transitions.get(election.status, []):
            raise ValueError(f"Invalid transition from {election.status} to {new_status}")

        # Audit history
        history = ApprovalHistory(
            entity_id=election.id,
            entity_type="election",
            action="status_transition",
            previous_status=election.status,
            new_status=new_status,
            officer_id=officer_id,
            comments=comments
        )
        db.add(history)
        
        election.status = new_status
        db.commit()
        db.refresh(election)
        return election
