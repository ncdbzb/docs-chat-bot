import uuid
import httpx
from fastapi import UploadFile, HTTPException

from app.documents.schemas import DocumentCreateResponse, DocumentCreateMeta
from app.documents.doc_repository import DocumentRepository
from app.clients.minio_client import MinioClient
from app.auth.models import AuthUser
from app.logger import logger


MAX_FILE_SIZE_MB = 100
ALLOWED_EXTENSIONS = {".docx"}

async def save_document(
    file: UploadFile,
    user: AuthUser,
    metadata: DocumentCreateMeta,
    minio_client: MinioClient,
    repo: DocumentRepository,
) -> DocumentCreateResponse:
    logger.info(f"Начало загрузки документа пользователем {user.id}: {file.filename}")

    if not file.filename:
        logger.warning("Файл не загружен")
        raise HTTPException(status_code=400, detail="Файл не загружен")

    if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        logger.warning(f"Недопустимый тип файла: {file.filename}")
        raise HTTPException(status_code=400, detail="Неподдерживаемый тип файла")

    contents = await file.read()
    if not contents:
        logger.warning("Файл пустой")
        raise HTTPException(status_code=400, detail="Файл пустой")

    file_size = len(contents)
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        logger.warning("Файл превышает допустимый размер")
        raise HTTPException(status_code=400, detail="Размер файла превышает 100MB")

    if await repo.is_name_exists_for_user(user.id, metadata.name):
        raise HTTPException(status_code=400, detail="Документ с таким именем уже существует")

    file_type = file.filename.split(".")[-1].lower()
    doc_id = uuid.uuid4()
    object_name = f"{doc_id}.{file_type}"
    content_type = file.content_type or "application/octet-stream"

    try:
        minio_client.upload_document(
            file_bytes=contents,
            object_name=object_name,
            content_type=content_type
        )
    except Exception as e:
        logger.error(f"Ошибка загрузки файла в MinIO: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при сохранении в MinIO")

    try:
        result = await repo.add_document(
            doc_id=doc_id,
            metadata=metadata,
            original_filename=file.filename,
            type=file_type,
            size=file_size,
            user_id=user.id,
            storage_key=object_name,
        )
    except Exception:
        try:
            minio_client.delete_document(object_name)
            logger.info(f"Файл {object_name} удалён из MinIO после ошибки в БД.")
        except Exception as minio_err:
            logger.critical(f"Ошибка при удалении из MinIO после сбоя: {minio_err}")
        raise HTTPException(status_code=500, detail="Ошибка при сохранении документа")
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "http://docs_api:8080/documents/ingest",
                json={
                    "document_id": str(doc_id),
                    "storage_key": object_name,
                    "original_filename": file.filename,
                }
                )
    except Exception as e:
        logger.error(f"Ошибка при вызове docs_api для обработки документа: {e}")
    
    return result
