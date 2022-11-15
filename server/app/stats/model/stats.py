
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Stats(BaseModel):

    __tablename__ = "stats"

    title = Column(String, index=True)
    description = Column(String, index=True)
    total = Column(Integer)
