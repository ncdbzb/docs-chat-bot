from fastapi import APIRouter

from app.tests.test_service import generate_test_question
from app.tests.schemas import TestRequest, TestResponse


router = APIRouter()


@router.post("/get_test", response_model=TestResponse)
async def get_test(request: TestRequest):
    return generate_test_question(request)
