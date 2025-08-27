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

    def get_all_texts(self, collection_name: str | None = None) -> list[dict]:
        """
        Получает все тексты из указанной коллекции с метаданными.
        Если collection_name не указан — возвращает данные из всех коллекций.

        Возвращает список словарей:
        {
            "text": str,
            "metadata": dict,
            "id": str,
            "collection": str
        }
        """
        all_texts = []
        try:
            collections = [collection_name] if collection_name else self.get_list_collections()
            for coll_name in collections:
                collection = self._get_collection(coll_name)
                # ids не нужно явно указывать в include
                result = collection.get(include=['documents', 'metadatas'], limit=None)

                for text, metadata, doc_id in zip(result['documents'], result['metadatas'], result['ids']):
                    if text and text.strip():  # защита от пустых строк
                        all_texts.append({
                            "text": text,
                            "metadata": metadata,
                            "id": doc_id,
                            "collection": coll_name
                        })
        except Exception as e:
            logger.error(f"Ошибка при получении всех текстов: {e}")
        return all_texts



    def _add_texts(self, collection_name: str, texts: list[str], ids: list[str], metadatas: list[dict] | None = None) -> list[str]:
        """Добавляет документы в указанную коллекцию Chroma."""
        vectorstore = self.get_vectorstore(collection_name)
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                return vectorstore.add_texts(texts=texts, ids=ids, metadatas=metadatas)
            except Exception as e:
                logger.error(f"Ошибка при добавлении документов в Chroma (попытка {attempt}): {e}")
        logger.error("Документы не были добавлены в Chroma после всех попыток.")
        return []

    def add_chunks(self, collection_name: str, chunks: list[Chunk]) -> list[str]:
        """Добавляет чанки документа в указанную коллекцию с метаданными."""
        if not chunks:
            logger.info("Список чанков пуст — добавление в Chroma пропущено.")
            return []

        logger.info(f"Добавление {len(chunks)} чанков в коллекцию '{collection_name}'...")

        texts = [chunk.text for chunk in chunks]
        ids = [chunk.id for chunk in chunks]

        metadatas = [
            {
                "section": chunk.section or "Unknown",
                "source_id": chunk.source_id or "N/A"
            }
            for chunk in chunks
        ]

        # Добавляем тексты с metadata
        chunk_ids = self._add_texts(collection_name, texts, ids, metadatas=metadatas)
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

    def get_chunk_ids_by_collection(self, collection_name: str) -> list[str]:
        """Возвращает список всех IDs чанков в коллекции."""
        try:
            collection = self._get_collection(collection_name)
            result = collection.get(include=['metadatas'], limit=None)
            return result['ids']
        except Exception as e:
            logger.error(f"Ошибка при получении IDs из коллекции '{collection_name}': {e}")
            return []

    def get_chunk_by_id(self, collection_name: str, chunk_id: str) -> str | None:
        """Возвращает текст чанка по его ID из указанной коллекции."""
        try:
            collection = self._get_collection(collection_name)
            result = collection.get(ids=[chunk_id], include=['documents'])
            documents = result.get('documents', [])
            if documents:
                return documents[0]
            else:
                logger.warning(f"Чанк с id '{chunk_id}' не найден в коллекции '{collection_name}'.")
                return None
        except Exception as e:
            logger.error(f"Ошибка при получении чанка с id '{chunk_id}' из коллекции '{collection_name}': {e}")
            return None
