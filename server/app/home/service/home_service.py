from datetime import timedelta
from typing import Any, Type, TypeVar
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.util import verify_password, get_password_hash
from app.system.model.user import User
from app.system.schema.user_schema import UserSchema
from app.system.service.user_service import user_service
from app.system.service.org_user_service import org_user_service
from ..security.auth import create_access_token
from ..schema.home_schema import Token, UserDetailSchema, RegisterSchema


class HomeService:

    def __init__(self):
        pass

    def home(self) -> Any:
        return {"index": "Home"}

    def register(self, register_schema: RegisterSchema, db: Session) -> UserSchema:
        user_schema = UserSchema(**register_schema.dict())
        # user_schema.password = get_password_hash(user_schema.password)
        user = user_service.create(user_schema=user_schema, db=db)
        return user

    def login(self, auth_form: OAuth2PasswordRequestForm, db: Session) -> Any:
        password = auth_form.password
        user = user_service.find_by_username(
            username=auth_form.username,
            db=db
        )
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户不存在")
        elif not user.is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无效用户")

        verify = verify_password(plain_password=password, hashed_password=user.password)
        if not verify:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="密码错误")

        token_type = "Bearer"
        access_token = create_access_token(
            subject=user.id,
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

        org = org_user_service.find_user_org(user_id=user.id, db=db)
        user_detail = UserDetailSchema(user=user, org=org)

        return user_detail


home_service = HomeService()
