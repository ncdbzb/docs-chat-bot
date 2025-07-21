import httpx
from app.logger import logger
from app.config import settings


class DocsApiClient:
    def __init__(self):
        self.base_url = settings.docs_api_url

    async def ingest_document(self, document_id: str, storage_key: str, original_filename: str) -> None:
        url = f"{self.base_url}/documents/ingest"
        payload = {
            "document_id": document_id,
            "storage_key": storage_key,
            "original_filename": original_filename
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"[DocsAPI] Ошибка при отправке документа {document_id} на индексирование: {e}")
            raise

    async def delete_document(self, document_id: str) -> None:
        url = f"{self.base_url}/documents/{document_id}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(url)
                response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"[DocsAPI] Ошибка при удалении документа {document_id}: {e}")
            raise
