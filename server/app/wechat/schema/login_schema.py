from datetime import datetime
from pydantic import BaseModel


class LoginSchema(BaseModel):
    code: str
    info: str | None = None

    class Config:
        orm_mode = True
