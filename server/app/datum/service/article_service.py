from typing import Type, TypeVar, List
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
import requests

from ..model.article import Article
from ..schema.datum_schema import DatumSchema

ArticleModelType = TypeVar("ArticleModelType", bound=Article)


class ArticleService:

    def __init__(self, model: Type[ArticleModelType]):
        self.model = model

    def find(self, db: Session) -> list[tuple[Article]]:
        datums = db.query(self.model).all()
        return datums

    def find_by_title(self, title: str, db: Session) -> List[str]:
        articles = db.query(self.model).filter(self.model.title.like('%{title}%'.format(title=title))).all()
        return articles

    def find_article_title(self, *, db: Session) -> List[str]:
        articles = db.query(self.model).all()
        title_list = []
        for a in articles:
            title_list.append(a.title)
        return title_list

    # def get_article_title(self, *, title: str) -> List[str]:
    #     title_list = list(graph_service.total_table["Title"].values)
    #     return title_list


article_service = ArticleService(Article)
