from sqlalchemy.orm import Session
from sqlalchemy import func, case, text
from shared.models.voter import VoterProfile
from shared.models.voter_application import VoterApplication, ApplicationStatus
from shared.models.election import Election, ElectionStatus
from shared.models.grievance import Grievance, GrievanceStatus
from shared.models.audit import AuditLog


class AnalyticsService:
    """
    Real SQL aggregation queries — no mock data.
    Each method returns a dict ready to be serialised.
    """

    # ------------------------------------------------------------------ #
    #  National / State summary                                            #
    # ------------------------------------------------------------------ #
    @staticmethod
    def national_overview(db: Session) -> dict:
        total_voters = db.query(func.count(VoterProfile.id)).scalar() or 0

        # Gender breakdown
        gender_rows = (
            db.query(VoterProfile.gender, func.count(VoterProfile.id))
            .group_by(VoterProfile.gender)
            .all()
        )
        gender_breakdown = {row[0]: row[1] for row in gender_rows}

        # Application funnel
        app_rows = (
            db.query(VoterApplication.status, func.count(VoterApplication.id))
            .group_by(VoterApplication.status)
            .all()
        )
        application_funnel = {row[0]: row[1] for row in app_rows}

        # Active elections
        active_elections = (
            db.query(func.count(Election.id))
            .filter(Election.status.notin_([ElectionStatus.ARCHIVED]))
            .scalar() or 0
        )

        # Pending grievances (not resolved/closed)
        pending_grievances = (
            db.query(func.count(Grievance.id))
            .filter(Grievance.status.notin_([GrievanceStatus.RESOLVED, GrievanceStatus.CLOSED]))
            .scalar() or 0
        )

        return {
            "total_registered_voters": total_voters,
            "gender_breakdown": gender_breakdown,
            "application_funnel": application_funnel,
            "active_elections": active_elections,
            "pending_grievances": pending_grievances,
        }

    # ------------------------------------------------------------------ #
    #  State-level drill-down                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def state_summary(db: Session, state_id: str) -> dict:
        total = (
            db.query(func.count(VoterProfile.id))
            .filter(VoterProfile.state_id == state_id)
            .scalar() or 0
        )
        pending_apps = (
            db.query(func.count(VoterApplication.id))
            .filter(
                VoterApplication.state_id == state_id,
                VoterApplication.status == ApplicationStatus.BLO_VERIFICATION,
            )
            .scalar() or 0
        )
        approved_apps = (
            db.query(func.count(VoterApplication.id))
            .filter(
                VoterApplication.state_id == state_id,
                VoterApplication.status == ApplicationStatus.APPROVED,
            )
            .scalar() or 0
        )
        rejected_apps = (
            db.query(func.count(VoterApplication.id))
            .filter(
                VoterApplication.state_id == state_id,
                VoterApplication.status == ApplicationStatus.REJECTED,
            )
            .scalar() or 0
        )
        return {
            "state_id": state_id,
            "total_voters": total,
            "pending_verifications": pending_apps,
            "approved_registrations": approved_apps,
            "rejected_registrations": rejected_apps,
        }

    # ------------------------------------------------------------------ #
    #  District drill-down                                                 #
    # ------------------------------------------------------------------ #
    @staticmethod
    def district_summary(db: Session, district_id: str) -> dict:
        total = (
            db.query(func.count(VoterProfile.id))
            .filter(VoterProfile.district_id == district_id)
            .scalar() or 0
        )
        grievance_count = (
            db.query(func.count(Grievance.id))
            .filter(Grievance.district_id == district_id)
            .scalar() or 0
        )
        return {
            "district_id": district_id,
            "total_voters": total,
            "grievance_count": grievance_count,
        }

    # ------------------------------------------------------------------ #
    #  Audit activity (rolling 7 days)                                     #
    # ------------------------------------------------------------------ #
    @staticmethod
    def recent_audit_activity(db: Session, limit: int = 50) -> list:
        rows = (
            db.query(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "action": r.action,
                "resource": r.resource,
                "actor_id": r.actor_id,
                "timestamp": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
