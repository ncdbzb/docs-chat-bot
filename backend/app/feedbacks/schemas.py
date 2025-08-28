from typing import Optional, Literal
from pydantic import BaseModel, UUID4, Field


class FeedbackCreate(BaseModel):
    request_id: UUID4 = Field(..., description="ID запроса")
    value: Literal["like", "dislike"] = Field(..., description="Тип фидбека: like или dislike")
    user_comment: Optional[str] = Field(None, description="Комментарий пользователя")
