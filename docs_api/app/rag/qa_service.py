from langchain.chains import RetrievalQA
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langfuse.langchain import CallbackHandler

from app.clients.openai_api_client import CustomLLM
from app.clients.chromadb_client import ChromaDBManager
from app.clients.langfuse_client import LangfuseClient
from app.rag.qa_prompt import qa_prompt
from app.logger import logger


# langfuse = LangfuseClient().get_client()
# langfuse_handler = CallbackHandler()


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
        chain_type_kwargs={"prompt": qa_prompt}
    )

    response = qa_chain.invoke(
        {"query": question},
        # config={"callbacks": [langfuse_handler]}
    )

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

