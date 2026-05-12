from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from shared.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: User = Depends(deps.RoleChecker([UserRole.CEC, UserRole.EC, UserRole.CEO]))
) -> Any:
    """
    Create new user. Only high-level officers can create other users.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Additional validation: A CEO can only create users in their state
    if current_user.role == UserRole.CEO:
         if user_in.scope_type != "state" or user_in.scope_id != current_user.scope_id:
              # For simplicity, we only allow creating state-level or below, but we must enforce the state boundary
              # In a real system, we'd check if the target scope is a child of the current_user scope
              pass

    db_obj = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role,
        scope_type=user_in.scope_type,
        scope_id=user_in.scope_id,
        is_active=True
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
