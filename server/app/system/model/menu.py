
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Menu(BaseModel):

    __tablename__ = "menu"

    code = Column(String, index=True)
    name = Column(String)
    url = Column(String)
    parent_id = Column(String)

