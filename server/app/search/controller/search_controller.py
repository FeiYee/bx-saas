from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db

from ..service.search_service import search_service
from ..schema.search_schema import SearchResultSchema


router = APIRouter()


@router.get("/search", response_model=SearchResultSchema, tags=["search"])
async def search(keyword: str, db: Session = Depends(get_db)):
    return search_service.search(db=db, keyword=keyword)


@router.get("/search/graph", tags=["search"])
async def search_graph(keyword: str, db: Session = Depends(get_db)):
    return search_service.search_graph(keyword=keyword, db=db)


@router.get("/search/article", tags=["search"])
async def search_article(keyword: str, db: Session = Depends(get_db)):
    return search_service.search_article(keyword=keyword, db=db)
