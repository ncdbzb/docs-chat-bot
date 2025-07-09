import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import include_routers
from app.auth.init_db import delayed_admin_init


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(delayed_admin_init())
    yield


app = FastAPI(
    title="DOCS-CHAT-BOT",
    root_path="/api",
    lifespan=lifespan
)

origins = [
    f"http://{settings.SERVER_DOMAIN}",
    f"https://{settings.SERVER_DOMAIN}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

include_routers(app)

@app.get("/ping")
async def ping():
    return {"message": "pong"}
