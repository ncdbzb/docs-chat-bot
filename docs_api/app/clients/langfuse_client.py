from langfuse import Langfuse

from app.logger import logger
from app.config import settings


class LangfuseClient:

    def __init__(self):
        self.secret_key=settings.LANGFUSE_SECRET_KEY
        self.public_key=settings.LANGFUSE_PUBLIC_KEY
        self.host=settings.LANGFUSE_HOST

    def get_client(self) -> Langfuse | None:
        try:
            langfuse = Langfuse(
                secret_key=settings.LANGFUSE_SECRET_KEY,
                public_key=settings.LANGFUSE_PUBLIC_KEY,
                host=settings.LANGFUSE_HOST,
            )
            logger.info(f"Подключено к логгированию Langfuse {settings.LANGFUSE_HOST}: {langfuse.auth_check()}")
            return langfuse
        
        except Exception as e:
            logger.error(
                f"Ошибка при подключении к Langfuse {settings.LANGFUSE_HOST}, логгирование запросов отключено!, {e}"
            )
            return None
