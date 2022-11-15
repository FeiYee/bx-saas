from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Search(BaseModel):
    __tablename__ = "search"

    keyword = Column(String, index=True)
    user = Column(String)
    count = Column(Integer, default=0)
    search_date = Column(DateTime, onupdate=func.now(), comment='搜索日期')

