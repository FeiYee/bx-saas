from typing import Any

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..service.login_service import login_service
from ..schema.login_schema import LoginSchema

router = APIRouter()


@router.post("/wechat/login", response_model=None, tags=["wechat"])
async def login(login_schema: LoginSchema, db: Session = Depends(get_db)) -> Any:
    return login_service.login(code=login_schema.code, db=db)

