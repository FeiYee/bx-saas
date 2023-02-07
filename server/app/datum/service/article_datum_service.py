from typing import Type, TypeVar
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from config import BASE_DIR
from app.core.util import write_file

from ..model.article_datum import ArticleDatum
from ..schema.article_datum_schema import ArticleDatumSchema


ArticleDatumModelType = TypeVar("ArticleDatumModelType", bound=ArticleDatum)


class ArticleDatumService:

    def __init__(self, model: Type[ArticleDatumModelType]):
        self.model = model

    def find(self, article_id: str, db: Session) -> list[tuple[ArticleDatum]]:
        article_datums = db.query(self.model).filter(self.model.article_id == article_id).all()
        return article_datums

    async def create(self, article_id: str, file: UploadFile, db: Session) -> ArticleDatum:
        file_path = await write_file(file=file, write_path='article_datum', write_sub_path=article_id)

        article_datum = self.model()
        article_datum.article_id = article_id
        article_datum.keyword = article_id
        article_datum.url = str('/' / file_path.relative_to(BASE_DIR)).replace('\\', '/')
        article_datum.file_name = file.filename
        article_datum.file_path = str(file_path)
        article_datum.file_type = file.content_type
        article_datum.file_size = file_path.stat().st_size

        if 'image' in file.content_type:
            article_datum.type = 0
        elif 'sheet' in file.content_type:
            article_datum.type = 1
        elif 'pdf' in file.content_type:
            article_datum.type = 2
        elif 'zip' in file.content_type:
            article_datum.type = 3

        db.add(article_datum)
        db.commit()
        db.refresh(article_datum)
        return article_datum

    def update(self, article_datum_id: str, datum_schema: ArticleDatumSchema, db: Session) -> ArticleDatum:
        data = jsonable_encoder(datum_schema, exclude_unset=True, exclude=['id'])
        article_datum = db.query(self.model).get(article_datum_id)
        for field in data:
            setattr(article_datum, field, data[field])
        db.commit()
        db.refresh(article_datum)
        return article_datum

    def delete(self, *, article_datum_id: str, db: Session) -> ArticleDatum:
        article_datum = db.query(self.model).get(article_datum_id)
        setattr(article_datum, 'deleted_at', func.now())
        db.delete(article_datum)
        db.commit()
        return article_datum

    def remove(self, *, article_datum_id: str, db: Session) -> ArticleDatum:
        article_datum = db.query(self.model).get(article_datum_id)
        db.delete(article_datum)
        db.commit()
        return article_datum

    def download(self, *, article_datum_id: str, db: Session) -> ArticleDatum:
        article_datum = db.query(self.model).get(article_datum_id)
        return article_datum


article_datum_service = ArticleDatumService(ArticleDatum)
