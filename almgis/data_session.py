from contextlib import contextmanager

# from qga import data_session

from almgis import AlmSessionCls
# from almgis.data_model import DmSettings
from almgis.logger import Logger

"""verwende den Contextmanager 'session_cm' für schnelle Datenbankzugriffe;
danach wird automatisch 'commit' und 'close' ausgeführt"""
@contextmanager
def session_cm(expire_on_commit=True, name=''):
    # print(f"- create SESSION - {name}")
    Logger.info(f"--- create SESSION: {name} "
                f"(expire_on_commit={expire_on_commit})")
    session = AlmSessionCls()
    session.expire_on_commit = expire_on_commit
    try:
        yield session
        # print(f"-- commit SESSION -- {name}")
        Logger.info(f"--- commit SESSION: {name})")
        session.commit()
    except:
        # print(f"-- except SESSION -- {name}")
        session.rollback()
        Logger.info(f"--- except SESSION: {name})")
        raise
    finally:
        # print(f"--- close SESSION --- {name}")
        session.close()
        Logger.info(f"--- close SESSION: {name})")

""""""

# def getSettingProjectValue(code):
#     """
#     lese die Einstellung mit dem übergebenen Code aus der Datenbank
#     und liefere den Wert zurück
#
#     :param code: str
#     :return: value
#     """
#     with session_cm(expire_on_commit=False,
#                     name=f'get project setting value \'{code}\'') as session:
#         stmt = select(DmSettings).where(DmSettings.code == code)
#         query = session.scalars(stmt).first()
#
#     return query.value
