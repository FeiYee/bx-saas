from pydantic import BaseModel


class OrgSchema(BaseModel):
    code: str
    name: str
    logo: str | None = None

    class Config:
        orm_mode = True
