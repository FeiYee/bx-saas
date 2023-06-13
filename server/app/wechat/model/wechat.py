from sqlalchemy import Column, String, Boolean

from app.core.base import BaseModel


class Wechat(BaseModel):
    __tablename__ = "wechat"

    user_id = Column(String(32), comment='用户ID')
    openid = Column(String(255), comment='用户唯一标识')
    unionid = Column(String(255), comment='开放平台的唯一标识符')
    session_key = Column(String(255), comment='会话密钥')
