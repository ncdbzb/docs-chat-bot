from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.admin_requests.models import AdminRequestStatus  # Enum: pending, approved, rejected


class UserInfo(BaseModel):
    name: str
    surname: str
    email: EmailStr


class AdminRequest(BaseModel):
    id: UUID
    user_id: UUID
    status: AdminRequestStatus
    created_at: datetime
    info: UserInfo

    class Config:
        from_attributes = True


class RequestIdSchema(BaseModel):
    request_id: UUID