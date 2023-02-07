from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
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


# @router.get("/article/datum/download", tags=["datum"])
# async def download(title: str, db: Session = Depends(get_db)):
#     return article_datum_service.download(title=title, db=db)
#
#
# @router.post("/article_datum/upload", tags=["datum"])
# async def upload(file: bytes = File(), path: str = Form()):
#     return {
#         "file_size": len(file),
#         "path": path,
#     }
#
