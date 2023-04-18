from sqlalchemy import Boolean, Column, Integer, String, TEXT
from app.core.base import BaseModel


class Graph(BaseModel):
    __tablename__ = "graph"

    title = Column(String(255), comment='文章标题')
    ent1 = Column(String(255), comment='文章标题')
    rela = Column(String(255), comment='文章标题')
    ent2 = Column(String(255), comment='文章标题')