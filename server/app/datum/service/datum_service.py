from typing import Type, TypeVar
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..model.datum import Datum
from ..schema.datum_schema import DatumSchema


DatumModelType = TypeVar("DatumModelType", bound=Datum)


class DatumService:

    def __init__(self, model: Type[DatumModelType]):
        self.model = model

    def find(self, datum_schema: DatumSchema, db: Session) -> list[tuple[Datum]]:
        data = jsonable_encoder(datum_schema, exclude_unset=True)
        datums = db.query(self.model).all()
        return datums

    def create(self, file: UploadFile, path: str, db: Session) -> Datum:
        # data = jsonable_encoder(datum_schema)
        datum = self.model()
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


datum_service = DatumService(Datum)
