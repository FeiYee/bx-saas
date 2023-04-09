from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: str | None = None
    code: str
    name: str
    logo: str | None = None
    abbreviation: str | None = None

    class Config:
        orm_mode = True
