from fastapi import FastAPI

from app.documents.router import router as documents_router


def include_routers(app: FastAPI):
    app.include_router(documents_router, prefix="/documents", tags=["Documents"])
