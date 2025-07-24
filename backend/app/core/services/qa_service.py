from app.documents.doc_repository import DocumentRepository
from app.clients.docs_api_client import DocsApiClient
from app.core.core_repository import CoreRepository
from app.auth.models import AuthUser
from app.logger import logger


async def get_answer_for_user(
    user: AuthUser,
    filename: str,
    question: str,
    doc_repo: DocumentRepository,
    core_repo: CoreRepository,
    docs_api_client: DocsApiClient,
) -> str:
    document = await doc_repo.get_document_by_name(filename)
    if not document:
        raise ValueError("Документ не найден")

    try:
        answer = await docs_api_client.get_answer(
            question=question,
            collection_name=str(document.id)
        )
    except Exception as e:
        logger.error(f"Ошибка генерации ответа: {e}")
        raise RuntimeError(f"Ошибка генерации ответа")

    try:
        await core_repo.log_qa_interaction(
            user_id=user.id,
            document_id=document.id,
            question=question,
            answer=answer,
        )
    except Exception as e:
        logger.error(f"Ошибка логирования ответа: {e}")
        raise RuntimeError(f"Ошибка логирования ответа")

    return answer
