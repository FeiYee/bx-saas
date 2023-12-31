from pydantic import BaseModel


class DatumSchema(BaseModel):
    id: str | None = None
    article_id: str
    url: str | None = None
    file_name: str | None = None
    file_path: str | None = None
    file_type: str | None = None
    file_size: str | None = None
    title: str | None = None

    class Config:
        orm_mode = True
