from contextlib import contextmanager
from almgis.logger import LOGGER

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listen

from almgis.data_model import *
from almgis.config import PathsAndFiles

"""important to load the app-config-file ('config.yaml')"""
""""""


def load_spatialite(dbapi_conn, connection_record):
    """
    ermöglicht die verwendung von  spatialite mit geoalchemy2;
    siehe: https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html
    :param dbapi_conn:
    :param connection_record:
    :return:
    """
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension(str(PathsAndFiles.mod_spatialite_dll))

data_engine = create_engine(f"sqlite:///{PathsAndFiles.data_db_path}",
                       echo=True)

# setting_engine = create_engine(f"sqlite:///{PathsAndFiles.setting_db_path}",
#                        echo=True)

listen(data_engine, 'connect', load_spatialite)

DBSessionData = sessionmaker()
DBSessionData.configure(bind=data_engine)

"""verwende die Klasse 'DbSession' für Sessions bei denen du 'commit' und
'close' steuerst"""
DbSession = sessionmaker()
# DbSession.configure(bind=data_engine)
DbSession.configure(binds={data_model.BAkt: data_engine,
                           data_model.BBanu: data_engine,
                           data_model.BBearbeitungsstatus: data_engine,
                           data_model.BCutKoppelGstAktuell: data_engine,
                           data_model.BErfassungsart: data_engine,
                           data_model.BGisLayer: data_engine,
                           data_model.BGisLayerMenu: data_engine,
                           data_model.BGisStyle: data_engine,
                           data_model.BGisStyleLayerVar: data_engine,
                           data_model.BGisScope: data_engine,
                           data_model.BGisScopeLayer: data_engine,
                           data_model.BGst: data_engine,
                           data_model.BGstAwbStatus: data_engine,
                           data_model.BGstEigentuemer: data_engine,
                           data_model.BGstEz: data_engine,
                           data_model.BGstNutzung: data_engine,
                           data_model.BGstVersion: data_engine,
                           data_model.BGstZuordnung: data_engine,
                           data_model.BGstZuordnungMain: data_engine,
                           data_model.BKatGem: data_engine,
                           data_model.BAbgrenzung: data_engine,
                           data_model.BAbgrenzungStatus: data_engine,
                           data_model.BKomplex: data_engine,
                           data_model.BKomplexName: data_engine,
                           data_model.BKontakt: data_engine,
                           data_model.BKontaktTyp: data_engine,
                           data_model.BKoppel: data_engine,
                           data_model.BRechtsgrundlage: data_engine,
                           data_model.BSys: data_engine,
                           data_model.McInfoButton: data_engine,
                           # data_model.BSettings: setting_engine,
                           })
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

@contextmanager
def db_session_cm_data(expire_on_commit=True, name=''):
    # print(f"- create SESSION - {name}")
    LOGGER.info(f"--- create SESSION: {name} "
                f"(expire_on_commit={expire_on_commit})")
    session = DBSessionData()
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
