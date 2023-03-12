from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from app.system.model.user import User
from app.home.security.auth import get_current_user
from ..schema.paper_datum_schema import PaperDatumSchema
from ..service.paper_datum_service import paper_datum_service


router = APIRouter()


@router.get("/paper/{paper_id}/datum", response_model=list[PaperDatumSchema], tags=["paper_datum"])
async def get(paper_id: str, db: Session = Depends(get_db)):
    return paper_datum_service.find(paper_id=paper_id, db=db)


@router.post("/paper/{paper_id}/datum", response_model=PaperDatumSchema, tags=["paper_datum"])
async def create(paper_id: str, name: str = Form(default=''), description: str = Form(default=''), file: UploadFile = File(),
                 db: Session = Depends(get_db)):
    return await paper_datum_service.create(paper_id=paper_id, name=name, description=description, file=file, db=db)


@router.put("/paper/datum/{paper_datum_id}", response_model=PaperDatumSchema, tags=["paper_datum"])
async def update(paper_datum_id: str, paper_datum_schema: PaperDatumSchema, db: Session = Depends(get_db)):
    return paper_datum_service.update(paper_datum_id=paper_datum_id, paper_datum_schema=paper_datum_schema, db=db)


@router.delete("/paper/datum/{paper_datum_id}", response_model=PaperDatumSchema, tags=["paper_datum"])
async def delete(paper_datum_id: str, db: Session = Depends(get_db)):
    return paper_datum_service.delete(paper_datum_id=paper_datum_id, db=db)


@router.get("/paper/datum/user", response_model=list[PaperDatumSchema], tags=["paper_datum"])
async def query_by_user(paper_id: str = '', keyword: str = '', current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return paper_datum_service.query_by_user(paper_id=paper_id, keyword=keyword, current_user=current_user, db=db)

# @router.get("/article/datum/download", tags=["datum"])
# async def download(title: str, db: Session = Depends(get_db)):
#     return article_datum_service.download(title=title, db=db)
