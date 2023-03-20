from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Keyword(BaseModel):
    __tablename__ = "keyword"

    keyword = Column(String(255), index=True)
    weight = Column(Integer, default=1)
    type = Column(Integer, default=0, comment="0:图谱, 1:资料")
    is_preset = Column(Boolean, default=True)
    user_id = Column(String(32))
    # user_name = Column(String(32))
    org_id = Column(String(32))
    # org_name = Column(String(32))
