from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependence import get_db
from app.core.util import get_uuid
from app.system.model.user import User
from ..service.home_service import home_service
from ..security.auth import get_current_user

router = APIRouter()


@router.get("/")
async def home():
    return home_service.home()


@router.post("/login", tags=["home"])
async def login(auth_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    return home_service.login(auth_form=auth_form, db=db)


@router.post("/logout", tags=["home"])
async def logout():
    return home_service.logout()


@router.get("/user/detail", tags=["home"])
async def get_user_detail(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return home_service.get_user_detail(current_user=current_user, db=db)


@router.get("/token/user", tags=["home"])
def user(current_user: User = Depends(get_current_user)) -> Any:
    return current_user


@router.get("/uuid", tags=["home"])
def uuid() -> Any:
    return get_uuid()
