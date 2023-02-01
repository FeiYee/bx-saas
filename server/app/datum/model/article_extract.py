from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class ArticleExtract(BaseModel):
    """
    论文相关文件
    """

    __tablename__ = "article_extract"

    article_id = Column(String(32), index=True, comment='标题')
    title = Column(String(255), comment='标题')
    url = Column(String(255), unique=True, comment='URL')
    file_name = Column(String(255), index=True, comment='文件名称')
    file_path = Column(String(255), comment='文件路径')
    file_type = Column(String(255), comment='文件类型')
    file_size = Column(String(255), comment='文件大小')
