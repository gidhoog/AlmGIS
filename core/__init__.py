from contextlib import contextmanager
from core import config

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
    # dbapi_conn.load_extension('C:/Program Files/OSGeo4W/bin/mod_spatialite.dll')
    dbapi_conn.load_extension('C:/work/_anwendungen/OSGeo4W/bin/mod_spatialite.dll')

engine = create_engine(f"sqlite:///{config.alm_data_db_path}")
listen(engine, 'connect', load_spatialite)

SessionFactory = sessionmaker()
SessionFactory.configure(bind=engine)


class DbSession:
    """
    klasse mit einer methode als context-manager für den datenzugriff
    """

    @staticmethod
    @contextmanager
    def session_scope():
        """stelle eine generelle session zur verfügung die für datenzugriffe
        auf die db verwendet werden kann"""
        # print(f"- create SESSION -")
        session = SessionFactory()
        session.expire_on_commit = False
        try:
            yield session
            # print(f"-- commit SESSION --")
            session.commit()
        except:
            # print("-- rollback SESSION --")
            session.rollback()
            raise
        finally:
            # print(f"--- close SESSION ---")
            session.close()
