from typing import List
from app.models.voter_application import VoterApplication, ApplicationStatus
from datetime import datetime

class VerificationService:
    async def assign_blo(self, application_id: str, blo_id: str):
        """
        Assign a Booth Level Officer to an application for field verification.
        """
        # Fetch app from DB
        # Update status to BLO_ASSIGNED
        return {"status": "success", "blo_id": blo_id}

    async def record_field_verification(self, application_id: str, remarks: str, is_genuine: bool):
        """
        Record the results of a physical visit by the BLO.
        """
        status = ApplicationStatus.FIELD_VERIFIED if is_genuine else ApplicationStatus.REJECTED
        return {
            "status": status,
            "remarks": remarks,
            "verification_date": datetime.utcnow()
        }

    async def approve_application(self, application_id: str, officer_id: str):
        """
        Final approval by RO/ARO. Triggers EPIC generation.
        """
        # 1. Update app status to APPROVED
        # 2. Trigger EPIC generation service
        # 3. Notify voter
        return {"status": ApplicationStatus.APPROVED, "approved_by": officer_id}

verification_service = VerificationService()
