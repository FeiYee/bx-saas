from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..service.message_service import message_service
from ..schema.message_schema import MessageSchema

router = APIRouter()


@router.get("/message", response_model=list[MessageSchema], tags=["org"])
async def get(db: Session = Depends(get_db)):
    return message_service.find(db=db)


@router.post("/message", response_model=MessageSchema, tags=["org"])
async def create(org_schema: MessageSchema, db: Session = Depends(get_db)):
    return message_service.create(org_schema=org_schema, db=db)

