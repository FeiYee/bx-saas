from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class SearchRecord(BaseModel):
    __tablename__ = "search_record"

    keyword = Column(String, unique=True, index=True)
    search = Column(String)
    user = Column(String)
