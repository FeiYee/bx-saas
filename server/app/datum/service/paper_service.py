from os import path
from typing import Type, TypeVar, List
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from config import BASE_DIR
from app.core.util import write_file, get_file_type
from app.system.model.user import User
from ..model.paper import Paper
from ..schema.paper_schema import PaperSchema

PaperModelType = TypeVar("PaperModelType", bound=Paper)


class PaperService:

    def __init__(self, model: Type[PaperModelType]):
        self.model = model

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

    def find_page_by_title(self, title: str, page_number: int, page_size: int, db: Session) -> list[tuple[Paper]]:
        datums = db.query(self.model)\
            .filter(self.model.title.like('%{title}%'.format(title=title)))\
            .limit(page_size)\
            .offset((page_number-1)*page_size)
        return datums

    def find_by_title(self, title: str, db: Session) -> List[tuple[Paper]]:
        articles = db.query(self.model).filter(self.model.title.like('%{title}%'.format(title=title))).all()
        # if len(title) == 0 or str.isspace(title):
        #     articles = db.query(self.model).all()
        # else:
        #     articles = db.query(self.model).filter(self.model.title.like('%{title}%'.format(title=title))).all()
        return articles


paper_service = PaperService(Paper)
