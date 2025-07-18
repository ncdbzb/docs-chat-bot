from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.documents.doc_repository import DocumentRepository
from app.admin_requests.admin_repository import AdminRepository


def get_document_repository(
    session: AsyncSession = Depends(get_async_session),
) -> DocumentRepository:
    return DocumentRepository(session)


def get_admin_repository(
    session: AsyncSession = Depends(get_async_session), 
) -> AdminRepository:
    return AdminRepository(session)
