from pydantic import BaseModel


class TestResponse(BaseModel):
    response: str
