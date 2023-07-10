# from typing import Type, TypeVar, Any
# from sqlalchemy.orm import Session
# from app.core.util import get_uuid
# from app.system.model.user import User
# from ..model.search import Search
# from ..model.keyword import Keyword
# from ..model.search_record import SearchRecord
# from app.datum.service.article_service import article_service
# from app.datum.service.paper_service import paper_service
# from app.graph.service.graph_service import graph_service

# KeywordModelType = TypeVar("KeywordModelType", bound=Keyword)
# SearchModelType = TypeVar("SearchModelType", bound=Search)
# SearchRecordModelType = TypeVar("SearchRecordModelType", bound=SearchRecord)


# class SearchService:
#     def __init__(
#         self,
#         keyword_model: Type[KeywordModelType],
#         search_model: Type[SearchModelType],
#         search_record_model: Type[SearchRecordModelType]
#     ):
#         self.keyword_model = keyword_model
#         self.search_model = search_model
#         self.search_record_model = search_record_model

#     def search(self, keyword_text: str, current_user: User, db: Session, search_type: int = 0):
#         if not keyword_text:
#             return
#         keyword = db.query(self.keyword_model).filter(
#             self.keyword_model.keyword == keyword_text,
#             self.keyword_model.type == search_type,
#             self.keyword_model.user_id == current_user.id,
#         ).first()
#         search = db.query(self.search_model).filter(
#             self.search_model.keyword == keyword_text,
#             self.keyword_model.type == search_type,
#             self.keyword_model.user_id == current_user.id,
#         ).first()
#         search_record = self.search_record_model()

#         if keyword is None:
#             keyword = self.keyword_model()
#             keyword.keyword = keyword_text
#             keyword.weight = 1
#             keyword.type = search_type
#             keyword.is_preset = False
#             keyword.user_id = current_user.id
#         elif not keyword.is_preset:
#             keyword.weight = keyword.weight + 1

#         if search is None:
#             search = self.search_model()
#             search.id = get_uuid()
#             search.keyword = keyword_text
#             search.type = search_type
#             search.count = 1
#             search.user_id = current_user.id
#         else:
#             search.count = search.count + 1

#         search_record.keyword = keyword_text
#         search_record.search_id = search.id
#         search_record.user_id = current_user.id

#         db.add(keyword)
#         db.add(search)
#         db.add(search_record)

#         db.commit()
#         return None

#     def search_graph(self, keyword_text: str, current_user: User, db: Session) -> Any:
#         self.search(keyword_text=keyword_text, current_user=current_user, db=db, search_type=0)
#         try:
#             # data = graph_service.search_graph(text=keyword_text, db=db)

#             data = graph_service.find_by_keyword(keyword=keyword_text, db=db)
#             print("图谱检索成功：",keyword_text)
#         except Exception as err:
#             print("图谱检索失败：",err,keyword_text)
#             data = None

#         return data
#         # return simplejson.loads(simplejson.dumps(data, ignore_nan=True))

#     def search_article(self, keyword_text: str, top_level: int, current_user: User, db: Session) -> Any:
#         print("search_article",keyword_text)
#         self.search(keyword_text=keyword_text, current_user=current_user, db=db, search_type=0)
#         articles = article_service.find_by_title(title=keyword_text, db=db)
#         if top_level != 0:
#             articles = articles[0:top_level]
#         return articles

#     def search_paper(self, keyword_text: str, current_user: User, db: Session) -> Any:
#         print("search_paper",keyword_text)
#         self.search(keyword_text=keyword_text, current_user=current_user, db=db, search_type=1)
#         papers = paper_service.find_by_user(name=keyword_text, current_user=current_user, db=db)
#         return papers


# search_service = SearchService(keyword_model=Keyword, search_model=Search, search_record_model=SearchRecord)



from typing import Type, TypeVar, Any
from sqlalchemy.orm import Session
from app.core.util import get_uuid
from app.system.model.user import User
from ..model.search import Search
from ..model.keyword import Keyword
from ..model.search_record import SearchRecord
from app.datum.service.article_service import article_service
from app.datum.service.paper_service import paper_service
from app.graph.service.graph_service import graph_service

KeywordModelType = TypeVar("KeywordModelType", bound=Keyword)
SearchModelType = TypeVar("SearchModelType", bound=Search)
SearchRecordModelType = TypeVar("SearchRecordModelType", bound=SearchRecord)


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

    def search(self, keyword_text: str, current_user: User, db: Session, search_type: int = 0):
        if not keyword_text:
            return
        keyword = db.query(self.keyword_model).filter(
            self.keyword_model.keyword == keyword_text,
            self.keyword_model.type == search_type,
            self.keyword_model.user_id == current_user.id,
        ).first()
        search = db.query(self.search_model).filter(
            self.search_model.keyword == keyword_text,
            self.keyword_model.type == search_type,
            self.keyword_model.user_id == current_user.id,
        ).first()
        search_record = self.search_record_model()

        if keyword is None:
            keyword = self.keyword_model()
            keyword.keyword = keyword_text
            keyword.weight = 1
            keyword.type = search_type
            keyword.is_preset = False
            keyword.user_id = current_user.id
        elif not keyword.is_preset:
            keyword.weight = keyword.weight + 1

        if search is None:
            search = self.search_model()
            search.id = get_uuid()
            search.keyword = keyword_text
            search.type = search_type
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
        self.search(keyword_text=keyword_text, current_user=current_user, db=db, search_type=0)
        try:
            # data = graph_service.search_graph(text=keyword_text, db=db)

            data = graph_service.find_by_keyword(keyword=keyword_text, db=db)
            print("图谱检索成功：",keyword_text)
        except Exception as err:
            print("图谱检索失败：",err,keyword_text)
            data = None
        # print(data)
        return data
        # return simplejson.loads(simplejson.dumps(data, ignore_nan=True))

    def search_article(self, keyword_text: str, top_level: int, current_user: User, db: Session) -> Any:
        print("search_article",keyword_text)
        self.search(keyword_text=keyword_text, current_user=current_user, db=db, search_type=0)
        articles = article_service.find_by_title(title=keyword_text, db=db)
        if top_level != 0:
            articles = articles[0:top_level]
        return articles

    def search_paper(self, keyword_text: str, current_user: User, db: Session) -> Any:
        print("search_paper",keyword_text)
        self.search(keyword_text=keyword_text, current_user=current_user, db=db, search_type=1)
        papers = paper_service.find_by_user(name=keyword_text, current_user=current_user, db=db)
        return papers


search_service = SearchService(keyword_model=Keyword, search_model=Search, search_record_model=SearchRecord)
