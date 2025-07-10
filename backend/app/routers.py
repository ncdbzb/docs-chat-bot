from fastapi import FastAPI

from app.auth.auth_config import auth_backend, fastapi_users
from app.auth.schemas import UserRead, UserCreate, UserUpdate
from app.auth.routers.verify_router import router as verify_router
from app.auth.routers.forgot_pass_router import router as forgot_pass_router
from app.documents.router import router as documents_router


def include_routers(app: FastAPI):
    app.include_router(
        fastapi_users.get_auth_router(auth_backend, requires_verification=False),
        prefix="/auth",
        tags=["Auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["Auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )
    app.include_router(verify_router, prefix="/auth", tags=["Auth"])
    app.include_router(forgot_pass_router, prefix="/auth", tags=["Auth"])
    app.include_router(documents_router, prefix="/documents", tags=["Documents"])