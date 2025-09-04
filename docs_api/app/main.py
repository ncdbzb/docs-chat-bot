import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

from app.routers import include_routers
from app.clients.langfuse_client import LangfuseClient


# Фильтр для скрытия логов от healthcheck
class HealthcheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/health" not in record.getMessage()


# Добавляем фильтр к uvicorn.access
logging.getLogger("uvicorn.access").addFilter(HealthcheckFilter())


@asynccontextmanager
async def lifespan(app: FastAPI):
    langfuse = LangfuseClient().get_client()
    yield


app = FastAPI(
    title="DOCS-API",
    # lifespan=lifespan
)

# Подключаем все роутеры
include_routers(app)


@app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"})
