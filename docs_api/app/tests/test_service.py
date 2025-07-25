from random import choice
from pydantic import ValidationError
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap

from app.logger import logger
from app.clients.chromadb_client import ChromaDBManager
from app.clients.openai_api_client import CustomLLM
from app.tests.schemas import TestRequest, TestResponse


QUESTION_GEN_PROMPT = PromptTemplate.from_template(
    """Ты — ассистент по обучению сотрудников на основе внутренних документов компании ООО «УЦСБ».

Вот отрывок из внутреннего документа:
```{chunk_text}```

На его основе сгенерируй **один** тестовый вопрос с **четырьмя вариантами ответа**, **строго в формате JSON** со всеми следующими полями:

- `"question"`: строка — формулировка вопроса.
- `"1 option"`, `"2 option"`, `"3 option"`, `"4 option"`: строки — варианты ответа.
- `"right answer"`: **строго текст одного из четырёх вариантов**, то есть должно точно совпадать с одним из полей `"1 option"`–`"4 option"`.

**Формат ответа — строго только JSON. Без пояснений, без заголовков, без комментариев.**

Все ключи должны быть заключены в **двойные кавычки**. Не завершай JSON до тех пор, пока все поля не будут заполнены.

Вот пример правильного формата:

```json
{{
  "question": "Кто отвечает за пожарную безопасность?",
  "1 option": "Охранник",
  "2 option": "Ответственный по ПБ",
  "3 option": "Любой сотрудник",
  "4 option": "Пожарная инспекция",
  "right answer": "Ответственный по ПБ"
}}
```
"""
)


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
    prompt = QUESTION_GEN_PROMPT

    chain = (
        RunnableMap({"chunk_text": RunnablePassthrough()})
        | prompt
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
