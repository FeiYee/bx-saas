from pydantic import BaseModel


class GraphSchema(BaseModel):
    article_id: str
    ent1: str
    rela: str
    ent2: str

