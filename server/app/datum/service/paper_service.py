from os import path
from typing import Type, TypeVar, List
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from config import BASE_DIR
from app.core.util import write_file, get_file_type
from app.system.model.user import User
from ..model.paper import Paper
from ..model.paper_datum import PaperDatum
from ..schema.paper_schema import PaperSchema

PaperModelType = TypeVar("PaperModelType", bound=Paper)
PaperDatumModelType = TypeVar("PaperDatumModelType", bound=PaperDatum)


class PaperService:

    def __init__(self, model: Type[PaperModelType], paper_datum_model: Type[PaperDatumModelType]):
        self.model = model
        self.paper_datum_model = paper_datum_model

    def find(self, db: Session) -> list[tuple[Paper]]:
        papers = db.query(self.model).order_by(self.model.created_at.desc()).all()
        return papers

    async def create(self, description: str, name: str, file: UploadFile, user_id: str, current_user: User, db: Session) -> Paper:
        user_id = user_id or current_user.id
        file_path = await write_file(file=file, write_path='paper', write_sub_path=user_id)

        paper = self.model()
        paper.name = name or path.splitext(file.filename)[0]
        paper.description = description
        paper.user_id = user_id
        paper.created_by = current_user.id

        paper.url = str('/' / file_path.relative_to(BASE_DIR)).replace('\\', '/')
        paper.file_name = file.filename
        paper.file_path = str(file_path)
        paper.file_type = file.content_type
        paper.file_size = file_path.stat().st_size
        paper.type = get_file_type(file)

        db.add(paper)
        db.commit()
        db.refresh(paper)
        return paper

    async def update(self, paper_id: str, description: str, name: str, file: UploadFile, db: Session) -> Paper:
        paper = db.query(self.model).get(paper_id)
        paper.name = name
        paper.description = description
        if file:
            file_path = await write_file(file=file, write_path='paper', write_sub_path=paper.user_id)
            paper.url = str('/' / file_path.relative_to(BASE_DIR)).replace('\\', '/')
            paper.file_name = file.filename
            paper.file_path = str(file_path)
            paper.file_type = file.content_type
            paper.file_size = file_path.stat().st_size
            paper.type = get_file_type(file)

        db.commit()
        db.refresh(paper)
        return paper

    def delete(self, *, paper_id: str, db: Session) -> Paper:
        paper = db.query(self.model).get(paper_id)
        setattr(paper, 'deleted_at', func.now())
        db.delete(paper)
        db.commit()
        return paper

    def find_by_user(self, name: str, current_user: User, db: Session) -> List[any]:
        papers = (
            db.query(self.model)
            .filter(and_(
                self.model.user_id == current_user.id,
                self.model.name.like('%{name}%'.format(name=name))
            ))
            .order_by(self.model.created_at.desc())
            .all()
        )

        for paper in papers:
            paper_datums = (
                db.query(self.paper_datum_model)
                .filter(self.paper_datum_model.paper_id == paper.id)
                .all()
            )
            paper.paper_datums = paper_datums

        return papers

    def find_page_by_title(self, title: str, page_number: int, page_size: int, db: Session) -> list[tuple[Paper]]:
        datums = db.query(self.model)\
            .filter(self.model.title.like('%{title}%'.format(title=title)))\
            .limit(page_size)\
            .offset((page_number-1)*page_size)
        return datums


paper_service = PaperService(Paper, PaperDatum)
