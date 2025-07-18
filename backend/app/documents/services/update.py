from fastapi import HTTPException

from app.documents.doc_repository import DocumentRepository
from app.documents.schemas import DocumentUpdate
from app.auth.models import AuthUser


async def update_document(payload: DocumentUpdate, user: AuthUser, repo: DocumentRepository) -> None:
    try:
        doc = await repo.get_document_by_name(payload.current_name)
    except ValueError:
        raise HTTPException(status_code=404, detail="Документ не найден")

    if not user.is_superuser and doc.user_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к изменению")

    update_fields = {}

    if payload.new_name and payload.new_name != doc.name:
        update_fields['name'] = payload.new_name

    if payload.description and payload.description != doc.description:
        update_fields['description'] = payload.description

    if update_fields:
        await repo.update_document_by_name(payload.current_name, update_fields)

