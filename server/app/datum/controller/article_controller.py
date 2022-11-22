from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..schema.datum_schema import DatumSchema
from ..service.article_service import article_service


router = APIRouter()


@router.get("/article", tags=["article"])
async def get_article(title: str):
    return article_service.get_article(title=title)


@router.get("/article/title", tags=["article"])
async def get_article_title(title: str = ''):
    return article_service.get_article_title(title=title)

