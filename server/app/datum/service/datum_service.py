from typing import Type, TypeVar
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from config import BASE_DIR
from app.core.util import write_file
from ..model.datum import Datum
from ..schema.datum_schema import DatumSchema


DatumModelType = TypeVar("DatumModelType", bound=Datum)


class DatumService:

    def __init__(self, model: Type[DatumModelType]):
        self.model = model

    def find(self, db: Session) -> list[tuple[Datum]]:
        datums = db.query(self.model).all()
        return datums

    async def create(self, article_id: str, file: UploadFile, db: Session) -> Datum:
        file_path = await write_file(file=file, write_path='datum', write_sub_path=article_id)

        datum = self.model()
        datum.article_id = article_id
        datum.title = file.filename
        datum.url = str('/' / file_path.relative_to(BASE_DIR)).replace('\\', '/')
        datum.file_name = file.filename
        datum.file_path = str(file_path)
        datum.file_type = file.content_type
        datum.file_size = file_path.stat().st_size()

        db.add(datum)
        db.commit()
        db.refresh(datum)
        return datum

    def update(self, datum_id: str, datum_schema: DatumSchema, db: Session) -> Datum:
        data = jsonable_encoder(datum_schema, exclude_unset=True, exclude=['id'])
        datum = db.query(self.model).get(datum_id)
        for field in data:
            setattr(datum, field, data[field])
        db.commit()
        db.refresh(datum)
        return datum

    def delete(self, *, datum_id: str, db: Session) -> Datum:
        datum = db.query(self.model).get(datum_id)
        setattr(datum, 'deleted_at', func.now())
        db.delete(datum)
        db.commit()
        return datum

    def remove(self, *, datum_id: str, db: Session) -> Datum:
        datum = db.query(self.model).get(datum_id)
        db.delete(datum)
        db.commit()
        return datum

    def find_by_article(self, *, article_id: str, db: Session) -> Datum:
        datum = db.query(self.model).filter(self.model.article_id == article_id).first()
        return datum


datum_service = DatumService(Datum)
