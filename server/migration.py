import logging

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import engine, Base, DBSession
from app.core.util import get_password_hash
from app.system.model.user import User
import app.datum.model.article
import app.datum.model.article_extract
import app.datum.model.article_datum
import app.datum.model.paper
import app.datum.model.paper_datum
import app.datum.model.datum
import app.graph.model.graph
import app.search.model.keyword
import app.search.model.search
import app.search.model.search_record
import app.system.model.user
import app.system.model.org
import app.system.model.org_user

import app.wechat.model.wechat


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_user(db: Session):
    username = 'admin'
    user = db.query(User).filter(
        username == username
    ).first()
    if not user:
        user = User(username=username, password=get_password_hash('123'), is_admin=True, name='Admin')
        db.add(user)
        db.commit()


def migrate():
    logger.info('migrate database start')
    Base.metadata.create_all(bind=engine)
    logger.info('migrate database end')

    try:
        db = DBSession()
        init_user(db)
        # Try to create session to check if DB is awake
        db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == '__main__':
    migrate()
