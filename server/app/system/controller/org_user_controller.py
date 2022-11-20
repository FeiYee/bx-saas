from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..schema.org_user_schema import OrgUserSchema
from ..service.org_service import org_service


router = APIRouter()


@router.get("/org/{org_id}/user", response_model=list[OrgUserSchema], tags=["org"])
async def get(db: Session = Depends(get_db)):
    return org_service.find(db=db)


@router.post("/org/{org_id}/user", response_model=OrgUserSchema, tags=["org"])
async def create(org_user_schema: OrgUserSchema, db: Session = Depends(get_db)):
    return org_service.create(org_schema=org_user_schema, db=db)


@router.put("/org/{org_id}/user", response_model=OrgUserSchema, tags=["org"])
async def update(org_id: str, org_user_schema: OrgUserSchema, db: Session = Depends(get_db)):
    return org_service.update(org_id=org_id, org_schema=org_user_schema, db=db)

