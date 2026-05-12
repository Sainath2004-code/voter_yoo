from sqlalchemy.orm import Session
from sqlalchemy import func, and_, text
from shared.models.grievance import Grievance, GrievanceStatus, GrievanceCategory
from shared.models.user import User, UserRole
from datetime import datetime, timedelta, timezone
import uuid

# --- SLA in hours per priority ---
SLA_HOURS = {"low": 120, "medium": 48, "high": 24, "emergency": 4}

# --- Auto-assignment role per category ---
CATEGORY_ROLE_MAP = {
    GrievanceCategory.VOTER_REGISTRATION: UserRole.BLO,
    GrievanceCategory.POLLING_BOOTH: UserRole.DEO,
    GrievanceCategory.CANDIDATE_CONDUCT: UserRole.RO,
    GrievanceCategory.TECHNICAL_ISSUE: UserRole.CEO,
    GrievanceCategory.FRAUD_REPORT: UserRole.DEO,
}


class GrievanceService:
    @staticmethod
    def submit(
        db: Session,
        user_id: str,
        category: GrievanceCategory,
        subject: str,
        description: str,
        state_id: str,
        district_id: str = None,
        ac_id: str = None,
        priority: str = "medium",
        attachment_urls: list = None,
    ) -> Grievance:
        """
        Citizen submits a grievance. Auto-assigns an officer and sets SLA.
        """
        sla_hours = SLA_HOURS.get(priority, 48)
        sla_deadline = datetime.now(timezone.utc) + timedelta(hours=sla_hours)

        # Find the appropriate officer for auto-assignment
        target_role = CATEGORY_ROLE_MAP.get(category, UserRole.DEO)
        assigned_officer = (
            db.query(User)
            .filter(
                User.role == target_role,
                User.is_active == True,
                # Match on district scope if available, else state
                User.scope_id == (district_id or state_id),
            )
            .first()
        )

        grievance = Grievance(
            id=str(uuid.uuid4()),
            user_id=user_id,
            category=category,
            status=GrievanceStatus.SUBMITTED,
            subject=subject,
            description=description,
            state_id=state_id,
            district_id=district_id,
            ac_id=ac_id,
            priority=priority,
            sla_deadline=sla_deadline,
            attachment_urls=attachment_urls or [],
            assigned_officer_id=assigned_officer.id if assigned_officer else None,
        )
        db.add(grievance)

        # If auto-assigned, advance status
        if assigned_officer:
            grievance.status = GrievanceStatus.ASSIGNED

        db.commit()
        db.refresh(grievance)
        return grievance

    @staticmethod
    def transition(
        db: Session,
        grievance_id: str,
        new_status: GrievanceStatus,
        officer_id: str,
        notes: str = None,
    ) -> Grievance:
        """Officer advances the grievance workflow state."""
        valid_transitions = {
            GrievanceStatus.SUBMITTED: [GrievanceStatus.CATEGORIZED, GrievanceStatus.ASSIGNED],
            GrievanceStatus.CATEGORIZED: [GrievanceStatus.ASSIGNED],
            GrievanceStatus.ASSIGNED: [GrievanceStatus.INVESTIGATING],
            GrievanceStatus.INVESTIGATING: [GrievanceStatus.RESOLVED],
            GrievanceStatus.RESOLVED: [GrievanceStatus.CLOSED],
        }
        grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
        if not grievance:
            raise ValueError("Grievance not found")
        if new_status not in valid_transitions.get(grievance.status, []):
            raise ValueError(f"Cannot move from {grievance.status} → {new_status}")

        grievance.status = new_status
        if notes:
            grievance.resolution_notes = notes
        db.commit()
        db.refresh(grievance)
        return grievance

    @staticmethod
    def check_sla_breaches(db: Session) -> list:
        """Returns grievances that have breached SLA and are not yet resolved."""
        now = datetime.now(timezone.utc)
        breached = (
            db.query(Grievance)
            .filter(
                Grievance.sla_deadline < now,
                Grievance.status.notin_([GrievanceStatus.RESOLVED, GrievanceStatus.CLOSED]),
            )
            .all()
        )
        return breached
