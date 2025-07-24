from fastapi import APIRouter

from app.rag.qa_service import get_answer
from app.rag.schemas import QARequest, QAResponse


router = APIRouter()


@router.post("/answer", response_model=QAResponse)
async def answer_endpoint(request: QARequest):
    answer = get_answer(request.question, request.collection_name)
    return QAResponse(answer=answer)
