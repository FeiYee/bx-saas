from typing import Type, TypeVar, List
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..model.datum import Datum
from ..schema.datum_schema import DatumSchema


DatumModelType = TypeVar("DatumModelType", bound=Datum)


class ArticleService:

    def __init__(self, model: Type[DatumModelType]):
        self.model = model

    def find(self, datum_schema: DatumSchema, db: Session) -> list[tuple[Datum]]:
        data = jsonable_encoder(datum_schema, exclude_unset=True)
        datums = db.query(self.model).all()
        return datums

    def get_article(self, *, title: str) -> List[str]:
        title_list = ['abc', 'ddd', 'ccc']
        return title_list

    def get_article_title(self, *, title: str) -> List[str]:
        title_list = ['abc', 'ddd', 'ccc']
        return title_list


article_service = ArticleService(Datum)
