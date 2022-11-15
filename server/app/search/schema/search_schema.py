from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SearchSchema(BaseModel):
    id: str
    keyword: str
    user: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class SearchResultSchema(BaseModel):
    # id: str
    keyword: str
    data: Optional[list] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
