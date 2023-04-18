from sqlalchemy import Boolean, Column, Integer, String, TEXT
from app.core.base import BaseModel


class Graph(BaseModel):
    __tablename__ = "graph"

    title = Column(String(255), comment='文章标题')
    ent1 = Column(String(255), comment='起始实体')
    rela = Column(String(255), comment='关系')
    ent2 = Column(String(255), comment='目标实体')