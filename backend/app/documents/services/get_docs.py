from app.auth.models import AuthUser
from app.documents.doc_repository import DocumentRepository
from app.documents.schemas import DocumentShort


async def get_user_documents(user: AuthUser, repo: DocumentRepository) -> list[DocumentShort]:
    return await repo.get_my_documents_from_repo(user_id=user.id)


async def get_all_documents(repo: DocumentRepository) -> list[DocumentShort]:
    documents = await repo.get_all_documents_from_repo()
    return [DocumentShort(name=doc.name, description=doc.description) for doc in documents]
