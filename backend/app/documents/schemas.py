import re
from uuid import UUID
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel, Field, field_validator


def validate_filename(value: str | None) -> str | None:
    if value is None:
        return value

    value = value.strip()

    if not (1 <= len(value) <= 255):
        raise ValueError("Имя должно содержать от 1 до 255 символов")

    forbidden_pattern = r'[<>:"/\\|?*\x00-\x1F]'
    if re.search(forbidden_pattern, value):
        raise ValueError("Имя содержит недопустимые символы: <>:\"/\\|?* или управляющие символы")

    return value


class DocumentBase(BaseModel):
    name: str
    description: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        return validate_filename(v)


class DocumentCreateMeta(DocumentBase):
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str | None = Form(None),
    ):
        return cls(name=name, description=description)


class DocumentCreateResponse(BaseModel):
    id: UUID
    name: str
    original_filename: str
    type: str
    size: int
    created_at: datetime

    class Config:
        from_attributes = True


class Document(DocumentBase):
    id: UUID
    original_filename: str
    type: str
    size: int
    user_id: UUID
    storage_key: str
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentShort(DocumentBase):
    class Config:
        from_attributes = True


class DocumentUpdate(BaseModel):
    current_name: str = Field(..., description="Текущее имя документа")
    new_name: str | None = Field(None, description="Новое имя документа (опционально)")
    description: str | None = Field(None, description="Новое описание документа (опционально)")

    @field_validator("new_name")
    @classmethod
    def validate_new_name(cls, v):
        return validate_filename(v)
