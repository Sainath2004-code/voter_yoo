import os
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from shared.models.user import User

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGEME_PROD_SECRET")
ALGORITHM = "HS256"

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/access-token")


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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=403, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    return user
