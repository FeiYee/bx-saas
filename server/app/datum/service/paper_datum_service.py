from os import path
from typing import Type, TypeVar
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session
from config import BASE_DIR
from app.core.util import write_file, get_file_type
from app.system.model.user import User
from ..model.paper_datum import PaperDatum
from ..schema.paper_datum_schema import PaperDatumSchema

PaperDatumModelType = TypeVar("PaperDatumModelType", bound=PaperDatum)


class PaperDatumService:

    def __init__(self, model: Type[PaperDatumModelType]):
        self.model = model

    def find(self, paper_id: str, db: Session) -> list[tuple[PaperDatum]]:
        paper_datums = (
            db.query(self.model)
            .filter(self.model.paper_id == paper_id)
            .order_by(self.model.created_at.desc())
            .all()
        )
        return paper_datums

    async def create(self, paper_id: str, name: str, description: str, file: UploadFile, db: Session) -> PaperDatum:
        file_path = await write_file(file=file, write_path='paper_datum', write_sub_path=paper_id)

        paper_datum = self.model()
        paper_datum.paper_id = paper_id
        paper_datum.name = name or path.splitext(file.filename)[0]
        paper_datum.description = description
        paper_datum.url = str('/' / file_path.relative_to(BASE_DIR)).replace('\\', '/')
        paper_datum.file_name = file.filename
        paper_datum.file_path = str(file_path)
        paper_datum.file_type = file.content_type
        paper_datum.file_size = file_path.stat().st_size
        paper_datum.type = get_file_type(file)

        db.add(paper_datum)
        db.commit()
        db.refresh(paper_datum)
        return paper_datum

    def update(self, paper_datum_id: str, datum_schema: PaperDatumSchema, db: Session) -> PaperDatum:
        data = jsonable_encoder(datum_schema, exclude_unset=True, exclude=['id'])
        paper_datum = db.query(self.model).get(paper_datum_id)
        for field in data:
            setattr(paper_datum, field, data[field])
        db.commit()
        db.refresh(paper_datum)
        return paper_datum

    def delete(self, *, paper_datum_id: str, db: Session) -> PaperDatum:
        paper_datum = db.query(self.model).get(paper_datum_id)
        setattr(paper_datum, 'deleted_at', func.now())
        db.delete(paper_datum)
        db.commit()
        return paper_datum

    def remove(self, *, paper_datum_id: str, db: Session) -> PaperDatumSchema:
        paper_datum = db.query(self.model).get(paper_datum_id)
        db.delete(paper_datum)
        db.commit()
        return paper_datum

    def query_by_user(self, article_id: str, keyword: str, current_user: User, db: Session) -> list[tuple[PaperDatum]]:
        filters = [self.model.user_id == current_user.id]
        if keyword != '':
            filters = [and_(self.model.keyword == keyword, self.model.user_id == current_user.id)]
        if article_id != '':
            filters = [and_(self.model.article_id == article_id, self.model.user_id == current_user.id)]

        article_datums = db.query(self.model).filter(*filters).all()
        return article_datums

    def download(self, *, article_datum_id: str, db: Session) -> PaperDatum:
        article_datum = db.query(self.model).get(article_datum_id)
        return article_datum


paper_datum_service = PaperDatumService(PaperDatum)
