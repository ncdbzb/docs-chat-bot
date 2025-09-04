import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger
from app.feedbacks.models import feedbacks


class FeedbackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_feedback(
        self,
        *,
        user_id: uuid.UUID | None,
        request_id: uuid.UUID,
        value: str,
        user_comment: str | None = None,
    ) -> None:
        stmt = insert(feedbacks).values(
            user_id=user_id,
            request_id=request_id,
            value=value,
            user_comment=user_comment,
        )
        try:
            await self.session.execute(stmt)
            await self.session.commit()
            logger.info(
                f"Фидбек успешно сохранён: user_id={user_id}, request_id={request_id}, value={value}"
            )
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при сохранении фидбека: {e}")
            raise
