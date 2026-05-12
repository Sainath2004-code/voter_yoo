from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.services.aggregation import AnalyticsService
from shared.models.user import User

router = APIRouter()


@router.get("/national")
def national_overview(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """National summary: voters, applications, elections, grievances."""
    return AnalyticsService.national_overview(db)


@router.get("/state/{state_id}")
def state_summary(
    state_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """State-level voter & application breakdown."""
    return AnalyticsService.state_summary(db, state_id)


@router.get("/district/{district_id}")
def district_summary(
    district_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """District-level breakdown."""
    return AnalyticsService.district_summary(db, district_id)


@router.get("/audit-activity")
def audit_activity(
    limit: int = 50,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Recent audit log entries."""
    return AnalyticsService.recent_audit_activity(db, limit)
