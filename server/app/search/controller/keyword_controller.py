from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from app.system.model.user import User
from app.home.security.auth import get_current_user
from ..service.keyword_service import keyword_service
from ..schema.keyword_schema import KeywordSchema


router = APIRouter()


@router.get("/keyword", response_model=list[KeywordSchema], tags=["keyword"])
async def get(page_current: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    return keyword_service.find(db=db)


@router.post("/keyword", response_model=KeywordSchema, tags=["keyword"])
async def create(keyword_schema: KeywordSchema, db: Session = Depends(get_db)):
    return keyword_service.create(keyword_schema=keyword_schema, db=db)


@router.put("/keyword/{keyword_id}", response_model=KeywordSchema, tags=["keyword"])
async def update(keyword_id: str, keyword_schema: KeywordSchema, db: Session = Depends(get_db)):
    return keyword_service.update(keyword_id=keyword_id, keyword_schema=keyword_schema, db=db)


@router.delete("/keyword/{keyword_id}", response_model=KeywordSchema, tags=["keyword"])
async def delete(keyword_id: str, db: Session = Depends(get_db)):
    return keyword_service.delete(keyword_id=keyword_id, db=db)


@router.get("/keyword/user/{user_id}", response_model=list[str], tags=["keyword"])
async def get(user_id: str, db: Session = Depends(get_db)):
    return keyword_service.find_by_user(user_id=user_id, db=db)


@router.get("/keyword/user",  tags=["keyword"])
async def get(search_type: int = 0, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return keyword_service.find_user_keywords(search_type=search_type, current_user=current_user, db=db)


# 废弃
@router.get("/keyword/type/{keyword_type}/user",  tags=["keyword"])
async def get(keyword_type: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return keyword_service.find_user_keywords(keyword_type=keyword_type, current_user=current_user, db=db)
