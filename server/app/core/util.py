import uuid
from passlib.context import CryptContext
from fastapi import File, Form, UploadFile
from config import BASE_DIR

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_uuid():
    return str(uuid.uuid4()).replace('-', '')


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


def get_file_type(file: UploadFile) -> int:
    content_type = 4
    if 'image' in file.content_type:
        content_type = 0
    elif 'sheet' in file.content_type:
        content_type = 1
    elif 'pdf' in file.content_type:
        content_type = 2
    elif 'zip' in file.content_type:
        content_type = 3

    return content_type
