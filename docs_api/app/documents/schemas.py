import uuid
from typing import Any
from pydantic import BaseModel


class DocumentIngestionRequest(BaseModel):
    document_id: uuid.UUID
    storage_key: str
    original_filename: str


class CollectionListResponse(BaseModel):
    collections: list[str]


class Chunk(BaseModel):
    id: str
    text: str
    section: str | None = None
    source: str | None = None
    page_number: int | None = None
    element_type: str | None = None
    metadata: dict[str, Any] | None = None

    @staticmethod
    def create_id() -> str:
        return str(uuid.uuid4())
