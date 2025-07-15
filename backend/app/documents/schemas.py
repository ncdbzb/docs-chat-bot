import re
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class DocumentCreateResponse(BaseModel):
    id: UUID
    name: str
    original_filename: str
    type: str
    size: int
    created_at: datetime

    class Config:
        from_attributes = True


class Document(BaseModel):
    id: UUID
    name: str
    original_filename: str
    type: str
    size: int
    description: str | None
    user_id: UUID
    storage_key: str
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentShort(BaseModel):
    name: str
    description: str | None

    class Config:
        from_attributes = True


class DocumentUpdate(BaseModel):
    current_name: str = Field(..., description="Текущее имя документа")
    new_name: str | None = Field(None, description="Новое имя документа (опционально)")
    description: str | None = Field(None, description="Новое описание документа (опционально)")

    @field_validator('new_name')
    def validate_filename(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if not (1 <= len(value) <= 255):
            raise ValueError("Имя должно содержать от 1 до 255 символов")

        forbidden_pattern = r'[<>:"/\\|?*\x00-\x1F]'
        if re.search(forbidden_pattern, value):
            raise ValueError("Имя содержит недопустимые символы: <>:\"/\\|?* или управляющие символы")

        return value
