from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SearchSchema(BaseModel):
    id: str | None = None
    keyword: str
    user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class SearchResultSchema(BaseModel):
    keyword: str
    data: list | None = None

    class Config:
        orm_mode = True
