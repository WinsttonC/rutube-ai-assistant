from pydantic import BaseModel


class IndexResponse(BaseModel):
    text: str
