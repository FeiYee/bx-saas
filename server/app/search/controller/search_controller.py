from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from app.system.model.user import User
from app.home.security.auth import get_current_user

from ..service.search_service import search_service
from ..schema.search_schema import SearchResultSchema


router = APIRouter()


@router.get("/search", response_model=SearchResultSchema, tags=["search"])
async def search(keyword: str, db: Session = Depends(get_db)):
    return search_service.search(db=db, keyword_text=keyword)


@router.get("/search/graph", tags=["search"])
async def search_graph(keyword: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return search_service.search_graph(keyword_text=keyword, current_user=current_user, db=db)


@router.get("/search/article", tags=["search"])
async def search_article(keyword: str, top_level: int = 0, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return search_service.search_article(keyword_text=keyword, top_level=top_level, current_user=current_user, db=db)


@router.get("/search/file", tags=["search"])
async def search_file(keyword: str, top_level: int = 0, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return search_service.search_file(keyword_text=keyword, top_level=top_level, current_user=current_user, db=db)


@router.get("/search/extract", tags=["search"])
async def search_extract(keyword: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return search_service.search_extract(keyword_text=keyword, current_user=current_user, db=db)
