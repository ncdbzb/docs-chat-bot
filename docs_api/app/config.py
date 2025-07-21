import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # OpenAI API
    OPENAI_API_URL: str = os.getenv("OPENAI_API_URL")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")

    # ChromaDB
    CHROMADB_HOST: str
    CHROMA_CLIENT_AUTH_PROVIDER: str  
    CHROMA_SERVER_AUTHN_CREDENTIALS: str  
    CHROMADB_PORT: int  
    CHROMA_DOCS_COLLECTION_NAME: str  
    PERSIST_DIRECTORY: str


settings = Settings()
