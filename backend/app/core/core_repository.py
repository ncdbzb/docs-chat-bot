import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.core.models import qa_logs
from app.logger import logger


class CoreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_qa_interaction(
        self,
        *,
        user_id: uuid.UUID,
        document_id: uuid.UUID,
        question: str,
        answer: str,
    ) -> None:
        stmt = (
            insert(qa_logs).values(
                user_id=user_id,
                document_id=document_id,
                question=question,
                answer=answer,
            )
        )
        try:
            await self.session.execute(stmt)
            await self.session.commit()
            logger.info(f"QA лог успешно сохранен: user_id={user_id}, doc_id={document_id}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при логировании QA: {e}")
            raise
