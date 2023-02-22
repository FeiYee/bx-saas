from sqlalchemy import Boolean, Column, Integer, String, DateTime, func

from app.core.base import BaseModel


class ArticleDatum(BaseModel):
    """
    论文相关文件
    """

    __tablename__ = "article_datum"

    article_id = Column(String(32), index=True, comment='文章ID')
    user_id = Column(String(32), default=None, comment='用户ID')
    url = Column(String(255), unique=True, comment='URL')
    type = Column(Integer, default=0, comment="文件类型: 0->image, 1->excel, 2->pdf, 3->zip, 4->other")
    content_type = Column(Integer, default=0, comment="内容类型: 0->全文, 1->摘要")
    keyword = Column(String(255), comment='关键字')
    file_name = Column(String(255), comment='文件名称')
    file_path = Column(String(255), comment='文件路径')
    file_size = Column(String(255), comment='文件大小')
    file_type = Column(String(255), comment='文件类型')
    upload_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='上传日期')
