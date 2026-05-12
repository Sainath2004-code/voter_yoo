from sqlalchemy.orm import Session
from shared.models.workflow import VerificationTask, ApprovalHistory
from shared.models.voter_application import VoterApplication, ApplicationStatus
from shared.models.user import User
import uuid

class TaskService:
    @staticmethod
    def get_officer_tasks(db: Session, officer_id: str, status: str = "pending"):
        return db.query(VerificationTask).filter(
            VerificationTask.assigned_officer_id == officer_id,
            VerificationTask.status == status
        ).all()

    @staticmethod
    def process_task(db: Session, task_id: str, officer_id: str, action: str, comments: str = None, payload: dict = None):
        task = db.query(VerificationTask).filter(VerificationTask.id == task_id).first()
        if not task:
            raise ValueError("Task not found")
        
        if task.assigned_officer_id != officer_id:
            # Check if officer has appropriate scope if not assigned directly
            # For now, we assume direct assignment or scope check in API dependency
            pass

        # Update Task
        task.status = "completed" if action == "approve" else "failed"
        task.comments = comments
        task.verification_payload = payload

        # Update the linked entity (VoterApplication etc.)
        if task.entity_type == "voter_application":
            application = db.query(VoterApplication).filter(VoterApplication.id == task.entity_id).first()
            if application:
                if action == "approve":
                    # Move to next state: ERO Review or Approved
                    application.status = ApplicationStatus.ERO_REVIEW
                else:
                    application.status = ApplicationStatus.REJECTED

        # Record History
        history = ApprovalHistory(
            entity_id=task.entity_id,
            entity_type=task.entity_type,
            action=action,
            previous_status="pending",
            new_status=task.status,
            officer_id=officer_id,
            comments=comments
        )
        db.add(history)
        db.commit()
        return task
