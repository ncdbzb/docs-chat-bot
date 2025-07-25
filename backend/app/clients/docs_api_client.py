import httpx
from app.logger import logger
from app.config import settings
from app.core.schemas import GetTestInnerResult


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
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"[DocsAPI] Ошибка при отправке документа {document_id} на индексирование: {repr(e)}")
            raise

    async def delete_document(self, document_id: str) -> None:
        url = f"{self.base_url}/documents/{document_id}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(url)
                response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"[DocsAPI] Ошибка при удалении документа {document_id}: {repr(e)}")
            raise

    async def get_collections(self) -> list[str]:
        url = f"{self.base_url}/documents/collections"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                collections = data.get("collections", [])
                logger.info(f"Получено {len(collections)} объектов из ChromaDB")
                return collections
        except httpx.HTTPError as e:
            logger.error(f"[DocsAPI] Ошибка при получении списка коллекций: {repr(e)}")
            raise

    async def get_answer(self, question: str, collection_name: str) -> str:
        url = f"{self.base_url}/get_answer"
        payload = {
            "question": question,
            "collection_name": collection_name
        }

        try:
            async with httpx.AsyncClient(timeout=300) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()["answer"]
        except httpx.HTTPError as e:
            logger.error(f"[DocsAPI] Ошибка при получении ответа от DocsAPI: {repr(e)}")
            raise
    
    async def get_test(self, collection_name: str) -> GetTestInnerResult:
        url = f"{self.base_url}/get_test"
        payload = {"collection_name": collection_name}

        try:
            async with httpx.AsyncClient(timeout=300) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return GetTestInnerResult(**response.json())
        except httpx.HTTPError as e:
            logger.error(f"[DocsAPI] Ошибка при получении теста от DocsAPI: {repr(e)}")
            raise
