from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..schema.datum_schema import DatumSchema
from ..service.datum_service import datum_service


router = APIRouter()


@router.get("/datum", response_model=list[DatumSchema], tags=["datum"])
async def get(datum_schema: DatumSchema, db: Session = Depends(get_db)):
    return datum_service.find(datum_schema=datum_schema, db=db)


@router.post("/datum", response_model=DatumSchema, tags=["datum"])
async def create(file: UploadFile = File(), path: str = Form(), db: Session = Depends(get_db)):
    return datum_service.create(file=file, path=path, db=db)


@router.put("/datum/{datum_id}", response_model=DatumSchema, tags=["datum"])
async def update(datum_id: str, datum_schema: DatumSchema, db: Session = Depends(get_db)):
    return datum_service.update(datum_id=datum_id, datum_schema=datum_schema, db=db)


@router.delete("/datum/{datum_id}", response_model=DatumSchema, tags=["datum"])
async def delete(datum_id: str, db: Session = Depends(get_db)):
    return datum_service.delete(datum_id=datum_id, db=db)


@router.post("/datum/upload", tags=["datum"])
async def upload(file: bytes = File(), path: str = Form()):
    return {
        "file_size": len(file),
        "path": path,
    }

