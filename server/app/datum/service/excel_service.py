from typing import Type, TypeVar
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from config import BASE_DIR

from ..model.datum import Datum
from ..service.article_service import article_service


class ExcelService:

    def __init__(self):
        pass

    def get_file_path(self, filename: str, write_path: str = '', write_sub_path: str = ''):
        file_dir = BASE_DIR / 'asset'
        if write_path:
            file_dir = file_dir / write_path
        if not file_dir.exists():
            file_dir.mkdir()
        if write_sub_path:
            file_dir = file_dir / write_sub_path
        if not file_dir.exists():
            file_dir.mkdir()
        file_path = file_dir / filename
        return file_path

    def write_excel(self, keyword: str, db: Session) -> str:
        filename = ''
        file_path = self.get_file_path(filename=filename, write_path='article_datum_excel', write_sub_path=keyword)
        articles = article_service.find_by_title(title=keyword, db=db)


        url = str('/' / file_path.relative_to(BASE_DIR)).replace('\\', '/')
        return url


excel_service = ExcelService()
