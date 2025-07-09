import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_URL: str = os.getenv("OPENAI_API_URL")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")

settings = Settings()
