from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..service.excel_service import excel_service


router = APIRouter()


@router.get("/excel/article", tags=["Excel"])
async def get_article_excel(keyword: str, db: Session = Depends(get_db)):
    return excel_service.get_article_excel(keyword=keyword, db=db)
