from pydantic import BaseModel


class DatumSchema(BaseModel):
    id: str | None = None
    title: str
    file_name: str | None = None
    url: str | None = None
    file_path: str | None = None

    class Config:
        orm_mode = True
