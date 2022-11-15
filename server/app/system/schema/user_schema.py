from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    username: str
    password: str
    name: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
