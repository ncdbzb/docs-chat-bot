import uuid
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM 
from sqlalchemy import (
    Table, Column, DateTime, ForeignKey, MetaData
)
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func

from app.auth.models import user

metadata = MetaData()


class AdminRequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


admin_requests = Table(
    "admin_requests",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey(user.c.id, ondelete="CASCADE"), nullable=False),
    Column("status", ENUM(AdminRequestStatus, name="adminrequeststatus", create_type=False),
           nullable=False, default=AdminRequestStatus.pending),
    Column("info", MutableDict.as_mutable(JSONB), nullable=False, default=dict),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)
