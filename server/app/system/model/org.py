
from sqlalchemy import Column, String

from app.core.base import BaseModel


class Org(BaseModel):

    __tablename__ = "org"

    code = Column(String(255), index=True, comment='编码')
    name = Column(String(255), comment='名称')
    logo = Column(String(255), comment='Logo, Base64编码图片')
    abbreviation = Column(String(255), comment='简称')
