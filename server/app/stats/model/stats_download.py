
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class StatsDownload(BaseModel):

    __tablename__ = "stats_download"

    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    total = Column(Integer)
