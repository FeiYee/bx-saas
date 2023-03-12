from sqlalchemy import Boolean, Column, Integer, String, TEXT, DateTime, func
from app.core.base import BaseModel


class Paper(BaseModel):
    """
    材料，资料
    """

    __tablename__ = "paper"

    user_id = Column(String(32), default=None, comment='用户ID')
    name = Column(String(1024), comment='名称')
    description = Column(TEXT, default='', comment='描述')
    url = Column(String(255), unique=True, comment='URL')
    type = Column(Integer, default=0, comment="文件类型: 0->image, 1->excel, 2->pdf, 3->zip, 4->other")
    file_name = Column(String(255), comment='文件名称')
    file_path = Column(String(255), comment='文件路径')
    file_size = Column(String(255), comment='文件大小')
    file_type = Column(String(255), comment='文件类型')
    upload_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='上传日期')
    group = Column(String(1024), default='', comment='分组')
