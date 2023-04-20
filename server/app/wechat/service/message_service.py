from typing import Type, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session


class MessageService:

    def __init__(self):
        pass

    def receive(self, content: any, db: Session) -> any:
        print(content)
        return content


message_service = MessageService()
