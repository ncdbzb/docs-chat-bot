import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from time import time

from app.config import settings
from app.logger import logger
from app.clients.openai_api_client import CustomOllamaEmbeddings


class ChromaDBManager:
    def __init__(self, collection_name: str):
        self._collection_name = collection_name
        self._client = chromadb.HttpClient(
            host=settings.chromadb_host,
            port=settings.chromadb_port,
            settings=Settings(
                is_persistent=True,
                persist_directory=settings.persist_directory,
                chroma_client_auth_provider=settings.chroma_client_auth_provider,
                chroma_client_auth_credentials=settings.chroma_server_authn_credentials,
            ),
        )
        self.embeddings = CustomOllamaEmbeddings()
        self._chroma_collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"timestamp": time()}
        )
        if not self._chroma_collection.metadata or not self._chroma_collection.metadata.get("timestamp"):
            self._update_collection_timestamp()

        self._vectorstore = None

    def _update_collection_timestamp(self):
        try:
            self._chroma_collection.modify(
                metadata={"timestamp": time()}
            )
        except Exception as e:
            logger.warning(f"Не удалось обновить timestamp коллекции: {e}")

    @property
    def vectorstore(self) -> Chroma:
        if self._vectorstore is None:
            self._vectorstore = Chroma(
                client=self._client,
                collection_name=self._collection_name,
                embedding_function=self.embeddings,
                persist_directory=settings.persist_directory,
            )
        return self._vectorstore

    def get_collection_length(self) -> int:
        return self._chroma_collection.count()
