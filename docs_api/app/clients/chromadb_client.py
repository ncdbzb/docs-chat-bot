import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma

from app.config import settings
from app.logger import logger
from app.clients.openai_api_client import CustomOllamaEmbeddings
from app.documents.schemas import Chunk


class ChromaDBManager:
    def __init__(self):
        self._client = chromadb.HttpClient(
            host=settings.CHROMADB_HOST,
            port=settings.CHROMADB_PORT,
            settings=Settings(
                is_persistent=True,
                persist_directory=settings.PERSIST_DIRECTORY,
                chroma_client_auth_provider=settings.CHROMA_CLIENT_AUTH_PROVIDER,
                chroma_client_auth_credentials=settings.CHROMA_SERVER_AUTHN_CREDENTIALS,
            ),
        )
        self.embeddings = CustomOllamaEmbeddings()

    def get_vectorstore(self, collection_name: str) -> Chroma:
        self._get_collection(collection_name)

        return Chroma(
            client=self._client,
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=settings.PERSIST_DIRECTORY,
        )

    def _get_collection(self, collection_name: str):
        return self._client.get_or_create_collection(name=collection_name)

    def get_collection_length(self, collection_name: str) -> int:
        try:
            collection = self._get_collection(collection_name)
            return collection.count()
        except Exception as e:
            logger.error(f"Не удалось получить размер коллекции '{collection_name}': {e}")
            return 0
    
    def get_list_collections(self) -> list[str]:
        try:
            collections = self._client.list_collections()
            return [collection.name for collection in collections]
        except Exception as e:
            logger.error(f"Ошибка при получении списка коллекций: {e}")
            return []

    def _add_texts(self, collection_name: str, texts: list[str], ids: list[str]) -> list[str]:
        """Добавляет документы в указанную коллекцию Chroma."""
        vectorstore = self.get_vectorstore(collection_name)
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                return vectorstore.add_texts(texts=texts, ids=ids)
            except Exception as e:
                logger.error(f"Ошибка при добавлении документов в Chroma (попытка {attempt}): {e}")
        logger.error("Документы не были добавлены в Chroma после всех попыток.")
        return []

    def add_chunks(self, collection_name: str, chunks: list[Chunk]) -> list[str]:
        """Добавляет чанки документа в указанную коллекцию."""
        if not chunks:
            logger.info("Список чанков пуст — добавление в Chroma пропущено.")
            return []

        logger.info(f"Добавление {len(chunks)} чанков в коллекцию '{collection_name}'...")
        texts = [chunk.text for chunk in chunks]
        ids = [chunk.id for chunk in chunks]
        chunk_ids = self._add_texts(collection_name, texts, ids)
        total_chunks = self.get_collection_length(collection_name)

        logger.info(
            f"Добавлено {len(chunk_ids)} чанков, всего в коллекции: {total_chunks}"
        )
        return chunk_ids

    def delete_collection(self, collection_name: str) -> None:
        """Удаляет коллекцию по её имени."""
        try:
            self._client.delete_collection(name=collection_name)
            logger.info(f"Коллекция '{collection_name}' успешно удалена.")
        except Exception as e:
            logger.error(f"Ошибка при удалении коллекции '{collection_name}': {e}")
