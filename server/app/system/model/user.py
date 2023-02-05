from sqlalchemy import Column, String, Boolean

from app.core.base import BaseModel

# OAuth2 规定在使用「password 流程」时，客户端/用户必须将 username 和 password 字段作为表单数据发送。
# 而且规范明确了字段必须这样命名。因此 user-name 或 email 是行不通的。


class User(BaseModel):
    __tablename__ = "user"

    username = Column(String(255), unique=True, index=True, comment='用户名')
    password = Column(String(255), comment='密码')
    name = Column(String(255), comment='名称')
    email = Column(String(255), index=True, comment='邮箱')
    is_admin = Column(Boolean, default=False, comment="是否管理员")
    domain = Column(String(255), index=True, comment='域')
