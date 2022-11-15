from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from ..model.search import Search
from ..schema.search_schema import SearchResultSchema


class SearchService:
    def __init__(self, model: Search):
        self.model = model

    def search(self, db: Session, keyword: str) -> SearchResultSchema:
        data = jsonable_encoder({'keyword': keyword})
        search = self.model(**data)
        # db.add(search)
        # db.commit()
        # db.refresh(search)
        return search


search_service = SearchService(Search)
