from models.base import BaseModel


class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool
