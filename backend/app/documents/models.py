import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Table, Column, String, DateTime, ForeignKey, Text, MetaData, BigInteger
)
from sqlalchemy.sql import func

from app.auth.models import user


metadata = MetaData()

documents = Table(
    "documents",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True),
    Column("name", String, nullable=False),
    Column("original_filename", String, nullable=False),
    Column("type", String(10), nullable=False),
    Column("size", BigInteger, nullable=False),
    Column("description", Text),
    Column("user_id", UUID(as_uuid=True), ForeignKey(user.c.id, ondelete="CASCADE")),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)
