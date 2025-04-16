from pydantic import BaseModel


class MessageError(BaseModel):
    detail: str
