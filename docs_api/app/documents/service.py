from fastapi import HTTPException

from app.documents.schemas import DocumentIngestionRequest
from app.documents.parser import parse_docx_to_chunks
from app.clients.minio_client import MinioClient
from app.clients.chromadb_client import ChromaDBManager
from app.logger import logger


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
        chunks = parse_docx_to_chunks(document_bytes)
        logger.info(f"Документ {request.document_id} разбит на {len(chunks)} чанков")
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        raise

    try:
        chromadb_manager.add_chunks(
            collection_name=str(request.document_id),
            chunks=chunks,
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


async def get_list_collections(chromadb_manager: ChromaDBManager) -> list[str]:
    try:
        collections = chromadb_manager.get_list_collections()
        return collections
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при получении списка коллекций")
