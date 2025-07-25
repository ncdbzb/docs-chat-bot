from fastapi import FastAPI

from app.documents.router import router as documents_router
from app.rag.router import router as rag_router
from app.tests.router import router as tests_router

def include_routers(app: FastAPI):
    app.include_router(documents_router, prefix="/documents", tags=["Documents"])
    app.include_router(rag_router)
    app.include_router(tests_router)
