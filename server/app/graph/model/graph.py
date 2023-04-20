from sqlalchemy import Boolean, Column, Integer, String, TEXT
from app.core.base import BaseModel


class Graph(BaseModel):
    __tablename__ = "graph"

    article_id = Column(String(32), index=True, comment='文章ID')
    ent1 = Column(String(255), comment='文章标题')
    rela = Column(String(255), comment='文章标题')
    ent2 = Column(String(255), comment='文章标题')
