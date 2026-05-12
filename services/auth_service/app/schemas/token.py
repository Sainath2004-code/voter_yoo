from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
    mfa_required: bool = False
    mfa_token: Optional[str] = None # Temporary token for MFA verification

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    scope: Optional[str] = None
    exp: Optional[int] = None
