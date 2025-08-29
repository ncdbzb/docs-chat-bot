from pydantic import BaseModel, Field, model_validator


class TestRequest(BaseModel):
    collection_name: str = Field(..., description="ID документа / имя коллекции в ChromaDB")


class TestResponse(BaseModel):
    question: str
    option_1: str = Field(..., alias="1 option")
    option_2: str = Field(..., alias="2 option")
    option_3: str = Field(..., alias="3 option")
    option_4: str = Field(..., alias="4 option")
    right_answer: str = Field(..., alias="right answer")

    @model_validator(mode="after")
    def check_validity(self):
        options = [self.option_1, self.option_2, self.option_3, self.option_4]

        if self.right_answer not in options:
            raise ValueError(
                f"Поле right_answer='{self.right_answer}' не совпадает ни с одним из вариантов: {options}"
            )

        if len(set(options)) < len(options):
            raise ValueError(f"Варианты ответа содержат дубликаты: {options}")

        return self
