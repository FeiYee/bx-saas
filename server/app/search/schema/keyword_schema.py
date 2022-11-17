from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class KeywordSchema(BaseModel):
    id: Optional[str] = None
    keyword: str
    user_id: Optional[str] = None
    org_id: Optional[str] = None
    is_preset: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
