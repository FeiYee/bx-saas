from typing import Type, TypeVar, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.util import get_uuid
from app.system.model.user import User
from ..model.search import Search
from ..model.keyword import Keyword
from ..model.search_record import SearchRecord
from ..schema.search_schema import SearchResultSchema
from app.graph.service.graph_service import GraphNeo
from config import NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD
import simplejson


KeywordModelType = TypeVar("KeywordModelType", bound=Keyword)
SearchModelType = TypeVar("SearchModelType", bound=Search)
SearchRecordModelType = TypeVar("SearchRecordModelType", bound=SearchRecord)

graph_service = GraphNeo(NEO4J_HOST, NEO4J_PORT, NEO4J_USER, NEO4J_PASSWORD)


class SearchService:
    def __init__(
        self,
        keyword_model: Type[KeywordModelType],
        search_model: Type[SearchModelType],
        search_record_model: Type[SearchRecordModelType]
    ):
        self.keyword_model = keyword_model
        self.search_model = search_model
        self.search_record_model = search_record_model

    def search(self, keyword_text: str, current_user: User, db: Session):
        keyword = db.query(self.keyword_model).filter(
            self.keyword_model.keyword == keyword_text,
            # self.keyword_model.type == 0,
            self.keyword_model.user_id == current_user.id,
        ).first()
        search = db.query(self.search_model).filter(
            self.search_model.keyword == keyword_text,
            # self.keyword_model.type == 0,
            self.keyword_model.user_id == current_user.id,
        ).first()
        search_record = self.search_record_model()

        if keyword is None:
            keyword = self.keyword_model()
            keyword.keyword = keyword_text
            keyword.weight = 1
            # keyword.type = 0
            keyword.is_preset = False
            keyword.user_id = current_user.id
        elif not keyword.is_preset:
            keyword.weight = keyword.weight + 1

        if search is None:
            search = self.search_model()
            search.id = get_uuid()
            search.keyword = keyword_text
            # search.type = 0
            search.count = 1
            search.user_id = current_user.id
        else:
            search.count = search.count + 1

        search_record.keyword = keyword_text
        search_record.search_id = search.id
        search_record.user_id = current_user.id

        db.add(keyword)
        db.add(search)
        db.add(search_record)

        db.commit()
        return None

    def search_graph(self, keyword_text: str, current_user: User, db: Session) -> Any:
        self.search(keyword_text=keyword_text, current_user=current_user, db=db)

        # data = jsonable_encoder({'keyword': keyword_text})
        try:
            data = graph_service.search_graph(text=keyword_text)
        except Exception as err:
            data = None

        # return data
        return simplejson.loads(simplejson.dumps(data, ignore_nan=True))

    def search_article(self, keyword_text: str, top_level: int, current_user: User, db: Session) -> Any:
        self.search(keyword_text=keyword_text, current_user=current_user, db=db)

        # data = jsonable_encoder({'keyword': keyword_text})
        data = None
        try:
            result = graph_service.search_table(text=keyword_text)
        except Exception as err:
            result = None

        if result is not None:
            data = result
            if top_level != 0:
                data['table'] = result['table'][0:top_level]

        # return data
        return simplejson.loads(simplejson.dumps(data, ignore_nan=True))


search_service = SearchService(keyword_model=Keyword, search_model=Search, search_record_model=SearchRecord)
