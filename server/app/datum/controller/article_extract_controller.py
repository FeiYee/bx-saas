from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..schema.article_extract_schema import ArticleExtractSchema
from ..service.article_extract_service import article_extract_service


router = APIRouter()


@router.get("/article/{article_id}/extract", response_model=list[ArticleExtractSchema], tags=["article_extract"])
async def get(article_id: str, db: Session = Depends(get_db)):
    return article_extract_service.find(article_id=article_id, db=db)


@router.post("/article/{article_id}/extract", response_model=ArticleExtractSchema, tags=["article_extract"])
async def create(article_id: str, file: UploadFile = File(), db: Session = Depends(get_db)):
    return await article_extract_service.create(article_id=article_id, file=file, db=db)


@router.put("/article/extract/{article_extract_id}", response_model=ArticleExtractSchema, tags=["article_extract"])
async def update(article_extract_id: str, article_extract_schema: ArticleExtractSchema, db: Session = Depends(get_db)):
    return article_extract_service.update(article_extract_id=article_extract_id, article_extract_schema=article_extract_schema, db=db)


@router.delete("/article/extract/{article_extract_id}", response_model=ArticleExtractSchema, tags=["article_extract"])
async def delete(article_extract_id: str, db: Session = Depends(get_db)):
    return article_extract_service.delete(article_extract_id=article_extract_id, db=db)


# @router.get("/article/extract/download", tags=["datum"])
# async def download(title: str, db: Session = Depends(get_db)):
#     return article_extract_service.download(title=title, db=db)
#
#
# @router.get("/article_extract/download/excel", tags=["datum"])
# async def download(title: str, name: str):
#     return article_extract_service.download_excel(title=title, name=name)
#
#
# @router.post("/article_extract/upload", tags=["datum"])
# async def upload(file: bytes = File(), path: str = Form()):
#     return {
#         "file_size": len(file),
#         "path": path,
#     }
#
