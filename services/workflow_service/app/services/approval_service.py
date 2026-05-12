from sqlalchemy.orm import Session
from app.models.approval import ApprovalHistory, VerificationTask
from shared.models.audit import AuditLog
import uuid

class ApprovalService:
    """
    Handles approval actions, task generation, and escalation logic.
    """

    @staticmethod
    def log_approval(
        db: Session, 
        entity_type: str, 
        entity_id: str, 
        action: str, 
        officer_id: str, 
        comments: str = None
    ) -> ApprovalHistory:
        history = ApprovalHistory(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            performed_by_id=officer_id,
            comments=comments
        )
        db.add(history)
        db.commit()
        return history

    @staticmethod
    def create_verification_task(
        db: Session, 
        entity_type: str, 
        entity_id: str, 
        assigned_role: str, 
        scope_id: str
    ) -> VerificationTask:
        task = VerificationTask(
            entity_type=entity_type,
            entity_id=entity_id,
            assigned_role=assigned_role,
            assigned_scope_id=scope_id
        )
        db.add(task)
        db.commit()
        return task

    @staticmethod
    def escalate_task(db: Session, task_id: str, new_role: str, new_scope_id: str) -> VerificationTask:
        task = db.query(VerificationTask).filter(VerificationTask.id == task_id).first()
        if not task:
            return None
            
        task.assigned_role = new_role
        task.assigned_scope_id = new_scope_id
        task.priority = "urgent"
        db.commit()
        return task
