from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.base import BaseModel


class Article(BaseModel):
    __tablename__ = "article"

    title = Column(String(255), index=True, comment='标题')
    summary = Column(String(255), unique=True, comment='summary')
    author = Column(String(255), index=True, comment='author')
    date = Column(String(255), comment='Date')
    molecular = Column(String(255), comment='Molecular')
    journal = Column(String(255), comment='期刊')
    DOI = Column(String(255), comment='Doi')
    PMID = Column(String(255), comment='PMID')
    relate_count = Column(String(255), comment='被引次数')
    result = Column(String(255), comment='结论')
    effect = Column(String(255), comment='疗效')
    sample_count = Column(String(255), comment='样本量')
    indicator = Column(String(255), comment='临床指标')
    group = Column(String(255), comment='分组')
    drugs = Column(String(255), comment='药物')
    disease = Column(String(255), comment='疾病')
    side_effect = Column(String(255), comment='副作用')
    microbe = Column(String(255), comment='微生物')
    gene = Column(String(255), comment='基因')
    pathway_target = Column(String(255), comment='通路/靶标')


# `title` longtext CHARACTER SET utf8 NOT NULL,
# `summary` longtext CHARACTER SET utf8,
# `author` longtext CHARACTER SET utf8,
# `Date` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `Molecular` longtext CHARACTER SET utf8,
# `期刊` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `Doi` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `PMID` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `被引次数` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
# `index_file` longtext CHARACTER SET utf8,
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
