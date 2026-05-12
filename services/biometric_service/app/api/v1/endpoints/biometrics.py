from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api import deps
from app.services.biometric_vault import BiometricVault
from shared.models.user import User
import base64

router = APIRouter()


class FacePayload(BaseModel):
    """Client sends a base64-encoded JPEG/PNG. Never a raw binary upload."""
    image_b64: str          # data:image/jpeg;base64,... or raw base64
    correlation_id: str | None = None


class RevokePayload(BaseModel):
    reason: str


@router.post("/enroll/face")
def enroll_face(
    body: FacePayload,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Enroll a face biometric for the authenticated voter.
    Raw image data is processed in memory — NEVER persisted.
    """
    # Strip data-URI prefix if present
    b64 = body.image_b64.split(",")[-1]
    result = BiometricVault.enroll_face(
        db, user_id=current_user.id, image_b64=b64, correlation_id=body.correlation_id
    )
    if not result["success"]:
        raise HTTPException(status_code=422, detail=result.get("reason", "enrollment_failed"))
    return result


@router.post("/verify/face")
def verify_face(
    body: FacePayload,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Verify the authenticated voter's face against their stored encrypted template."""
    b64 = body.image_b64.split(",")[-1]
    result = BiometricVault.verify_face(
        db, user_id=current_user.id, image_b64=b64, correlation_id=body.correlation_id
    )
    return result


@router.post("/{user_id}/revoke")
def revoke_biometric(
    user_id: str,
    body: RevokePayload,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(
        deps.RoleChecker(["chief_election_commissioner", "district_election_officer"])
    ),
):
    """Officer revokes a voter's biometric template (compromise / loss)."""
    result = BiometricVault.revoke(db, user_id=user_id, reason=body.reason, officer_id=current_user.id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail="No template found")
    return result
