from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.core.base import BaseModel

# OAuth2 规定在使用「password 流程」时，客户端/用户必须将 username 和 password 字段作为表单数据发送。
# 而且规范明确了字段必须这样命名。因此 user-name 或 email 是行不通的。


class Website(BaseModel):
    __tablename__ = "website"

    org = Column(String, unique=True, index=True, comment='用户名')
    password = Column(String, comment='密码')
    name = Column(String, comment='名称')
    email = Column(String, unique=True, index=True, comment='邮箱')
