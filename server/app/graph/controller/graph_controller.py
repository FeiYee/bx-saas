from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from app.system.model.user import User
from app.home.security.auth import get_current_user
from ..schema.graph_schema import GraphSchema
from ..service.graph_service import graph_service


router = APIRouter()


@router.post("/graph", response_model=GraphSchema, tags=["graph"])
async def create(graph_schema: GraphSchema, db: Session = Depends(get_db)):
    return graph_service.create(graph_schema=graph_schema, db=db)


