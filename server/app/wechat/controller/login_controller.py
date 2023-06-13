from typing import Any

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..service.login_service import login_service

router = APIRouter()


@router.post("/wechat/login", response_model=None, tags=["wechat"])
async def login(code: str, db: Session = Depends(get_db)) -> Any:
    return login_service.login(code=code, db=db)

