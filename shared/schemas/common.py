from pydantic import BaseModel, field_validator
from typing import Optional, Any, Dict
from datetime import datetime
import re

class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class AuditEvent(BaseModel):
    service: str
    action: str
    actor_id: str
    resource_id: Optional[str] = None
    resource_type: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.utcnow()

class MaskedAadhaar(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        # Mask everything except last 4
        clean = re.sub(r'[^0-9]', '', v)
        if len(clean) < 4:
            return "XXXX"
        return f"XXXX-XXXX-{clean[-4:]}"

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string', format='aadhaar-masked')
