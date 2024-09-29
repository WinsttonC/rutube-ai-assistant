from pydantic import BaseModel


class PredictRequest(BaseModel):
    question: str
