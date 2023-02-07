import uuid
from passlib.context import CryptContext
from fastapi import File, Form, UploadFile
from config import BASE_DIR

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_uuid():
    id = str(uuid.uuid4()).replace('-', '')
    return id


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def write_file(file: UploadFile, write_path: str = '', write_sub_path: str = ''):
    content = await file.read()
    file_dir = BASE_DIR / 'asset'
    if write_path:
        file_dir = file_dir / write_path
    if not file_dir.exists():
        file_dir.mkdir()
    if write_sub_path:
        file_dir = file_dir / write_sub_path
    if not file_dir.exists():
        file_dir.mkdir()
    file_path = file_dir / file.filename
    file_path.write_bytes(content)
    return file_path
