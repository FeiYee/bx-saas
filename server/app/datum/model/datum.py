from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Datum(BaseModel):
    __tablename__ = "datum"

    title = Column(String, index=True, comment='标题')
    name = Column(String, index=True, comment='名称')
    url = Column(String, unique=True, comment='URL')
    path = Column(String, comment='路径')
    type = Column(String, comment='类型')
    size = Column(String, comment='大小')
