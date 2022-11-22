from typing import Type, TypeVar
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from config import BASE_DIR
from ..model.datum import Datum
from ..schema.datum_schema import DatumSchema


DatumModelType = TypeVar("DatumModelType", bound=Datum)


class DatumService:

    def __init__(self, model: Type[DatumModelType]):
        self.model = model

    def find(self, db: Session) -> list[tuple[Datum]]:
        datums = db.query(self.model).all()
        return datums

    async def create(self, file: UploadFile, title: str, db: Session) -> Datum:
        content = await file.read()
        file_path = BASE_DIR / 'asset' / file.filename
        file_path.write_bytes(content)

        datum = self.model()
        datum.title = title
        datum.file_name = file.filename
        datum.url = str('/' / file_path.relative_to(BASE_DIR))
        datum.file_path = str(file_path)
        # datum.file_size = file_path.stat().st_size()

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
        db.commit()
        return datum

    def remove(self, *, datum_id: str, db: Session) -> Datum:
        datum = db.query(self.model).get(datum_id)
        db.delete(datum)
        db.commit()
        return datum

    def download(self, *, title: str, db: Session) -> Datum:
        datum = db.query(self.model).filter(self.model.title == title).first()
        return datum

    def download_excel(self, *, title: str) -> any:
        datum = {"title", title}

        return datum


datum_service = DatumService(Datum)
