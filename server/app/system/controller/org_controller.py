from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from ..schema.org_schema import OrgSchema
from ..service.org_service import org_service


router = APIRouter()


@router.get("/org", response_model=list[OrgSchema], tags=["org"])
async def get(org_schema: OrgSchema, db: Session = Depends(get_db)):
    return org_service.find(org_schema=org_schema, db=db)


@router.post("/org", response_model=OrgSchema, tags=["org"])
async def create(org_schema: OrgSchema, db: Session = Depends(get_db)):
    return org_service.create(org_schema=org_schema, db=db)


@router.put("/org/{org_id}", response_model=OrgSchema, tags=["org"])
async def update(org_id: str, org_schema: OrgSchema, db: Session = Depends(get_db)):
    return org_service.update(org_id=org_id, org_schema=org_schema, db=db)


@router.delete("/org/{org_id}", response_model=OrgSchema, tags=["org"])
async def delete(org_id: str, db: Session = Depends(get_db)):
    return org_service.delete(org_id=org_id, db=db)
