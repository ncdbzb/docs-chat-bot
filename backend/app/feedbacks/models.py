import uuid
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import Table, Column, DateTime, ForeignKey, MetaData, Text
from sqlalchemy.sql import func

from app.auth.models import user


metadata = MetaData()


class FeedbackValue(str, Enum):
    like = "like"
    dislike = "dislike"


feedbacks = Table(
    "feedbacks",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey(user.c.id, ondelete="CASCADE"), nullable=False),
    Column("request_id", UUID(as_uuid=True), nullable=False),
    Column(
        "value",
        ENUM(FeedbackValue, name="feedbackvalue", create_type=False),
        nullable=False
    ),
    Column("user_comment", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)
