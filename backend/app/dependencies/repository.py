from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.documents.doc_repository import DocumentRepository
from app.admin_requests.admin_repository import AdminRepository
from app.core.core_repository import CoreRepository
from app.feedbacks.feedback_repository import FeedbackRepository


def get_document_repository(
    session: AsyncSession = Depends(get_async_session),
) -> DocumentRepository:
    return DocumentRepository(session)


def get_admin_repository(
    session: AsyncSession = Depends(get_async_session), 
) -> AdminRepository:
    return AdminRepository(session)


def get_core_repository(
    session: AsyncSession = Depends(get_async_session), 
) -> CoreRepository:
    return CoreRepository(session)


def get_feedback_repository(
    session: AsyncSession = Depends(get_async_session),
) -> FeedbackRepository:
    return FeedbackRepository(session)
