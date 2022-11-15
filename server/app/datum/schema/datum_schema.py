from pydantic import BaseModel


class DatumSchema(BaseModel):
    name: str
    file: str

    class Config:
        orm_mode = True
