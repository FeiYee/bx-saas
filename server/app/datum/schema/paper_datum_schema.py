from datetime import datetime
from pydantic import BaseModel


class PaperDatumSchema(BaseModel):
    id: str | None = None
    paper_id: str | None = None
    name: str | None = None
    description: str | None = None
    url: str | None = None
    type: int | None = None
    file_name: str | None = None
    file_path: str | None = None
    file_size: str | None = None
    file_type: str | None = None
    upload_date: datetime | None = None

    class Config:
        orm_mode = True
