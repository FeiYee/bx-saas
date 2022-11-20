
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class OrgUser(BaseModel):

    __tablename__ = "org_user"

    org_id = Column(String(32), index=True)
    user_id = Column(String(32))

    # org = relationship("Org", back_populates="org")
    # user = relationship("User", back_populates="user")
