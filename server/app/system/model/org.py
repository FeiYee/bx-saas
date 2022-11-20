
from sqlalchemy import Column, String

from app.core.base import BaseModel


class Org(BaseModel):

    __tablename__ = "org"

    code = Column(String, index=True, comment='编码')
    name = Column(String, comment='名称')
    logo = Column(String, comment='Logo, Base64编码图片')
    abbreviation = Column(String, comment='简称')
