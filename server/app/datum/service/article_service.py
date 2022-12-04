from typing import Type, TypeVar, List
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from config import NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD
from app.graph.service.graph_service import GraphNeo
from ..model.datum import Datum
from ..schema.datum_schema import DatumSchema


DatumModelType = TypeVar("DatumModelType", bound=Datum)

graph_service = GraphNeo(NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD)


class ArticleService:

    def __init__(self, model: Type[DatumModelType]):
        self.model = model

    def find(self, datum_schema: DatumSchema, db: Session) -> list[tuple[Datum]]:
        data = jsonable_encoder(datum_schema, exclude_unset=True)
        datums = db.query(self.model).all()
        return datums

    def get_article(self, *, title: str = '') -> List[str]:
        title_list = graph_service.total_table["Title"].values
        return title_list

    def get_article_title(self, *, title: str) -> List[str]:
        print(graph_service.total_table)
        title_list = list(graph_service.total_table["Title"].values)
        return title_list


article_service = ArticleService(Datum)
