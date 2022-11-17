from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Datum(BaseModel):
    __tablename__ = "datum"

    title = Column(String, index=True, comment='标题')
    url = Column(String, unique=True, comment='URL')
    file_name = Column(String, index=True, comment='文件名称')
    file_path = Column(String, comment='文件路径')
    file_type = Column(String, comment='文件类型')
    file_size = Column(String, comment='文件大小')
