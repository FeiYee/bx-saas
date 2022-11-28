from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..schema.org_user_schema import OrgUserSchema
from ..service.org_user_service import org_user_service


router = APIRouter()


@router.get("/org/{org_id}/user", response_model=list[OrgUserSchema], tags=["org_user"])
async def get(org_id: str, db: Session = Depends(get_db)):
    return org_user_service.find(org_id=org_id, db=db)


@router.post("/org/{org_id}/user", response_model=OrgUserSchema, tags=["org_user"])
async def create(org_id: str, user_id_list: list[str], db: Session = Depends(get_db)):
    return org_user_service.create(org_id=org_id, user_id_list=user_id_list, db=db)


@router.delete("/org/user/{org_user_id}", response_model=OrgUserSchema, tags=["org_user"])
async def delete(org_user_id: str, db: Session = Depends(get_db)):
    return org_user_service.delete(org_user_id=org_user_id, db=db)

