from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from app.clients.openai_api_client import CustomLLM
from app.clients.chromadb_client import ChromaDBManager


# Кастомный промпт для ассистента по нормативным документам ООО УЦСБ
template = """Ты — интеллектуальный ассистент сотрудников компании ООО УЦСБ. У тебя есть доступ к внутренним нормативным документам, инструкциям и регламентам компании. Используй предоставленный контекст для точного ответа на вопрос пользователя. 

Контекст:
{context}

Вопрос пользователя:
{question}

Инструкции:
1. Внимательно изучи предоставленный контекст.
2. Используй только информацию из контекста для ответа.
3. Если нужной информации нет — прямо скажи, что она отсутствует.
4. Отвечай понятно, профессионально и по делу.
5. Когда уместно — цитируй конкретные формулировки из документа.
6. Не выдумывай факты, которых нет в контексте.
7. Не делай предположений, если они не основаны на тексте.

Ответ:"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)


def get_answer(question: str, collection_name: str) -> str:
    chromadb_manager = ChromaDBManager()
    vectorstore = chromadb_manager.get_vectorstore(collection_name=collection_name)

    # RetrievalQA с кастомным промптом
    qa_chain = RetrievalQA.from_chain_type(
        llm=CustomLLM(),
        retriever=vectorstore.as_retriever(search_kwargs={"k": 1}),
        chain_type="stuff",
        # return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    response = qa_chain.invoke({"query": question})
    return response["result"]
