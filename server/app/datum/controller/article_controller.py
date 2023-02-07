from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from app.system.model.user import User
from app.home.security.auth import get_current_user
from ..schema.article_schema import ArticleSchema
from ..service.article_service import article_service


router = APIRouter()


@router.get("/article", tags=["article"])
async def get(db: Session = Depends(get_db)):
    return article_service.find(db=db)


@router.post("/article", response_model=ArticleSchema, tags=["article"])
async def create(article_schema: ArticleSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return article_service.create(article_schema=article_schema, current_user=current_user, db=db)


@router.get("/article/query", tags=["article"])
async def get_article_by_title(title: str = '', db: Session = Depends(get_db)):
    return article_service.find_by_title(title=title, db=db)


@router.get("/article/title", tags=["article"])
async def get_article_title(db: Session = Depends(get_db)):
    return article_service.find_article_title(db=db)

