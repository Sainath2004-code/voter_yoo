from sqlalchemy.orm import Session
from shared.models.voter_application import VoterApplication, ApplicationType, ApplicationStatus
from shared.models.workflow import VerificationTask, TaskType, TaskPriority
import uuid

class RegistrationService:
    @staticmethod
    def submit_form(db: Session, user_id: str, app_type: ApplicationType, form_data: dict):
        """
        Submits a new voter application and initializes the workflow.
        """
        # 1. Persist Application
        application = VoterApplication(
            id=str(uuid.uuid4()),
            user_id=user_id,
            type=app_type,
            status=ApplicationStatus.SUBMITTED,
            state_id=form_data.get('state_id'),
            district_id=form_data.get('district_id'),
            ac_id=form_data.get('ac_id'),
            booth_id=form_data.get('booth_id'),
            form_data=form_data
        )
        db.add(application)
        db.flush() # Get ID

        # 2. Create Initial Verification Task for BLO
        task = VerificationTask(
            type=TaskType.VOTER_VERIFICATION,
            priority=TaskPriority.MEDIUM,
            entity_id=application.id,
            entity_type="voter_application",
            scope_type="booth",
            scope_id=application.booth_id,
            status="pending"
        )
        db.add(task)
        
        # Update application with task reference
        application.current_task_id = task.id
        application.status = ApplicationStatus.BLO_VERIFICATION
        
        db.commit()

        # --- Fire async notification (non-blocking) ---
        try:
            import sys, os
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../..")))
            from services.notification_service.app.services.dispatcher import NotificationDispatcher
            from shared.models.user import User
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                NotificationDispatcher.voter_application_submitted(
                    email=user.email,
                    phone=getattr(user, "phone", ""),
                    user_id=user_id,
                    application_id=application.id,
                )
        except Exception:
            pass  # Notification failure must never block registration

        return application

    @staticmethod
    def get_application_status(db: Session, application_id: str):
        return db.query(VoterApplication).filter(VoterApplication.id == application_id).first()
