from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import AuthUser
from app.documents.repository import DocumentRepository


async def get_user_documents(user: AuthUser, session: AsyncSession):
    repo = DocumentRepository(session)
    return await repo.get_my_documents_from_repo(user_id=user.id)


async def get_all_documents(session: AsyncSession):
    repo = DocumentRepository(session)
    return await repo.get_all_documents_from_repo()
