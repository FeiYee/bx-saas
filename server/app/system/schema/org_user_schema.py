from pydantic import BaseModel


class OrgUserSchema(BaseModel):
    org_id: str | None = None
    user_id: str | None = None

    class Config:
        orm_mode = True
