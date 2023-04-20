from typing import Any

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..service.message_service import message_service

router = APIRouter()


@router.get("/message", response_model=None, tags=["message"])
async def get(content: str, db: Session = Depends(get_db)) -> Any:
    return message_service.receive(content=content, db=db)


@router.post("/message", response_model=None, tags=["message"])
async def create(content: str, db: Session = Depends(get_db)) -> Any:
    return message_service.receive(content=content, db=db)

