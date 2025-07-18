from uuid import UUID
from fastapi import APIRouter, Depends, status

from app.admin_requests.schemas import AdminRequest, RequestIdSchema
from app.admin_requests.services.admin_service import get_all_pending_requests, accept_request_by_id, reject_request_by_id
from app.admin_requests.admin_repository import AdminRepository
from app.dependencies.repository import get_admin_repository


router = APIRouter()


@router.get(
    "/requests",
    response_model=list[AdminRequest],
    status_code=status.HTTP_200_OK,
)
async def fetch_pending_requests(
    repo: AdminRepository = Depends(get_admin_repository)
):
    return await get_all_pending_requests(repo)


@router.post("/accept", status_code=status.HTTP_204_NO_CONTENT)
async def accept_request(
    data: RequestIdSchema,
    repo: AdminRepository = Depends(get_admin_repository),
):
    await accept_request_by_id(repo, data.request_id)


@router.post("/reject", status_code=status.HTTP_204_NO_CONTENT)
async def reject_request(
    data: RequestIdSchema,
    repo: AdminRepository = Depends(get_admin_repository),
):
    await reject_request_by_id(repo, data.request_id)
