from typing import Type, Any
from pydantic import BaseModel
from app.system.model.user import User
from app.system.model.org import Org


class TokenPayload(BaseModel):
    sub: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
    grant_type: str = 'password'


class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str
    domain: str


class UserSchema(BaseModel):
    id: str
    username: str
    email: str
    domain: str

    class Config:
        orm_mode = True


class UserDetailSchema(BaseModel):
    user: Any | None = None
    org: Any | None = None
