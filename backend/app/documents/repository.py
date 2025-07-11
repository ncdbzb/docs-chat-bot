import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, or_
from sqlalchemy.exc import SQLAlchemyError

from app.documents.models import documents
from app.documents.schemas import DocumentCreateResponse
from app.logger import logger


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_document(
        self,
        *,
        doc_id: uuid.UUID,
        name: str,
        original_filename: str,
        description: str,
        type: str,
        size: int,
        user_id: uuid.UUID,
        storage_key: str,
    ) -> DocumentCreateResponse:
        stmt = (
            insert(documents)
            .values(
                id=doc_id,
                name=name,
                original_filename=original_filename,
                description=description,
                type=type,
                size=size,
                user_id=user_id,
                storage_key=storage_key,
            )
            .returning(documents)
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            logger.info(f"Документ '{name}' добавлен в БД с ID {doc_id}")
            return DocumentCreateResponse(**result.fetchone()._mapping)
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении документа в БД: {e}")
            raise

    async def get_all_documents(self) -> list[dict]:
        stmt = select(documents)
        try:
            result = await self.session.execute(stmt)
            rows = result.fetchall()
            logger.info(f"Получено {len(rows)} документов из БД")
            return [row._mapping for row in rows]
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении документов: {e}")
            raise

    async def is_name_exists_for_user(self, user_id: uuid.UUID, name: str) -> bool:
        stmt = select(documents.c.id).where(
            documents.c.name == name,
            documents.c.user_id == user_id
        ).limit(1)

        try:
            result = await self.session.execute(stmt)
            exists = result.scalar() is not None
            logger.debug(f"Документ с именем '{name}' у пользователя {user_id} уже существует: {exists}")
            return exists
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при проверке существования документа: {e}")
            raise
    
    async def delete_documents(self, doc_ids: list[uuid.UUID]) -> int:
        if not doc_ids:
            logger.warning("Список ID документов для удаления пуст")
            return 0

        stmt = delete(documents).where(documents.c.id.in_(doc_ids))

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            deleted_count = result.rowcount or 0
            logger.info(f"Удалено {deleted_count} документов из БД")
            return deleted_count
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении документов: {e}")
            raise
    
    async def get_my_documents_from_repo(self, user_id: uuid.UUID):
        try:
            stmt = select(documents.c.name, documents.c.description).where(
                documents.c.user_id == user_id
            )
            result = await self.session.execute(stmt)
            docs = result.mappings().all()
            logger.info(f"Найдено {len(docs)} документов для пользователя {user_id}")
            return docs
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении документов пользователя {user_id}: {e}")
            raise


    async def get_all_documents_from_repo(self):
        try:
            stmt = select(documents.c.name, documents.c.description)
            result = await self.session.execute(stmt)
            docs = result.mappings().all()
            logger.info(f"Найдено {len(docs)} документов (всего)")
            return docs
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении всех документов: {e}")
            raise
