import uuid
from fastapi import APIRouter, Depends

from app.auth.models import AuthUser
from app.auth.auth_config import current_user
from app.dependencies.repository import get_document_repository, get_core_repository
from app.dependencies.docs_api import get_docs_api_client, DocsApiClient
from app.core.core_repository import CoreRepository
from app.documents.doc_repository import DocumentRepository
from app.core.schemas import GetQARequest, GetQAResponse, GetTestResponse, GetTestRequest, CheckTestRequest, CheckTestResponse
from app.core.services.qa_service import get_answer_for_user
from app.core.services.test_service import get_test_for_user, check_test_answer


router = APIRouter()


@router.post("/get_answer", response_model=GetQAResponse)
async def get_answer_endpoint(
    body: GetQARequest,
    user: AuthUser = Depends(current_user),
    doc_repo: DocumentRepository = Depends(get_document_repository),
    core_repo: CoreRepository = Depends(get_core_repository),
    docs_api_client: DocsApiClient = Depends(get_docs_api_client),
):
    answer = await get_answer_for_user(
        user=user,
        filename=body.filename,
        question=body.question,
        doc_repo=doc_repo,
        core_repo=core_repo,
        docs_api_client=docs_api_client,
    )

    return GetQAResponse(result=answer, request_id=str(uuid.uuid4()))


@router.post("/get_test", response_model=GetTestResponse)
async def get_test_endpoint(
    body: GetTestRequest,
    user: AuthUser = Depends(current_user),
    doc_repo: DocumentRepository = Depends(get_document_repository),
    core_repo: CoreRepository = Depends(get_core_repository),
    docs_api_client: DocsApiClient = Depends(get_docs_api_client),
):
    test = await get_test_for_user(
        user=user,
        filename=body.filename,
        doc_repo=doc_repo,
        core_repo=core_repo,
        docs_api_client=docs_api_client,
    )

    return GetTestResponse(
        result=test,
        request_id=str(test.id)
    )


@router.post("/check_test", response_model=CheckTestResponse)
async def check_test_endpoint(
    body: CheckTestRequest,
    user: AuthUser = Depends(current_user),
    core_repo: CoreRepository = Depends(get_core_repository),
):
    return await check_test_answer(body=body, user=user, core_repo=core_repo)
