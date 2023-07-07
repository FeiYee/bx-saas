from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..schema.datum_schema import DatumSchema
from ..service.datum_service import datum_service


router = APIRouter()


@router.get("/datum", response_model=list[DatumSchema], tags=["datum"])
async def get(db: Session = Depends(get_db)):
    return datum_service.find(db=db)


@router.post("/datum", response_model=DatumSchema, tags=["datum"])
async def create(article_id: str = Form(), file: UploadFile = File(), db: Session = Depends(get_db)):
    return await datum_service.create(article_id=article_id, file=file, db=db)


@router.put("/datum/{datum_id}", response_model=DatumSchema, tags=["datum"])
async def update(datum_id: str, datum_schema: DatumSchema, db: Session = Depends(get_db)):
    return datum_service.update(datum_id=datum_id, datum_schema=datum_schema, db=db)


@router.delete("/datum/{datum_id}", response_model=DatumSchema, tags=["datum"])
async def delete(datum_id: str, db: Session = Depends(get_db)):
    return datum_service.delete(datum_id=datum_id, db=db)


@router.get("/datum/article/{article_id}", tags=["datum"])
async def download(article_id: str, db: Session = Depends(get_db)):
    return datum_service.find_by_article(article_id=article_id, db=db)
