from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.services.upload import save_document
from app.documents.services.get_docs import get_user_documents, get_all_documents
from app.documents.schemas import DocumentCreateResponse
from app.database import get_async_session
from app.auth.models import AuthUser
from app.auth.auth_config import current_superuser, current_user


router = APIRouter()

@router.post(
    "/upload",
    response_model=DocumentCreateResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_document(
    doc_name: str = Form(...),
    doc_description: str = Form(...),
    file: UploadFile = File(...),
    user: AuthUser = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session)
):
    return await save_document(
        file=file,
        user=user,
        session=session,
        doc_name=doc_name,
        doc_description=doc_description,
    )


@router.get("/my", status_code=status.HTTP_200_OK)
async def get_my_documents(
    user: AuthUser = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await get_user_documents(user=user, session=session)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_admin_documents(
    user: AuthUser = Depends(current_superuser),
    session: AsyncSession = Depends(get_async_session)
):
    return await get_all_documents(session=session)
