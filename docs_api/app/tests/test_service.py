from random import choice
from pydantic import ValidationError
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableMap

from app.logger import logger
from app.clients.chromadb_client import ChromaDBManager
from app.clients.openai_api_client import CustomLLM
from app.tests.schemas import TestRequest, TestResponse
from app.tests.test_prompt import test_prompt


def generate_test_question(request: TestRequest) -> TestResponse:
    chromadb = ChromaDBManager()

    chunk_ids = chromadb.get_chunk_ids_by_collection(request.collection_name)
    if not chunk_ids:
        logger.warning(f"Нет чанков в коллекции: {request.collection_name}")
        raise ValueError("Невозможно сгенерировать тест: коллекция пуста.")

    random_chunk_id = choice(chunk_ids)
    chunk_text = chromadb.get_chunk_by_id(request.collection_name, random_chunk_id)

    if not chunk_text:
        logger.error(f"Не удалось получить текст чанка с id={random_chunk_id}")
        raise ValueError("Ошибка при получении текста чанка.")

    llm = CustomLLM()
    parser = JsonOutputParser()

    chain = (
        RunnableMap({"chunk_text": RunnablePassthrough()})
        | test_prompt
        | llm
        | parser
    )

    try:
        result_dict = chain.invoke(chunk_text)
        return TestResponse(**result_dict)
    except ValidationError as ve:
        logger.error("Ошибка валидации при создании TestResponse из результата LLM:")
        for err in ve.errors():
            loc = ' -> '.join(str(x) for x in err.get('loc', []))
            msg = err.get('msg', 'Unknown error')
            typ = err.get('type', 'unknown_type')
            logger.error(f"Поле: {loc} | Ошибка: {msg} | Тип: {typ}")
        logger.error(f"Результат от LLM (до валидации): {result_dict}")
        raise ValueError("Ответ модели не соответствует ожидаемой структуре TestResponse.")
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка при генерации или парсинге вопроса: {e}")
        raise ValueError("Ошибка при генерации тестового вопроса.")
