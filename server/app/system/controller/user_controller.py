from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..schema.user_schema import UserSchema
from ..service.user_service import user_service


router = APIRouter()


@router.get("/user", response_model=list[UserSchema], tags=["user"])
async def get(db: Session = Depends(get_db)):
    return user_service.find(db=db)


@router.post("/user", response_model=UserSchema, tags=["user"])
async def create(user_schema: UserSchema, db: Session = Depends(get_db)):
    return user_service.create(user_schema=user_schema, db=db)


@router.put("/user/{user_id}", response_model=UserSchema, tags=["user"])
async def update(user_id: str, user_schema: UserSchema, db: Session = Depends(get_db)):
    return user_service.update(user_id=user_id, user_schema=user_schema, db=db)


@router.delete("/user/{user_id}", response_model=UserSchema, tags=["user"])
async def delete(user_id: str, db: Session = Depends(get_db)):
    return user_service.delete(user_id=user_id, db=db)


