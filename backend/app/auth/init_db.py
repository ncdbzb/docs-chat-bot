import httpx
import asyncio
from sqlalchemy import select

from app.config import settings
from app.logger import logger
from app.auth.models import user as user_table
from app.database import async_session_maker


async def init_admin_user(
    register_url: str = f"http://backend:{settings.BACKEND_PORT}/auth/register",
) -> None:
    """
    Создание пользователя-админа при старте, если он не существует.
    """

    async with async_session_maker() as session:
        result = await session.execute(
            select(user_table).where(user_table.c.email == settings.ADMIN_EMAIL)
        )
        if result.scalar_one_or_none():
            return

    admin_user_data = {
        "email": settings.ADMIN_EMAIL,
        "password": settings.ADMIN_PASSWORD,
        "confirmation_password": settings.ADMIN_PASSWORD,
        "name": "admin",
        "surname": "admin",
        "is_superuser": True,
        "is_verified": True,
        "is_active": True,
        "role": "manager"
    }

    max_retries = 3
    retry_delay = 3

    for attempt in range(1, max_retries + 1):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url=register_url,
                    json=admin_user_data,
                    timeout=10.0,
                )
                if response.status_code == 201:
                    logger.info(f"Администратор '{settings.ADMIN_EMAIL}' успешно зарегистрирован.")
                    return
                elif response.status_code == 400:
                    logger.info(f"Администратор '{settings.ADMIN_EMAIL}' уже существует.")
                    return
                else:
                    logger.error(f"[{attempt}] Ошибка регистрации админа: {response.status_code} — {response.text}")
            except httpx.RequestError as e:
                logger.error(f"[{attempt}] Ошибка соединения при регистрации админа: {str(e)}")

        if attempt < max_retries:
            await asyncio.sleep(retry_delay)

    logger.error("Все попытки создать администратора завершились неудачей.")

async def delayed_admin_init():
    await asyncio.sleep(1)
    await init_admin_user()
