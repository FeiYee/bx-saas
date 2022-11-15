from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..model.user import User
from ..schema.user_schema import UserSchema

UserModelType = TypeVar("UserModelType", bound=User)


class UserService:

    def __init__(self, model: Type[UserModelType]):
        self.model = model

    def find(self, user_schema: UserSchema, db: Session) -> list[tuple[User]]:
        data = jsonable_encoder(user_schema, exclude_unset=True)
        users = db.query(self.model).all()
        return users

    def create(self, user_schema: UserSchema, db: Session) -> User:
        data = jsonable_encoder(user_schema)
        user = self.model(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, user_id: str, user_schema: UserSchema, db: Session) -> User:
        data = jsonable_encoder(user_schema, exclude_unset=True, exclude=['id'])
        user = db.query(self.model).get(user_id)
        # user.username = data['username']
        for field in data:
            setattr(user, field, data[field])
        db.commit()
        db.refresh(user)
        return user

    def delete(self, *, user_id: str, db: Session) -> User:
        user = db.query(self.model).get(user_id)
        setattr(user, 'deleted_at', func.now())
        db.commit()
        return user

    def remove(self, *, user_id: str, db: Session) -> User:
        user = db.query(self.model).get(user_id)
        db.delete(user)
        db.commit()
        return user


user_service = UserService(User)
