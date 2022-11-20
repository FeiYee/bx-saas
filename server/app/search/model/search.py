from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Search(BaseModel):
    __tablename__ = "search"

    keyword = Column(String(255), index=True, comment='关键词')
    count = Column(Integer, default=1, comment='搜索次数')
    type = Column(Integer, default=0, comment="0:图谱, 1:文章")
    user_id = Column(String(32), comment='用户ID')

