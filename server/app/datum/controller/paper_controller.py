from fastapi import APIRouter, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependence import get_db
from app.system.model.user import User
from app.home.security.auth import get_current_user
from ..schema.paper_schema import PaperSchema
from ..service.paper_service import paper_service


router = APIRouter()


@router.get("/paper", response_model=list[PaperSchema], tags=["paper"])
async def get(db: Session = Depends(get_db)):
    return paper_service.find(db=db)


@router.post("/paper", response_model=PaperSchema, tags=["paper"])
async def create(name: str = Form(default=''), description: str = Form(default=''), user_id: str | None = Form(default=None), file: UploadFile = File(),
                 current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await paper_service.create(name=name, description=description, file=file, user_id=user_id,
                                      current_user=current_user, db=db)


@router.put("/paper/{paper_id}", response_model=PaperSchema, tags=["paper"])
async def put(paper_id: str, name: str = Form(default=''), description: str = Form(default=''), file: UploadFile | None = None, db: Session = Depends(get_db)):
    return await paper_service.update(paper_id=paper_id, name=name, description=description, file=file, db=db)


@router.get("/paper/query", tags=["paper"])
async def get_paper_by_title(title: str = '', db: Session = Depends(get_db)):
    return paper_service.find_by_title(title=title, db=db)


@router.get("/paper/title", tags=["paper"])
async def get_article_title(db: Session = Depends(get_db)):
    return paper_service.find_article_title(db=db)

