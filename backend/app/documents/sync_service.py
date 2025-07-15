from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.minio_client import MinioClient
from app.clients.repository_client import DocumentRepository
from app.logger import logger


async def sync_documents_with_storage(session: AsyncSession, minio_client: MinioClient):
    repo = DocumentRepository(session)

    # Получаем документы из Postgres
    postgres_docs = await repo.get_all_documents_from_repo()
    postgres_keys = {doc.storage_key: doc.id for doc in postgres_docs}
    postgres_key_set = set(postgres_keys.keys())

    # Получаем объекты из MinIO
    minio_keys_full = minio_client.list_documents()

    # Приводим ключи из MinIO к виду без root_path (обратная операция _get_object_name)
    prefix = f"{minio_client.root_path}/" if minio_client.root_path else ""
    minio_keys = {k[len(prefix):] for k in minio_keys_full if k.startswith(prefix)}

    # Вычисляем разницу
    only_in_postgres = postgres_key_set - minio_keys
    only_in_minio = minio_keys - postgres_key_set

    # Удаляем из Postgres
    if only_in_postgres:
        doc_ids_to_delete = [postgres_keys[k] for k in only_in_postgres]
        await repo.delete_documents(doc_ids_to_delete)

    # Удаляем из MinIO
    if only_in_minio:
        minio_client.delete_documents(list(only_in_minio))

    if not any((only_in_postgres, only_in_minio)):
        logger.info("Базы идентичны, удаление не требуется")

    logger.info("Синхронизация между MinIO и Postgres завершена")
