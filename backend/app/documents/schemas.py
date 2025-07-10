from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class DocumentCreateResponse(BaseModel):
    id: UUID
    name: str
    original_filename: str
    type: str
    size: int
    created_at: datetime

    class Config:
        from_attributes = True
