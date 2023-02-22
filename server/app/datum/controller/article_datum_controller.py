from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from app.system.model.user import User
from app.home.security.auth import get_current_user
from ..schema.article_datum_schema import ArticleDatumSchema
from ..service.article_datum_service import article_datum_service


router = APIRouter()


@router.get("/article/{article_id}/datum", response_model=list[ArticleDatumSchema], tags=["article_datum"])
async def get(article_id: str, db: Session = Depends(get_db)):
    return article_datum_service.find(article_id=article_id, db=db)


@router.post("/article/{article_id}/datum", response_model=ArticleDatumSchema, tags=["article_datum"])
async def create(article_id: str, file: UploadFile = File(), db: Session = Depends(get_db)):
    return await article_datum_service.create(article_id=article_id, file=file, db=db)


@router.put("/article/datum/{article_datum_id}", response_model=ArticleDatumSchema, tags=["article_datum"])
async def update(article_datum_id: str, article_datum_schema: ArticleDatumSchema, db: Session = Depends(get_db)):
    return article_datum_service.update(article_datum_id=article_datum_id, article_datum_schema=article_datum_schema, db=db)


@router.delete("/article/datum/{article_datum_id}", response_model=ArticleDatumSchema, tags=["article_datum"])
async def delete(article_datum_id: str, db: Session = Depends(get_db)):
    return article_datum_service.delete(article_datum_id=article_datum_id, db=db)


@router.post("/article/datum/upload", tags=["article_datum"])
async def upload(file: UploadFile = File(), article_id: str = Form(default=''), keyword: str = Form(default=''), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await article_datum_service.upload(file=file, article_id=article_id, keyword=keyword, current_user=current_user, db=db)


@router.get("/article/datum/user", response_model=list[ArticleDatumSchema], tags=["article_datum"])
async def query_by_user(article_id: str = '', keyword: str = '', current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return article_datum_service.query_by_user(article_id=article_id, keyword=keyword, current_user=current_user, db=db)

# @router.get("/article/datum/download", tags=["datum"])
# async def download(title: str, db: Session = Depends(get_db)):
#     return article_datum_service.download(title=title, db=db)
