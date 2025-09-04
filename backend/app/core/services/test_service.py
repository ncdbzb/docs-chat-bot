from fastapi import HTTPException
from random import shuffle
from sqlalchemy.exc import SQLAlchemyError

from app.core.schemas import GetTestInnerResult, CheckTestRequest, CheckTestResponse
from app.core.core_repository import CoreRepository
from app.clients.docs_api_client import DocsApiClient
from app.auth.models import AuthUser
from app.documents.doc_repository import DocumentRepository
from app.logger import logger


async def get_test_for_user(
    user: AuthUser | None,
    filename: str,
    doc_repo: DocumentRepository,
    core_repo: CoreRepository,
    docs_api_client: DocsApiClient,
) -> GetTestInnerResult:
    try:
        document = await doc_repo.get_document_by_name(filename)
    except Exception as e:
        logger.error(f"Ошибка при получении документа: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении документа")

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    try:
        test = await docs_api_client.get_test(collection_name=str(document.id))
    except Exception as e:
        logger.error(f"Ошибка при получении теста из docs_api: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении теста")

    options = [
        test.option_1,
        test.option_2,
        test.option_3,
        test.option_4,
    ]
    shuffle(options)

    shuffled_test = GetTestInnerResult(
        id=test.id,
        question=test.question,
        option_1=options[0],
        option_2=options[1],
        option_3=options[2],
        option_4=options[3],
        right_answer=test.right_answer,
    )

    try:
        await core_repo.log_test(
            test_id=test.id,
            user_id=user.id if user else None,
            document_id=document.id,
            question=test.question,
            option_1=test.option_1,
            option_2=test.option_2,
            option_3=test.option_3,
            option_4=test.option_4,
            right_answer=test.right_answer,
        )
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при логировании теста: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при логировании теста")

    return shuffled_test


async def check_test_answer(
    body: CheckTestRequest,
    user: AuthUser | None,
    core_repo: CoreRepository,
) -> CheckTestResponse:
    already_answered = await core_repo.is_already_answered(
        user_id=user.id if user else None,
        test_id=body.request_id
    )
    if already_answered:
        raise HTTPException(status_code=400, detail="Вы уже отвечали на этот вопрос")

    try:
        right_answer = await core_repo.get_right_answer_by_test_id(body.request_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Тест с указанным ID не найден")
    
    is_correct = body.selected_option.strip().lower() == right_answer.strip().lower()

    try:
        await core_repo.log_test_answer(
            user_id=user.id if user else None,
            test_id=body.request_id,
            selected_option=body.selected_option,
            is_correct=is_correct,
        )
    except Exception as e:
        logger.error(f"Ошибка при логировании ответа на тест: {e}")
        raise HTTPException(status_code=500, detail="Не удалось сохранить ответ")

    return CheckTestResponse(right_answer=right_answer)
