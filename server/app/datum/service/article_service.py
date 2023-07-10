from typing import Type, TypeVar, List
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
import requests
from app.system.model.user import User

from ..model.article import Article
from ..schema.article_schema import ArticleSchema

ArticleModelType = TypeVar("ArticleModelType", bound=Article)


class ArticleService:

    def __init__(self, model: Type[ArticleModelType]):
        self.model = model

    def find(self, db: Session) -> list[tuple[Article]]:
        datums = db.query(self.model).all()
        return datums

    def create(self, article_schema: ArticleSchema, db: Session) -> Article:
        data = jsonable_encoder(article_schema)
        article = self.model(**data)
        # article.created_by = current_user.id
        db.add(article)
        db.commit()
        db.refresh(article)
        return article

    def find_page_by_title(self, title: str, page_number: int, page_size: int, db: Session) -> list[tuple[Article]]:
        datums = db.query(self.model)\
            .filter(self.model.title.like('%{title}%'.format(title=title)))\
            .limit(page_size)\
            .offset((page_number-1)*page_size)
        print("信息合并")
        datums = self.article_info_specification(datums)
        print("合并成功")
        return datums

    def article_info_specification(self, datums):
        datums_list = []
        for line in datums:
            line = line.__dict__

            other = ""

            if len(str(line['microbe']).replace(" ;@;", "、")) > 1:
                other += "Microbe：" + str(line['microbe']).replace(" ;@;", "、") + "\n"
            if len(str(line['cell']).replace(" ;@;", "、")) > 1:
                other += "Cell：" + str(line['cell']).replace(" ;@;", "、") + "\n"
            if len(str(line['gene']).replace(" ;@;", "、")) > 1:
                other += "Gene：" + str(line['gene']).replace(" ;@;", "、") + "\n"
            line["other"] = other
            datums_list.append(line)
            return datums_list


    def find_by_title(self, title: str, db: Session) -> List[tuple[Article]]:
        articles = db.query(self.model).filter(self.model.title.like('%{title}%'.format(title=title))).all()
        print(articles)
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
