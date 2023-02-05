from pydantic import BaseModel


class ArticleSchema(BaseModel):
    id: str | None = None
    name: str | None = None
    title: str | None = None
    summary: str | None = None
    content: str | None = None
    author: str | None = None
    date: str | None = None
    molecular: str | None = None
    journal: str | None = None
    doi: str | None = None
    pmid: str | None = None
    relate_count: int | None = None
    result: str | None = None
    effect: str | None = None
    sample_count: str | None = None
    indicator: str | None = None
    group: str | None = None
    drugs: str | None = None
    disease: str | None = None
    side_effect: str | None = None
    microbe: str | None = None
    cell: str | None = None
    gene: str | None = None
    pathway_target: str | None = None

    class Config:
        orm_mode = True
