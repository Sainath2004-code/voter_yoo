from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.token import Token
from shared.models.user import User
import pyotp

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    request: Request,
    db: Session = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    Implements MFA check, brute-force protection, and session tracking.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Brute-force protection
    if user and user.locked_until and user.locked_until > security.get_now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Account is temporarily locked due to multiple failed attempts."
        )

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.locked_until = security.get_now() + timedelta(minutes=15)
            db.commit()
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Reset failed attempts on success
    user.failed_login_attempts = 0
    user.last_login = security.get_now()
    user.last_login_ip = request.client.host
    
    # Handle MFA Flow
    if user.mfa_enabled:
        # Create a temporary short-lived MFA token
        mfa_token = security.create_access_token(
            user.id, expires_delta=timedelta(minutes=5), scope="mfa_pending"
        )
        db.commit()
        return {
            "access_token": "",
            "token_type": "bearer",
            "mfa_required": True,
            "mfa_token": mfa_token
        }

    # Generate full access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = security.create_refresh_token(user.id)
    user.refresh_token = refresh_token # Store for session invalidation
    
    db.commit()
    
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "mfa_required": False
    }

@router.post("/login/verify-mfa", response_model=Token)
def verify_mfa(
    code: str,
    mfa_token: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Verify TOTP code after initial login.
    """
    try:
        payload = security.decode_token(mfa_token)
        if payload.get("scope") != "mfa_pending":
            raise HTTPException(status_code=403, detail="Invalid MFA token scope")
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid or expired MFA token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify TOTP
    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(code):
        raise HTTPException(status_code=400, detail="Invalid MFA code")

    # Success - generate full tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = security.create_refresh_token(user.id)
    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "mfa_required": False
    }
