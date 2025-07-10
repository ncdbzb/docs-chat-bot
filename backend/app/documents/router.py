from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.documents.service import save_document
from app.documents.schemas import DocumentCreateResponse
from app.database import get_async_session
from app.auth.models import AuthUser
from app.auth.auth_config import current_superuser


router = APIRouter()

@router.post("/upload", response_model=DocumentCreateResponse)
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
