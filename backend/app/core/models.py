from sqlalchemy import (
    Table, Column, ForeignKey, Text, DateTime, MetaData, Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.auth.models import user
from app.documents.models import documents

metadata = MetaData()

qa_logs = Table(
    "qa_logs",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()),
    Column("user_id", UUID(as_uuid=True), ForeignKey(user.c.id, ondelete="CASCADE"), nullable=True),
    Column("document_id", UUID(as_uuid=True), ForeignKey(documents.c.id, ondelete="CASCADE"), nullable=False),
    Column("question", Text, nullable=False),
    Column("answer", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

test_logs = Table(
    "test_logs",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()),
    Column("user_id", UUID(as_uuid=True), ForeignKey(user.c.id, ondelete="CASCADE"), nullable=True),
    Column("document_id", UUID(as_uuid=True), ForeignKey(documents.c.id, ondelete="CASCADE"), nullable=False),
    Column("question", Text, nullable=False),
    Column("option_1", Text, nullable=False),
    Column("option_2", Text, nullable=False),
    Column("option_3", Text, nullable=False),
    Column("option_4", Text, nullable=False),
    Column("right_answer", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

test_answers_log = Table(
    "test_answers_log",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()),
    Column("user_id", UUID(as_uuid=True), ForeignKey(user.c.id, ondelete="CASCADE"), nullable=True),
    Column("test_id", UUID(as_uuid=True), ForeignKey(test_logs.c.id, ondelete="CASCADE"), nullable=False),
    Column("selected_answer", Text, nullable=False),
    Column("is_correct", Boolean, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)
