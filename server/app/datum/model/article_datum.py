from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class ArticleDatum(BaseModel):
    """
    论文相关文件
    """

    __tablename__ = "article_datum"

    article_id = Column(String(32), index=True, comment='文章ID')
    user_id = Column(String(32), default=None, comment='用户ID')
    url = Column(String(255), unique=True, comment='URL')
    file_name = Column(String(255), comment='文件名称')
    file_path = Column(String(255), comment='文件路径')
    file_size = Column(String(255), comment='文件大小')
    file_type = Column(String(255), comment='文件类型: 0->image, 1->excel, 2->pdf, 3->zip')
    upload_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='搜索日期')
