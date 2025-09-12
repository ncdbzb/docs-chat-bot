from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # OpenAI API
    OPENAI_API_URL: str
    LLM_API_KEY: str
    LLM_MODEL: str
    EMBEDDING_MODEL: str

    # ChromaDB
    CHROMADB_HOST: str
    CHROMA_CLIENT_AUTH_PROVIDER: str  
    CHROMA_SERVER_AUTHN_CREDENTIALS: str  
    CHROMADB_PORT: int  
    CHROMA_DOCS_COLLECTION_NAME: str  
    PERSIST_DIRECTORY: str

    # Minio
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool = False
    MINIO_BUCKET_NAME: str
    MINIO_ROOT_PATH: str

    # Langfuse
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_HOST: str

    # Unstructured API
    UNSTRUCTURED_API_PORT: str
    @property
    def unstructured_api_url(self) -> str:
        return f"http://unstructured-api:{self.UNSTRUCTURED_API_PORT}/general/v0/general"

    # Chunking settings
    CHUNKING_STRATEGY: str = "by_title"   # or "basic"
    UNSTRUCTURED_STRATEGY: str = "auto"   # auto | fast | hi_res
    MAX_CHARACTERS: int = 1500
    NEW_AFTER_N_CHARS: int = 1200
    COMBINE_UNDER_N_CHARS: int = 200

settings = Settings()
