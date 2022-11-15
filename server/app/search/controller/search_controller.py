from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db

from ..service.search_service import search_service
from ..schema.search_schema import SearchResultSchema


router = APIRouter()


@router.get("/search", response_model=SearchResultSchema, tags=["search"])
async def search(db: Session = Depends(get_db)):
    return search_service.search(db=db, keyword='你好')


@router.get("/search/keyword", tags=["search"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/search/{username}", tags=["search"])
async def read_user(username: str):
    return {"username": username}
