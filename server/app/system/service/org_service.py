from typing import Type, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..model.org import Org
from ..schema.org_schema import OrgSchema

OrgModelType = TypeVar("OrgModelType", bound=Org)


class OrgService:

    def __init__(self, model: Type[OrgModelType]):
        self.model = model

    def find(self, org_schema: OrgSchema, db: Session) -> list[tuple[Org]]:
        data = jsonable_encoder(org_schema, exclude_unset=True)
        orgs = db.query(self.model).all()
        return orgs

    def create(self, org_schema: OrgSchema, db: Session) -> Org:
        data = jsonable_encoder(org_schema)
        org = self.model(**data)
        db.add(org)
        db.commit()
        db.refresh(org)
        return org

    def update(self, org_id: str, org_schema: OrgSchema, db: Session) -> Org:
        data = jsonable_encoder(org_schema, exclude_unset=True, exclude=['id'])
        org = db.query(self.model).get(org_id)
        for field in data:
            setattr(org, field, data[field])
        db.commit()
        db.refresh(org)
        return org

    def delete(self, *, org_id: str, db: Session) -> Org:
        org = db.query(self.model).get(org_id)
        setattr(org, 'deleted_at', func.now())
        db.commit()
        return org

    def remove(self, *, org_id: str, db: Session) -> Org:
        org = db.query(self.model).get(org_id)
        db.delete(org)
        db.commit()
        return org


org_service = OrgService(Org)
