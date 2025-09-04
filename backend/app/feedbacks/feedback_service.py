from fastapi import HTTPException

from app.logger import logger
from app.feedbacks.schemas import FeedbackCreate
from app.feedbacks.feedback_repository import FeedbackRepository
from app.auth.models import AuthUser


async def send_feedback_for_user(
    *,
    user: AuthUser | None,
    feedback_create: FeedbackCreate,
    feedback_repo: FeedbackRepository
) -> None:
    """
    Сохраняет фидбек пользователя в БД.
    Проверяет корректность значения value (like/dislike) и логирует результат.
    """
    valid_values = {"like", "dislike"}
    if feedback_create.value not in valid_values:
        raise ValueError(f"Недопустимое значение value: {feedback_create.value}. Допустимые: {valid_values}")
    
    user_id=user.id if user else None
    try:
        await feedback_repo.log_feedback(
            user_id=user_id,
            request_id=feedback_create.request_id,
            value=feedback_create.value,
            user_comment=feedback_create.user_comment,
        )
        logger.info(f"Фидбек сохранён для request_id={feedback_create.request_id} от user_id={user_id}")
    except Exception as e:
        logger.exception(f"Ошибка при отправке фидбека: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при сохранении фидбека")
