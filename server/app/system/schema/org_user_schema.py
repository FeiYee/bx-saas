from pydantic import BaseModel
from .org_schema import OrgSchema
from .user_schema import UserSchema


class OrgUserSchema(BaseModel):
    org_id: str | None = None
    user_id: str | None = None
    org_name: str | None = None
    user_name: str | None = None
    org: OrgSchema | None = None
    user: UserSchema | None = None

    class Config:
        orm_mode = True
