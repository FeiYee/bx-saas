from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class KeywordSchema(BaseModel):
    id: str | None = None
    keyword: str
    weight: int | None = None
    # type: int | None = None
    is_preset: bool | None = False
    user_id: str | None = None
    org_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
