from pydantic import BaseModel


class DatumSchema(BaseModel):
    title: str
    name: str
    file: str

    class Config:
        orm_mode = True
