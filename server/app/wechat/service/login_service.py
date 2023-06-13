from datetime import timedelta
from typing import Type, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.system.service.user_service import user_service
from app.system.schema.user_schema import UserSchema
from app.home.security.auth import create_access_token
from app.home.schema.home_schema import Token

from .wechat_service import wechat_service


class LoginService:

    def __init__(self):
        pass

    def login(self, code: any, db: Session) -> any:
        access_token = wechat_service.get_access_token()
        phone = wechat_service.get_user_phone(access_token=access_token, code=code);
        user = user_service.find_by_phone(phone=phone, db=db)
        if user is None:
            user_schema = UserSchema(
                username=phone,
                phone=phone,
                name=phone,
                is_admin=False,
            )
            user_service.create(user_schema=user_schema, db=db)
            user = user_service.find_by_phone(phone=phone, db=db)

        print(user)

        token_type = "Bearer"
        access_token = create_access_token(
            subject=user.id,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        token = Token(token_type=token_type, access_token=access_token)

        return token


login_service = LoginService()
