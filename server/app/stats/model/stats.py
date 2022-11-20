
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Stats(BaseModel):

    __tablename__ = "stats"

    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    total = Column(Integer)
