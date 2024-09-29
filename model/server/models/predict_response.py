from pydantic import BaseModel


class PredictResponse(BaseModel):
    answer: str
    class_1: str
    class_2: str
