from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal
from shared.models.user import User, ScopeType
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)
        
        # Session invalidation & Device tracking would go here
        
    except (JWTError, Exception):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges"
            )
        return current_user

def check_geographic_scope(
    target_scope_type: ScopeType,
    target_scope_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Enforce region-scoped RBAC. Ensures the officer is only accessing data within their jurisdiction.
    """
    if current_user.role == "chief_election_commissioner":
        return current_user # CEC has global access
    
    # If the user has a national scope but isn't CEC (e.g., an auditor), they have access
    if current_user.scope_type == ScopeType.NATIONAL:
        return current_user

    # Strict Hierarchy Matching Logic
    # In a real scenario, this would recursively check if the target_scope_id belongs to the current_user's scope_id
    # e.g., if target is Booth 123, does Booth 123 belong to AC 45, which belongs to District X (user's scope)?
    
    # For performance, this dependency assumes the endpoint provides the exact target_scope_type to validate against.
    if current_user.scope_type != target_scope_type or current_user.scope_id != target_scope_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Unauthorized. Your scope ({current_user.scope_type.value}) does not cover this resource."
        )
        
    return current_user
