import logging
from sqlalchemy.orm import Session
from app.core.database import engine, Base, DBSession
from app.system.model.user import User
import app.datum.model.datum
import app.search.model.keyword
import app.search.model.search
import app.search.model.search_record
import app.stats.model.stats_download
import app.system.model.user
import app.system.model.org
import app.system.model.org_user


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_user(db: Session):
    username = 'admin'
    user = db.query(User).filter(
        username == username
    ).first()
    if not user:
        user = User(username=username, password='123', is_admin=True, name='Admin')
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
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == '__main__':
    migrate()
