from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Keyword(BaseModel):
    __tablename__ = "keyword"

    keyword = Column(String, index=True)
    user_id = Column(String)
    org_id = Column(String)
    is_preset = Column(Boolean, default=True)
