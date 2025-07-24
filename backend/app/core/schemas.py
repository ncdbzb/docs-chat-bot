from pydantic import BaseModel


class GetQARequest(BaseModel):
    filename: str
    question: str


class GetQAResponse(BaseModel):
    result: str
    request_id: int
