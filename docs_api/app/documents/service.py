from app.documents.schemas import DocumentIngestionRequest
from app.clients.minio_client import MinioClient
from app.clients.chromadb_client import ChromaDBManager
from app.logger import logger


def dummy_parser(doc_bytes: bytes) -> list[str]:
    return ["chunk 1 from doc", "chunk 2 from doc"]

async def ingest_document(
    request: DocumentIngestionRequest,
    minio_client: MinioClient,
    chromadb_manager: ChromaDBManager,
):
    logger.info(f"Начинаем обработку документа: {request.original_filename}")

    try:
        document_bytes = minio_client.get_document(request.storage_key)
    except Exception as e:
        logger.error(f"Ошибка загрузки файла из MinIO: {e}")
        raise

    try:
        chunks = dummy_parser(document_bytes)
        logger.info(f"Документ {request.document_id} разбит на {len(chunks)} чанков")
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        raise

    try:
        chromadb_manager.add_chunks(
            collection_name=str(request.document_id),
            splitted_docs=chunks,
        )
        logger.info(f"Коллекция {request.document_id} успешно создана")
    except Exception as e:
        logger.error(f"Ошибка загрузки чанков в ChromaDB: {e}")
        raise

    logger.info(f'Коллекции: {chromadb_manager._client.list_collections()}')


async def delete_collection(document_id: str, chromadb_manager: ChromaDBManager):
    logger.info(f"Удаление коллекции {document_id} из ChromaDB")

    try:
        chromadb_manager.delete_collection(document_id)
    except Exception as e:
        logger.error(f"Ошибка удаления коллекции {document_id}: {e}")
        raise
