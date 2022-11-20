from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class SearchRecord(BaseModel):
    __tablename__ = "search_record"

    keyword = Column(String, index=True)
    search_id = Column(String)
    search_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='搜索日期')
    user_id = Column(String)
