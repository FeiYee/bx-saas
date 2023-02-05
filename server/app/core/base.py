

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from .database import Base
from .util import get_uuid


class BaseModel(Base):
    __abstract__ = True

    id = Column(String(32), primary_key=True, index=True, default=get_uuid)
    is_valid = Column(Boolean, default=True, comment='是否可用')
    remark = Column(String(255), comment='备注')
    created_by = Column(String(32), comment='创建人ID')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_by = Column(String(32), comment='更新人ID')
    updated_at = Column(DateTime, onupdate=func.now(), comment='更新时间')
    updated_count = Column(Integer, comment='更新次数')
    deleted_by = Column(String(32), comment='删除人ID')
    deleted_at = Column(DateTime, comment='删除时间')

    def set_id(self):
        self.id = get_uuid()

    def set_created_by(self, id: str):
        self.id = id


@as_declarative()
class BaseMapperModel:

    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseSchema:
    id: Any


ModelType = TypeVar("ModelType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseSchema)


class BaseService(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: SchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[SchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
