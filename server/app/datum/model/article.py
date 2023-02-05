from sqlalchemy import Boolean, Column, Integer, String, TEXT
from app.core.base import BaseModel


class Article(BaseModel):
    __tablename__ = "article"

    name = Column(String(1024), index=True, comment='名称')
    title = Column(String(1024), index=True, comment='文章标题')
    summary = Column(TEXT, default='', comment='摘要')
    content = Column(TEXT, default='', comment='内容')
    author = Column(String(255), default='', index=True, comment='作者')
    date = Column(String(255), default='', comment='Date')
    molecular = Column(String(1024), default='', comment='机理')
    journal = Column(String(255), default='', comment='期刊')
    doi = Column(String(255), default='', comment='DOI')
    pmid = Column(String(255), default='', comment='PMID')
    relate_count = Column(Integer, default=0, comment='被引次数')
    result = Column(String(1024), default='', comment='结论')
    effect = Column(String(1024), default='', comment='疗效')
    sample_count = Column(String(255), default='', comment='样本量')
    indicator = Column(String(1024), default='', comment='临床指标')
    group = Column(String(1024), default='', comment='分组')
    drugs = Column(String(1024), default='', comment='药物')
    disease = Column(String(1024), default='', comment='疾病')
    side_effect = Column(String(1024), default='', comment='副作用')
    microbe = Column(String(1024), default='', comment='微生物')
    cell = Column(String(1024), default='', comment='细胞')
    gene = Column(String(1024), default='', comment='基因')
    pathway_target = Column(String(1024), default='', comment='通路/靶标')


# `title` longtext CHARACTER SET utf8 NOT NULL,
# `summary` longtext CHARACTER SET utf8,
# `author` longtext CHARACTER SET utf8,
# `Date` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `Molecular` longtext CHARACTER SET utf8,
# `期刊` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `Doi` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `PMID` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `被引次数` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `结论-Result` longtext CHARACTER SET utf8,
# `疗效` longtext CHARACTER SET utf8,
# `样本量-Sample Count` longtext CHARACTER SET utf8,
# `临床指标-Indicator` longtext CHARACTER SET utf8,
# `分组-Group` longtext CHARACTER SET utf8,
# `药物-Drugs` longtext CHARACTER SET utf8,
# `疾病-Disease` longtext CHARACTER SET utf8,
# `副作用-Side Effect` longtext CHARACTER SET utf8,
# `微生物` longtext CHARACTER SET utf8,
# `细胞` longtext CHARACTER SET utf8,
# `基因-Gene` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `通路/靶标-Pathway/Target` varchar(255) CHARACTER SET utf8 DEFAULT NULL
# `index_file` longtext CHARACTER SET utf8,
