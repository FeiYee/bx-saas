from typing import Type, TypeVar, List
from fastapi import File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ..model.graph import Graph
from ..schema.graph_schema import GraphSchema

from app.datum.service.article_service import article_service

GraphModelType = TypeVar("GraphModelType", bound=Graph)


class GraphService:

    def __init__(self, model: Type[GraphModelType]):
        self.model = model

    def create(self, graph_schema: GraphSchema, db: Session) -> Graph:
        data = jsonable_encoder(graph_schema)
        graph = self.model(**data)
        # article.created_by = current_user.id
        db.add(graph)
        db.commit()
        db.refresh(graph)
        return graph

    def find_by_keyword(self, keyword: str, db: Session) -> List[tuple[Graph]]:
        articles = article_service.find_by_title(title=keyword, db=db)

        article_ids = []
        article_dict = {}
        for article in articles:
            article_ids.append(article.id)
            article_dict[article.id] = article

        filters = [or_(
            self.model.article_id.in_(article_ids),
            self.model.ent1.like('%{keyword}%'.format(keyword=keyword)),
            self.model.ent2.like('%{keyword}%'.format(keyword=keyword)),
            self.model.rela.like('%{keyword}%'.format(keyword=keyword))
        )]

        graphs = db.query(self.model).filter(*filters).all()
        db.query(self.model).filter(self.model.ent1.like('%{keyword}%'.format(keyword=keyword))).all()

        graph_dict = []
        for graph in graphs:
            data = graph.__dict__
            data['article'] = article_dict.get(graph.article_id)
            graph_dict.append(data)

        return graph_dict

    def search_graph(self, keyword: str, db: Session):
        graphs = self.find_by_keyword(keyword=keyword, db=db)

        return graphs


graph_service = GraphService(Graph)
