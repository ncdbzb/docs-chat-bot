import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update, or_
from sqlalchemy.exc import SQLAlchemyError

from app.documents.models import documents
from app.documents.schemas import DocumentCreateResponse, Document, DocumentShort, DocumentCreateMeta
from app.logger import logger


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_document(
        self,
        *,
        doc_id: uuid.UUID,
        metadata: DocumentCreateMeta,
        original_filename: str,
        type: str,
        size: int,
        user_id: uuid.UUID,
        storage_key: str,
        added_by_admin: bool,
    ) -> DocumentCreateResponse:
        stmt = (
            insert(documents)
            .values(
                id=doc_id,
                name=metadata.name,
                original_filename=original_filename,
                description=metadata.description,
                type=type,
                size=size,
                user_id=user_id,
                storage_key=storage_key,
                added_by_admin=added_by_admin,
            )
            .returning(documents)
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            logger.info(f"Документ '{metadata.name}' добавлен в БД с ID {doc_id}")
            return DocumentCreateResponse(**result.fetchone()._mapping)
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении документа в БД: {e}")
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

    async def delete_document_by_name(self, doc_names: str | list[str]) -> int:
        if isinstance(doc_names, str):
            doc_names = [doc_names]

        if not doc_names:
            logger.warning("Список имён документов для удаления пуст")
            return 0

        stmt = delete(documents).where(documents.c.name.in_(doc_names))

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            deleted_count = result.rowcount or 0
            logger.info(f"Удалено {deleted_count} документов из БД: {doc_names}")
            return deleted_count
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении документов по имени: {e}")
            raise

    async def update_document_by_name(self, current_name: str, fields: dict) -> None:
        try:
            stmt = (
                update(documents)
                .where(documents.c.name == current_name)
                .values(**fields)
            )
            await self.session.execute(stmt)
            await self.session.commit()
            logger.info(f"Документ '{current_name}' обновлён: {fields}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при обновлении документа '{current_name}': {e}")
            raise

    async def get_document_by_name(self, doc_name: str) -> Document:
        try:
            stmt = select(documents).where(documents.c.name == doc_name)
            result = await self.session.execute(stmt)
            row = result.mappings().first()

            if row is None:
                raise ValueError(f"Документ с именем '{doc_name}' не найден.")

            return Document.model_validate(row)

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении документа '{doc_name}': {e}")
            raise

    async def get_all_documents_from_repo(self) -> list[Document]:
        stmt = select(documents)
        try:
            result = await self.session.execute(stmt)
            rows = result.mappings().all()
            logger.info(f"Получено {len(rows)} документов из БД")
            return [Document.model_validate(row) for row in rows]

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении документов: {e}")
            raise

    async def get_my_documents_from_repo(self, user_id: uuid.UUID) -> list[DocumentShort]:
        try:
            stmt = select(documents.c.name, documents.c.description).where(
                or_(
                    documents.c.user_id == user_id,
                    documents.c.added_by_admin == True
                )
            )
            result = await self.session.execute(stmt)
            rows = result.mappings().all()
            logger.info(f"Найдено {len(rows)} документов для пользователя {user_id}")
            return [DocumentShort.model_validate(row) for row in rows]

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении документов пользователя {user_id}: {e}")
            raise

    async def get_document_owner_id(self, doc_name: str) -> uuid.UUID | None:
        stmt = select(documents.c.user_id).where(documents.c.name == doc_name)
        result = await self.session.execute(stmt)
        row = result.first()
        return row[0] if row else None

    async def document_exists(self, doc_name: str) -> bool:
        stmt = select(documents.c.id).where(documents.c.name == doc_name)
        result = await self.session.execute(stmt)
        return result.first() is not None

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
