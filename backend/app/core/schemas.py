from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field


class GetTestBase(BaseModel):
    question: str
    option_1: str = Field(..., alias="1 option")
    option_2: str = Field(..., alias="2 option")
    option_3: str = Field(..., alias="3 option")
    option_4: str = Field(..., alias="4 option")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class GetTestInnerResult(GetTestBase):
    id: UUID = Field(default_factory=uuid4)
    right_answer: str = Field(..., alias="right answer")


class GetTestInnerPublicResult(GetTestBase):
    pass


class GetTestRequest(BaseModel):
    filename: str


class GetTestResponse(BaseModel):
    result: GetTestInnerPublicResult
    request_id: str


class GetQARequest(BaseModel):
    filename: str
    question: str


class GetQAResponse(BaseModel):
    result: str
    request_id: str


class CheckTestRequest(BaseModel):
    request_id: UUID
    selected_option: str


class CheckTestResponse(BaseModel):
    right_answer: str