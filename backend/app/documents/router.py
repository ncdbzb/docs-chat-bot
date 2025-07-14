from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.minio_client import MinioClient
from app.clients.repository_client import DocumentRepository
from app.dependencies.minio import get_minio_client
from app.dependencies.repository import get_document_repository
from app.documents.services.upload import save_document
from app.documents.services.get_docs import get_user_documents, get_all_documents
from app.documents.services.delete import delete_document
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
    user: AuthUser = Depends(current_user),
    minio_client: MinioClient = Depends(get_minio_client),
    repo: DocumentRepository = Depends(get_document_repository),
):
    return await save_document(
        file=file,
        user=user,
        doc_name=doc_name,
        doc_description=doc_description,
        minio_client=minio_client,
        repo=repo,
    )


@router.get("/my", status_code=status.HTTP_200_OK)
async def get_my_documents(
    user: AuthUser = Depends(current_user),
    repo: DocumentRepository = Depends(get_document_repository),
):
    return await get_user_documents(user=user, repo=repo)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_admin_documents(
    user: AuthUser = Depends(current_superuser),
    repo: DocumentRepository = Depends(get_document_repository)
):
    return await get_all_documents(repo=repo)


@router.delete(
    '/delete-my',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def del_my_docs(
    doc_name: str = Query(..., description="Exact name of the document to delete"),
    user: AuthUser = Depends(current_user),
    minio_client: MinioClient = Depends(get_minio_client),
    repo: DocumentRepository = Depends(get_document_repository),
):
    await delete_document(doc_name=doc_name, user=user, repo=repo, minio_client=minio_client)
