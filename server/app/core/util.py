import uuid


def get_uuid():
    id = str(uuid.uuid4()).replace('-', '')
    return id
