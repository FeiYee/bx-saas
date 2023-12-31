from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi import Depends, HTTPException, status

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from config import PASSWORD_DEFAULT
from app.core.util import get_password_hash
from ..model.user import User
from ..schema.user_schema import UserSchema, UserInfoSchema

UserModelType = TypeVar("UserModelType", bound=User)


class UserService:

    def __init__(self, model: Type[UserModelType]):
        self.model = model

    def find_by_id(self, id: str, db: Session) -> User:
        user = db.query(self.model).get(id)
        return user

    def find_by_username(self, username: str, db: Session) -> User:
        user = db.query(self.model).filter(
            self.model.username == username,
        ).first()
        return user

    def find_by_phone(self, phone: str, db: Session) -> User:
        user = db.query(self.model).filter(
            self.model.phone == phone,
        ).first()
        return user

    def find(self, db: Session) -> list[tuple[User]]:
        # data = jsonable_encoder(user_schema, exclude_unset=True)
        users = db.query(self.model).filter(self.model.deleted_at.is_(None)).all()
        return users

    def create(self, user_schema: UserSchema, db: Session) -> User:
        exist_user = db.query(self.model).filter(self.model.username == user_schema.username).first()
        if exist_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用已存在.")
        data = jsonable_encoder(user_schema)
        user = self.model(**data)
        if user.password is not None and len(user.password) > 0:
            user.password = get_password_hash(user.password)
        else:
            user.password = get_password_hash(PASSWORD_DEFAULT)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, user_id: str, user_schema: UserSchema, db: Session) -> User:
        data = jsonable_encoder(user_schema, exclude_unset=True, exclude={'id', 'password'})
        if hasattr(data, 'password'):
            data.password = get_password_hash(data.password)
        user = db.query(self.model).get(user_id)

        for field in data:
            setattr(user, field, data[field])

        db.commit()
        db.refresh(user)
        return user

    def delete(self, *, user_id: str, db: Session) -> User:
        user = db.query(self.model).get(user_id)
        setattr(user, 'deleted_at', func.now())
        db.delete(user)
        db.commit()
        return user

    def remove(self, *, user_id: str, db: Session) -> User:
        user = db.query(self.model).get(user_id)
        db.delete(user)
        db.commit()
        return user

    def update_information(self, user_info_schema: UserInfoSchema, db: Session) -> User:
        exist_user = db.query(self.model).filter(self.model.id == user_info_schema.id).first()
        if exist_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户不存在.")

        data = jsonable_encoder(user_info_schema, exclude_unset=True, exclude={'id', 'password'})
        user = db.query(self.model).get(user_info_schema.id)
        for field in data:
            setattr(user, field, data[field])

        db.commit()
        db.refresh(user)
        return user


user_service = UserService(User)
