from fastapi import APIRouter, Depends, status

from app.feedbacks.schemas import FeedbackCreate
from app.feedbacks.feedback_service import send_feedback_for_user
from app.auth.auth_config import current_user_optional
from app.auth.models import AuthUser
from app.dependencies.repository import get_feedback_repository


router = APIRouter()


@router.post("/send_feedback", status_code=status.HTTP_201_CREATED)
async def send_feedback_endpoint(
    body: FeedbackCreate,
    user: AuthUser | None = Depends(current_user_optional),
    feedback_repo = Depends(get_feedback_repository),
):
    await send_feedback_for_user(
        user=user,
        feedback_create=body,
        feedback_repo=feedback_repo
    )
