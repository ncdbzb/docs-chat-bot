from app.auth.models import AuthUser
from app.clients.repository_client import DocumentRepository


async def get_user_documents(user: AuthUser, repo: DocumentRepository):
    return await repo.get_my_documents_from_repo(user_id=user.id)


async def get_all_documents(repo: DocumentRepository):
    return [
        {"name": doc.get("name"), "description": doc.get("description")}
        for doc in await repo.get_all_documents_from_repo()
    ]
