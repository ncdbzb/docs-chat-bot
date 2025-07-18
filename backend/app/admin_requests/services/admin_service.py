from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi_users.jwt import generate_jwt

from app.admin_requests.admin_repository import AdminRepository
from app.admin_requests.schemas import AdminRequest, UserInfo
from app.auth.models import AuthUser
from app.config import settings
from app.tasks.email_task import send_email
from app.logger import logger


async def get_all_pending_requests(repo: AdminRepository) -> list[AdminRequest]:
    try:
        return await repo.get_pending_requests()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail=f"Ошибка БД при получении заявок")
    except Exception:
        logger.exception("Ошибка при получении заявок")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


async def add_pending_request(session: AsyncSession, user: AuthUser):
    repo = AdminRepository(session)
    user_info = UserInfo(
        name=user.name,
        surname=user.surname,
        email=user.email
    )
    try:
        return await repo.add_request(user_id=user.id, user_info=user_info)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail=f"Ошибка БД при добавлении заявки")
    except Exception:
        logger.exception("Ошибка при добавлении заявок")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


async def accept_request_by_id(repo: AdminRepository, request_id: UUID) -> None:
    try:
        values = await repo.accept_request(request_id)
        if not values:
            raise HTTPException(status_code=404, detail="Request not found")

        user_email = values["info"]["email"]
        name = values["info"].get("name")
        token_data = {
            "sub": str(values["user_id"]),
            "email": user_email,
            "aud": "fastapi-users:verify",
        }
        token = generate_jwt(
            token_data,
            settings.SECRET_MANAGER,
            lifetime_seconds=settings.VERIFY_URL_LIFETIME_SECONDS,
        )

        send_email.delay(name=name, user_email=user_email, token=token, destiny="accept")
        logger.info(f'Заявка на регистрацию {request_id} успешно принята')
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail=f"Ошибка при одобрении заявки")
    except Exception:
        logger.exception("Ошибка при одобрении заявок")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


async def reject_request_by_id(repo: AdminRepository, request_id: UUID) -> None:
    try:
        result = await repo.reject_request(request_id)
        if not result:
            raise HTTPException(status_code=404, detail="Request not found")
        logger.info(f'Заявка на регистрацию {request_id} успешно отклонена')
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail=f"Ошибка при отклонении заявки")
    except Exception:
        logger.exception("Ошибка при одобрении заявок")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
