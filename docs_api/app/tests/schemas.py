from pydantic import BaseModel, Field


class TestRequest(BaseModel):
    collection_name: str = Field(..., description="ID документа / имя коллекции в ChromaDB")


class TestResponse(BaseModel):
    question: str
    option_1: str = Field(..., alias="1 option")
    option_2: str = Field(..., alias="2 option")
    option_3: str = Field(..., alias="3 option")
    option_4: str = Field(..., alias="4 option")
    right_answer: str = Field(..., alias="right answer")
