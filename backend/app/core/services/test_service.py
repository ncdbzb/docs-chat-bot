from app.core.schemas import GetTestInnerResult, CheckTestRequest, CheckTestResponse
from app.core.core_repository import CoreRepository
from app.clients.docs_api_client import DocsApiClient
from app.auth.models import AuthUser
from app.documents.doc_repository import DocumentRepository


async def get_test_for_user(
    user: AuthUser,
    filename: str,
    doc_repo: DocumentRepository,
    core_repo: CoreRepository,
    docs_api_client: DocsApiClient,
) -> GetTestInnerResult:
    document = await doc_repo.get_document_by_name(filename)
    if not document:
        raise ValueError("Документ не найден")

    test = await docs_api_client.get_test(collection_name=str(document.id))

    await core_repo.log_test(
        test_id=test.id,
        user_id=user.id,
        document_id=document.id,
        question=test.question,
        option_1=test.option_1,
        option_2=test.option_2,
        option_3=test.option_3,
        option_4=test.option_4,
        right_answer=test.right_answer,
    )

    return test


async def check_test_answer(
    body: CheckTestRequest,
    core_repo: CoreRepository,
) -> CheckTestResponse:
    right_answer = await core_repo.get_right_answer_by_test_id(body.request_id)
    return CheckTestResponse(right_answer=right_answer)
