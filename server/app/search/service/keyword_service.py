from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, or_
from sqlalchemy.orm import Session
from app.system.model.user import User
from app.system.service.org_user_service import org_user_service
from ..model.keyword import Keyword
from ..schema.keyword_schema import KeywordSchema

KeywordModelType = TypeVar("KeywordModelType", bound=Keyword)


class KeywordService:
    def __init__(self, model: Type[KeywordModelType]):
        self.model = model

    def find(self, db: Session) -> list[tuple[Keyword]]:
        # data = jsonable_encoder(keyword_schema, exclude_unset=True)
        keywords = db.query(self.model).all()
        return keywords

    def create(self, keyword_schema: KeywordSchema, db: Session) -> Keyword:
        data = jsonable_encoder(keyword_schema)
        keyword = self.model(**data)
        db.add(keyword)
        db.commit()
        db.refresh(keyword)
        return keyword

    def update(self, keyword_id: str, keyword_schema: KeywordSchema, db: Session) -> Keyword:
        data = jsonable_encoder(keyword_schema, exclude_unset=True, exclude=['id'])
        keyword = db.query(self.model).get(keyword_id)
        for field in data:
            setattr(keyword, field, data[field])
        db.commit()
        db.refresh(keyword)
        return keyword

    def delete(self, *, keyword_id: str, db: Session) -> Keyword:
        keyword = db.query(self.model).get(keyword_id)
        setattr(keyword, 'deleted_at', func.now())
        db.delete(keyword)
        db.commit()
        return keyword

    def remove(self, *, keyword_id: str, db: Session) -> Keyword:
        keyword = db.query(self.model).get(keyword_id)
        db.delete(keyword)
        db.commit()
        return keyword

    def find_by_user(self, user_id: str, db: Session) -> List[str]:
        keywords = (
            db.query(self.model)
            .filter(self.model.user == user_id)
            .order_by(self.model.weight.desc())
            .all()
        )
        keyword_list = []
        for k in keywords:
            keyword_list.append(k.keyword)
        return keyword_list

    def find_user_keywords(self, current_user: User, db: Session) -> Any:
        org = org_user_service.find_user_org(user_id=current_user.id, db=db)
        filters = [self.model.user_id == current_user.id]
        if org is not None:
            filters = [or_(self.model.org_id == org.id, self.model.user_id == current_user.id)]
        keywords = db.query(self.model).filter(*filters).order_by(self.model.weight.desc()).distinct(self.model.keyword).all()

        keyword_list = []
        for k in keywords:
            keyword_list.append(k)
        return keyword_list


keyword_service = KeywordService(Keyword)
