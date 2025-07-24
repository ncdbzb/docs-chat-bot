from pydantic import BaseModel


class QARequest(BaseModel):
    question: str
    collection_name: str


class QAResponse(BaseModel):
    answer: str
