import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from app.documents.models import documents
from app.documents.schemas import DocumentCreateResponse
from app.auth.models import AuthUser


async def save_document(
    file: UploadFile,
    user: AuthUser,
    session: AsyncSession,
    doc_name: str,
    doc_description: str,
) -> DocumentCreateResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Файл не загружен")

    if not file.filename.endswith((".txt")):
        raise HTTPException(status_code=400, detail="Неподдерживаемый тип файла")

    contents = await file.read()
    file_size = len(contents)
    file_type = file.filename.split(".")[-1].lower()

    doc_id = uuid.uuid4()

    stmt = insert(documents).values(
        id=doc_id,
        name=doc_name,
        original_filename=file.filename,
        description=doc_description,
        type=file_type,
        size=file_size,
        user_id=user.id
    ).returning(documents)

    result = await session.execute(stmt)
    await session.commit()

    return DocumentCreateResponse(**result.fetchone()._mapping)
