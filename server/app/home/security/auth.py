from datetime import datetime, timedelta
from typing import Any, Union
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from pydantic import ValidationError
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.dependence import get_db
from app.system.service.user_service import user_service
from ..schema.home_schema import TokenPayload


ALGORITHM = "HS256"


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/login"
)


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    claims = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(claims=claims, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> Any:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="验证失败",
        )
    user = user_service.find_by_id(id=token_data.sub, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="用户不存在")

    # user.password = None
    return user
