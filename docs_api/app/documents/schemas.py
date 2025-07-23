import uuid
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

    @staticmethod
    def create_id():
        return str(uuid.uuid4())
