from typing import Type, TypeVar
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from config import BASE_DIR
from app.core.util import write_file
from ..model.article_extract import ArticleExtract
from ..schema.article_extract_schema import ArticleExtractSchema


ArticleExtractModelType = TypeVar("ArticleExtractModelType", bound=ArticleExtract)


class ArticleExtractService:

    def __init__(self, model: Type[ArticleExtractModelType]):
        self.model = model

    def find(self, article_id: str, db: Session) -> list[tuple[ArticleExtract]]:
        article_extracts = db.query(self.model).filter(self.model.article_id == article_id).all()
        return article_extracts

    async def create(self, article_id: str, file: UploadFile, db: Session) -> ArticleExtract:
        # content = await file.read()
        # file_dir = BASE_DIR / 'asset' / 'article_extract'
        # if not file_dir.exists():
        #     file_dir.mkdir()
        # file_dir = file_dir / article_id
        # if not file_dir.exists():
        #     file_dir.mkdir()
        # file_path = file_dir / file.filename
        # file_path.write_bytes(content)
        file_path = await write_file(file=file, write_path='article_extract', write_sub_path=article_id)

        article_extract = self.model()
        article_extract.article_id = article_id
        article_extract.file_name = file.filename
        article_extract.url = str('/' / file_path.relative_to(BASE_DIR)).replace('\\', '/')
        article_extract.file_path = str(file_path)
        article_extract.file_type = file.content_type
        article_extract.file_size = file_path.stat().st_size

        if 'image' in file.content_type:
            article_extract.type = 0
        elif 'sheet' in file.content_type:
            article_extract.type = 1
        elif 'pdf' in file.content_type:
            article_extract.type = 2
        elif 'zip' in file.content_type:
            article_extract.type = 3

        db.add(article_extract)
        db.commit()
        db.refresh(article_extract)
        return article_extract

    def update(self, article_extract_id: str, datum_schema: ArticleExtractSchema, db: Session) -> ArticleExtract:
        data = jsonable_encoder(datum_schema, exclude_unset=True, exclude=['id'])
        article_extract = db.query(self.model).get(article_extract_id)
        for field in data:
            setattr(article_extract, field, data[field])
        db.commit()
        db.refresh(article_extract)
        return article_extract

    def delete(self, *, article_extract_id: str, db: Session) -> ArticleExtract:
        article_extract = db.query(self.model).get(article_extract_id)
        setattr(article_extract, 'deleted_at', func.now())
        db.delete(article_extract)
        db.commit()
        return article_extract

    def remove(self, *, article_extract_id: str, db: Session) -> ArticleExtract:
        article_extract = db.query(self.model).get(article_extract_id)
        db.delete(article_extract)
        db.commit()
        return article_extract

    def download(self, *, article_extract_id: str, db: Session) -> ArticleExtract:
        article_extract = db.query(self.model).get(article_extract_id)
        return article_extract


article_extract_service = ArticleExtractService(model=ArticleExtract)
