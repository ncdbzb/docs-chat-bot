from fastapi import APIRouter, Depends, status

from app.documents.schemas import DocumentIngestionRequest
from app.documents.service import ingest_document, delete_collection
from app.dependencies.minio import get_minio_client, MinioClient
from app.dependencies.chromadb_manager import get_chromadb_manager, ChromaDBManager


router = APIRouter()


@router.post("/ingest", status_code=status.HTTP_200_OK)
async def ingest(
    request: DocumentIngestionRequest,
    minio_client: MinioClient = Depends(get_minio_client),
    chromadb_manager: ChromaDBManager = Depends(get_chromadb_manager)
):
    await ingest_document(
        request=request,
        minio_client=minio_client,
        chromadb_manager=chromadb_manager,
    )
    return {"detail": "Document successfully ingested"}


@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
async def delete(
    document_id: str,
    chromadb_manager: ChromaDBManager = Depends(get_chromadb_manager)
):
    await delete_collection(document_id, chromadb_manager)
    return {"detail": f"Collection {document_id} successfully deleted"}
