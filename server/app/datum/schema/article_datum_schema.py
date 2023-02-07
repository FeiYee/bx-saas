from datetime import datetime
from pydantic import BaseModel


class ArticleDatumSchema(BaseModel):
    id: str | None = None
    article_id: str | None = None
    user_id: str | None = None
    url: str | None = None
    type: int | None = None
    keyword: int | None = None
    file_name: str | None = None
    file_path: str | None = None
    file_size: str | None = None
    file_type: str | None = None
    upload_date: datetime | None = None

    class Config:
        orm_mode = True
