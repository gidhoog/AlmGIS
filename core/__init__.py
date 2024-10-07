from contextlib import contextmanager
from core import config
from core.logger import LOGGER

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listen


def load_spatialite(dbapi_conn, connection_record):
    """
    ermöglicht die verwendung von  spatialite mit geoalchemy2;
    siehe: https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html
    :param dbapi_conn:
    :param connection_record:
    :return:
    """
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('C:/work/_anwendungen/OSGeo4W/bin/mod_spatialite.dll')
    # dbapi_conn.load_extension('/usr/lib/mod_spatialite.so')
    # dbapi_conn.load_extension(str(config.mod_spatialite_dll))

engine = create_engine(f"sqlite:///{config.alm_data_db_path}",
                       echo=True)
listen(engine, 'connect', load_spatialite)

"""verwende die Klasse 'DbSession' für Sessions bei denen du 'commit' und
'close' steuerst"""
DbSession = sessionmaker()
DbSession.configure(bind=engine)
""""""

"""verwende den Contextmanager 'db_session_cm' für schnelle Datenbankzugriffe;
danach wird automatisch 'commit' und 'close' ausgeführt"""
@contextmanager
def db_session_cm(expire_on_commit=True, name=''):
    # print(f"- create SESSION - {name}")
    LOGGER.info(f"--- create SESSION: {name} "
                f"(expire_on_commit={expire_on_commit})")
    session = DbSession()
    session.expire_on_commit = expire_on_commit
    try:
        yield session
        # print(f"-- commit SESSION -- {name}")
        LOGGER.info(f"--- commit SESSION: {name})")
        session.commit()
    except:
        # print(f"-- except SESSION -- {name}")
        session.rollback()
        LOGGER.info(f"--- except SESSION: {name})")
        raise
    finally:
        # print(f"--- close SESSION --- {name}")
        session.close()
        LOGGER.info(f"--- close SESSION: {name})")

""""""
