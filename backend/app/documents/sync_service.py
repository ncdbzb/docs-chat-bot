from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.minio_client import MinioClient
from app.documents.doc_repository import DocumentRepository
from app.clients.docs_api_client import DocsApiClient
from app.logger import logger


async def sync_documents_with_storage(
    session: AsyncSession,
    minio_client: MinioClient,
    docs_api_client: DocsApiClient,
):
    repo = DocumentRepository(session)

    # Получаем документы из Postgres
    postgres_docs = await repo.get_all_documents_from_repo()
    postgres_keys = {doc.storage_key: doc.id for doc in postgres_docs}
    postgres_key_set = set(postgres_keys.keys())
    postgres_ids = {str(doc.id) for doc in postgres_docs}

    # Получаем объекты из MinIO
    minio_keys_full = minio_client.list_documents()
    prefix = f"{minio_client.root_path}/" if minio_client.root_path else ""
    minio_keys = {k[len(prefix):] for k in minio_keys_full if k.startswith(prefix)}

    # Получаем коллекции из ChromaDB
    chroma_ids = set(await docs_api_client.get_collections())

    # --- Синхронизация MinIO ↔️ Postgres ---
    only_in_postgres = postgres_key_set - minio_keys
    only_in_minio = minio_keys - postgres_key_set

    if only_in_postgres:
        doc_ids_to_delete = [postgres_keys[k] for k in only_in_postgres]
        await repo.delete_documents(doc_ids_to_delete)
        logger.warning(f"Удалены документы из Postgres: {only_in_postgres}")
        actual_postgres_ids = postgres_ids - {str(doc_id) for doc_id in doc_ids_to_delete}
    else:
        actual_postgres_ids = postgres_ids

    if only_in_minio:
        minio_client.delete_documents(list(only_in_minio))
        logger.warning(f"Удалены объекты из MinIO: {only_in_minio}")

    # --- Восстановление недостающих коллекций в ChromaDB ---
    missing_in_chroma = actual_postgres_ids - chroma_ids
    for missing_id in missing_in_chroma:
        logger.warning(f"Коллекция {missing_id} отсутствует в ChromaDB — восстанавливаем через Docs API.")
        try:
            doc = next(d for d in postgres_docs if str(d.id) == missing_id)

            # Для простоты передаем только метаданные, Docs API сам возьмет текст из MinIO при индексации
            await docs_api_client.ingest_document(
                document_id=str(doc.id),
                storage_key=doc.storage_key,
                original_filename=doc.name,
            )
            logger.info(f"Восстановлена коллекция {missing_id} в ChromaDB через Docs API")
        except Exception as e:
            logger.error(f"Ошибка восстановления коллекции {missing_id}: {repr(e)}")

    # --- Удаление "мусорных" коллекций из ChromaDB ---
    extra_in_chroma = chroma_ids - actual_postgres_ids
    for collection_id in extra_in_chroma:
        try:
            await docs_api_client.delete_document(collection_id)
            logger.warning(f"Удалена лишняя коллекция из ChromaDB через Docs API: {collection_id}")
        except Exception as e:
            logger.error(f"Ошибка удаления коллекции {collection_id}: {repr(e)}")

    logger.info("Синхронизация между Postgres, MinIO и ChromaDB завершена")
