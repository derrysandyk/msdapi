import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

logger = logging.getLogger()
@contextmanager
def session_scope(engine=None):
    # print('\nDATABASE_URL: ', os.environ.get("DATABASE_URL"))
    if not engine:
        # an Engine, which the Session will use for connection resources
        engine = create_engine("oracle+cx_oracle://mbu:asmmbuapp05it@192.168.103.81:1521/OPASM1")

    """Provide a transactional scope around a series of operations."""
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error('{} - {}'.format(type(e), str(e)))
        session.rollback()
        raise
    finally:
        session.close()
