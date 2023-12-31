from sqlalchemy import Boolean, Column, Integer, String

from app.core.base import BaseModel


class ArticleExtract(BaseModel):
    """
    论文提取文件
    """

    __tablename__ = "article_extract"

    article_id = Column(String(32), index=True, comment='文章ID')
    url = Column(String(255), unique=True, comment='URL')
    type = Column(Integer, default=0, comment="文件类型: 0->image, 1->excel, 2->pdf, 3->zip")
    file_name = Column(String(255), comment='文件名称')
    file_path = Column(String(255), comment='文件路径')
    file_size = Column(String(255), comment='文件大小')
    file_type = Column(String(255), default='', comment="文件类型")
