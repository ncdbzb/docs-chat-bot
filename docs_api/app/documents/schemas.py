from pydantic import BaseModel
from uuid import UUID


class DocumentIngestionRequest(BaseModel):
    document_id: UUID
    storage_key: str
    original_filename: str
