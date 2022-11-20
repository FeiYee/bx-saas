from datetime import timedelta
from typing import Any, Type, TypeVar
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.system.model.user import User
from app.system.service.user_service import user_service
from ..security.auth import create_access_token
from ..schema.home_schema import Token, UserDetailSchema


class HomeService:

    def __init__(self):
        pass

    def home(self) -> Any:
        return {"index": "Home"}

    def login(self, auth_form: OAuth2PasswordRequestForm, db: Session) -> Any:
        user = user_service.find_by_username(
            username=auth_form.username,
            password=auth_form.password,
            db=db
        )
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误")
        elif not user.is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无效用户")

        token_type = "bearer"
        access_token = create_access_token(
            user.id,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        token = Token(token_type=token_type, access_token=access_token)

        return token

    def logout(self, current_user: User, db: Session) -> bool:
        return True

    def get_user_detail(self, current_user: User, db: Session) -> Any:
        user = current_user
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户不存在")
        elif not user.is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无效用户")

        user_detail = UserDetailSchema(user=user, org=None)

        return user_detail


home_service = HomeService()
