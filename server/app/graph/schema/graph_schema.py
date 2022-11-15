from pydantic import BaseModel


class GraphSchema(BaseModel):
    name: str
    title: str

