from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

from app.clients.openai_api_client import CustomLLM
from app.clients.chromadb_client import ChromaDBManager
from app.logger import logger


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
    chroma_manager = ChromaDBManager()
    vectorstore = chroma_manager.get_vectorstore(collection_name=collection_name)

    all_texts = chroma_manager.get_all_texts(collection_name=collection_name)

    chroma_retriever = vectorstore.as_retriever(search_kwargs={"k": 3}, search_type="similarity")
    
    bm25_retriever = BM25Retriever.from_texts(
        texts=[d["text"] for d in all_texts],
        metadatas=[d["metadata"] | {"id": d["id"], "collection": d["collection"]} for d in all_texts],
        k=2
    )

    ensemble_retriever = EnsembleRetriever(retrievers=[chroma_retriever, bm25_retriever])

    qa_chain = RetrievalQA.from_chain_type(
        llm=CustomLLM(),
        retriever=ensemble_retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    response = qa_chain.invoke({"query": question})

    source_docs = response.get("source_documents", [])
    if source_docs:
        for idx, doc in enumerate(source_docs, 1):
            metadata = doc.metadata if hasattr(doc, "metadata") else {}
            section = metadata.get("section", "Unknown section")
            source_id = metadata.get("source_id", "N/A")
            logger.info(f"[RAG source {idx}] Section: {section}, Source ID: {source_id}\n{doc.page_content}\n{'-'*50}")
    else:
        logger.info("RAG не нашел релевантных документов для вопроса.")

    return response["result"]

