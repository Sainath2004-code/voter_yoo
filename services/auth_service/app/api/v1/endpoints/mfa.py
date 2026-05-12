from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from shared.models.user import User
import pyotp
import qrcode
import io
import base64

router = APIRouter()

@router.post("/mfa/setup")
def setup_mfa(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Generate a new TOTP secret and QR code for the user.
    """
    if current_user.mfa_enabled:
        raise HTTPException(status_code=400, detail="MFA already enabled")
        
    secret = pyotp.random_base32()
    current_user.totp_secret = secret
    db.commit()
    
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=current_user.email, 
        issuer_name="National Secure Voting Portal"
    )
    
    # Generate QR Code
    img = qrcode.make(provisioning_uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    qr_base64 = base64.b64encode(buf.getvalue()).decode()
    
    return {
        "secret": secret,
        "qr_code": f"data:image/png;base64,{qr_base64}"
    }

@router.post("/mfa/enable")
def enable_mfa(
    code: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Verify the first code to formally enable MFA for the account.
    """
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="MFA setup not initiated")
        
    totp = pyotp.TOTP(current_user.totp_secret)
    if totp.verify(code):
        current_user.mfa_enabled = True
        db.commit()
        return {"status": "MFA enabled successfully"}
        
    raise HTTPException(status_code=400, detail="Invalid verification code")
