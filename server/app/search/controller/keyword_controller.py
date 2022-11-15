from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..service.keyword_service import keyword_service
from ..schema.keyword_schema import KeywordSchema


router = APIRouter()


@router.get("/keyword", response_model=list[KeywordSchema], tags=["keyword"])
async def get(keyword_schema: KeywordSchema, db: Session = Depends(get_db)):
    return keyword_service.find(keyword_schema=keyword_schema, db=db)


@router.post("/keyword", response_model=KeywordSchema, tags=["keyword"])
async def create(keyword_schema: KeywordSchema, db: Session = Depends(get_db)):
    return keyword_service.create(keyword_schema=keyword_schema, db=db)


@router.put("/keyword/{keyword_id}", response_model=KeywordSchema, tags=["keyword"])
async def update(keyword_id: str, keyword_schema: KeywordSchema, db: Session = Depends(get_db)):
    return keyword_service.update(keyword_id=keyword_id, keyword_schema=keyword_schema, db=db)


@router.delete("/keyword/{keyword_id}", response_model=KeywordSchema, tags=["keyword"])
async def delete(keyword_id: str, db: Session = Depends(get_db)):
    return keyword_service.delete(keyword_id=keyword_id, db=db)


@router.get("/keyword/user/{user_id}", response_model=list[KeywordSchema], tags=["keyword"])
async def get(user_id: str, db: Session = Depends(get_db)):
    return keyword_service.find_by_user(user_id=user_id, db=db)
