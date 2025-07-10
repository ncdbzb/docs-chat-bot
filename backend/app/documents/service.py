import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.documents.models import documents
from app.documents.schemas import DocumentCreateResponse
from app.clients.minio_client import MinioClient
from app.auth.models import AuthUser


MAX_FILE_SIZE_MB = 100
ALLOWED_EXTENSIONS = {".txt"}

minio_client = MinioClient()


async def save_document(
    file: UploadFile,
    user: AuthUser,
    session: AsyncSession,
    doc_name: str,
    doc_description: str,
) -> DocumentCreateResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Файл не загружен")

    if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Неподдерживаемый тип файла")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Файл пустой")

    file_size = len(contents)
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Размер файла превышает 100MB")

    check_query = select(documents).where(
        documents.c.name == doc_name,
        documents.c.user_id == user.id
    )
    result = await session.execute(check_query)
    if result.scalar():
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
        raise HTTPException(status_code=500, detail="Ошибка при сохранении в MinIO")

    stmt = insert(documents).values(
        id=doc_id,
        name=doc_name,
        original_filename=file.filename,
        description=doc_description,
        type=file_type,
        size=file_size,
        user_id=user.id,
        storage_key=object_name
    ).returning(documents)

    result = await session.execute(stmt)
    await session.commit()

    return DocumentCreateResponse(**result.fetchone()._mapping)
