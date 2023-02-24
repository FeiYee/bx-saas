from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str | None = None
    username: str
    # password: str | None = None
    name: str | None = None
    email: str | None = None
    domain: str | None = None
    is_admin: bool | None = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
