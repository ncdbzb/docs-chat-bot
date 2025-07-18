from uuid import UUID
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.admin_requests.models import admin_requests, AdminRequestStatus
from app.admin_requests.schemas import UserInfo, AdminRequest
from app.logger import logger


class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_pending_requests(self) -> list[AdminRequest]:
        try:
            stmt = select(admin_requests).where(admin_requests.c.status == AdminRequestStatus.pending)
            result = await self.session.execute(stmt)
            return result.mappings().all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении ожидающих заявок: {e}")
            raise

    async def add_request(self, user_id: UUID, user_info: UserInfo) -> AdminRequest:
        try:
            stmt = insert(admin_requests).values(
                user_id=user_id,
                status=AdminRequestStatus.pending,
                info=user_info.model_dump()
            ).returning(admin_requests)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.mappings().first()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении заявки: {e}")
            raise

    async def accept_request(self, request_id: UUID) -> dict | None:
        try:
            stmt = (
                update(admin_requests)
                .where(admin_requests.c.id == request_id)
                .values(status=AdminRequestStatus.approved)
                .returning(admin_requests)
            )
            result = await self.session.execute(stmt)
            values = result.mappings().first()
            await self.session.commit()
            return values
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при одобрении заявки (id={request_id}): {e}")
            raise

    async def reject_request(self, request_id: UUID) -> bool:
        try:
            stmt = (
                update(admin_requests)
                .where(admin_requests.c.id == request_id)
                .values(status=AdminRequestStatus.rejected)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при отклонении заявки (id={request_id}): {e}")
            raise
