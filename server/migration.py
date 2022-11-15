import logging
from app.core.database import engine, Base, DBSession
import app.datum.model.datum
import app.search.model.keyword
import app.search.model.search
import app.search.model.search_record
import app.stats.model.stats_download
import app.system.model.user
import app.system.model.org
import app.system.model.org_user
import app.system.model.menu
import app.system.model.website


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
    logger.info('migrate database start')
    Base.metadata.create_all(bind=engine)
    logger.info('migrate database end')

    try:
        db = DBSession()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == '__main__':
    migrate()
