import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.models import qa_logs, test_logs
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
    
    async def log_test(
        self,
        *,
        test_id: uuid.UUID,
        user_id: uuid.UUID,
        document_id: uuid.UUID,
        question: str,
        option_1: str,
        option_2: str,
        option_3: str,
        option_4: str,
        right_answer: str,
    ) -> None:
        stmt = insert(test_logs).values(
            id=test_id,
            user_id=user_id,
            document_id=document_id,
            question=question,
            option_1=option_1,
            option_2=option_2,
            option_3=option_3,
            option_4=option_4,
            right_answer=right_answer,
        )
        try:
            await self.session.execute(stmt)
            await self.session.commit()
            logger.info(f"Тест сохранён: user_id={user_id}, doc_id={document_id}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при логировании теста: {e}")
            raise

    async def get_right_answer_by_test_id(self, test_id: uuid.UUID) -> str:
        stmt = select(test_logs.c.right_answer).where(test_logs.c.id == test_id)
        try:
            result = await self.session.execute(stmt)
            answer_row = result.fetchone()
            if not answer_row:
                raise ValueError("Тест не найден")
            return answer_row[0]
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении правильного ответа: {e}")
            raise
