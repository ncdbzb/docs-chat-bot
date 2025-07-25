from typing import Any, Dict, List, Optional

from openai import OpenAI
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.embeddings import Embeddings

from app.config import settings
from app.logger import logger


class CustomLLM(LLM):
    """
    Кастомная LLM модель для работы с API.

    Attributes:
        model_name (str): Название модели для использования
        client (OpenAI | None): Клиент OpenAI API
    """

    model_name: str
    client: OpenAI | None

    def __init__(self):
        """
        Инициализация CustomLLM.

        Args:
            api_url (str): URL эндпоинта API
            model_name (str): Название модели
            api_key (str): Секретный ключ openai_api
        """
        super().__init__(model_name=settings.LLM_MODEL, client=None)
        self.model_name = settings.LLM_MODEL
        self.client = OpenAI(
            base_url=settings.OPENAI_API_URL,   
            api_key=settings.LLM_API_KEY,
        )

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        return self.get_response_from_server(prompt)
    
    def get_response_from_server(self, prompt: str) -> str:
        # logger.info(f'ПРОМПТ: {prompt}')
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.01,
                max_completion_tokens=2000,
            )
            return completion.choices[0].message.content
        
        except Exception as e:
            logger.exception(f"Error in _get_response_from_server: {e}")
            raise

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model_name": "CustomChatModel",
        }

    @property
    def _llm_type(self) -> str:
        return "custom"


class CustomOllamaEmbeddings(Embeddings):
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.client = OpenAI(
            base_url=settings.OPENAI_API_URL,
            api_key=settings.LLM_API_KEY,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._get_embeddings(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._get_embeddings([text])[0]

    def _get_embeddings(self, input_texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            model=self.model_name,
            input=input_texts
        )
        return [e.embedding for e in response.data]
