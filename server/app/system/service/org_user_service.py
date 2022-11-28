from typing import Type, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..model.org_user import OrgUser
from ..model.org import Org
from ..schema.org_schema import OrgSchema

OrgModelType = TypeVar("OrgModelType", bound=Org)
OrgUserModelType = TypeVar("OrgUserModelType", bound=OrgUser)


class OrgUserService:

    def __init__(
        self,
        org_user_model: Type[OrgUserModelType],
        org_model: Type[OrgModelType]
    ):
        self.org_user_model = org_user_model
        self.org_model = org_model

    def find(self, org_id: str, db: Session) -> list[tuple[OrgUser]]:
        # data = jsonable_encoder(org_schema, exclude_unset=True)
        org_users = db.query(self.org_user_model).filter(
            self.org_user_model.org_id == org_id,
            # self.model.deleted_at.is_(None)
        ).all()
        return org_users

    def create(self, org_id: str, user_id_list: list[str], db: Session) -> list[OrgUser]:
        for user_id in user_id_list:
            org_user = self.org_user_model()
            org_user.org_id = org_id
            org_user.user_id = user_id
            db.add(org_user)
        db.commit()
        return []

    def delete(self, *, org_user_id: str, db: Session) -> OrgUser:
        org_user = db.query(self.org_user_model).get(org_user_id)
        setattr(org_user, 'deleted_at', func.now())
        db.delete(org_user)
        db.commit()
        return org_user

    def remove(self, *, org_user_id: str, db: Session) -> OrgUser:
        org_user = db.query(self.org_user_model).get(org_user_id)
        db.delete(org_user)
        db.commit()
        return org_user

    def find_user_org(self, *, user_id: str, db: Session) -> Org:
        org_user = db.query(self.org_user_model).filter(
            self.org_user_model.user_id == user_id,
        ).first()
        org = None
        if org_user is not None:
            org = db.query(self.org_model).get(org_user.org_id)

        return org


org_user_service = OrgUserService(OrgUser, Org)
