from fastapi import HTTPException, status

from app.auth.models import AuthUser
from app.clients.repository_client import DocumentRepository
from app.clients.minio_client import MinioClient


async def delete_document(doc_name: str, user: AuthUser, repo: DocumentRepository, minio_client: MinioClient):
    if not await repo.document_exists(doc_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    if not user.is_superuser:
        owner_id = await repo.get_document_owner_id(doc_name)
        if owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: not the owner.")

    try:
        # Получаем storage_key по имени документа
        storage_key = await repo.get_storage_key_by_name(doc_name)

        # Удаляем объект из MinIO
        minio_client.delete_documents(storage_key)

        # Удаляем запись из базы данных
        await repo.delete_document_by_name(doc_name)
    
    except ValueError as ve:
    # Обрабатываем случай, когда документ не найден
        raise HTTPException(status_code=404, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {e}")
