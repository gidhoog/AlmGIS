from contextlib import contextmanager
from pathlib import Path

from qga.info_button import QgaInfoButton
from sqlalchemy import create_engine

from almgis import CommunitySessionCls, settings_user
from almgis.data_model import DmInfoButton
from almgis.data_session import session_cm

# info_btn_db = (Path().absolute()
#                            .joinpath('almgis',
#                                      'info_button_alm.db'))
#
# engine_string = 'sqlite:///' + str(info_btn_db)
# app_engine = create_engine(engine_string, echo=False)
# # listen(app_engine,
# #        'connect',
# #        (lambda x, l=logger: loadSpatialite(x, l))
# #        )
# CommunitySessionCls.configure(bind=app_engine)

# community_session_cls = CommunitySessionCls

@contextmanager
def session_cm():
    # session = CommunitySessionCls()
    session = CommunitySessionCls()
    try:
        yield session
        session.commit()
    except:
        print(f'cannot use session_cm')
        session.rollback()
        raise
    finally:
        session.close()

class AlmInfoButton(QgaInfoButton):

    def __init__(self, parent=None):
        super(AlmInfoButton, self).__init__(parent)

        self.session_cm = session_cm
        self.session = CommunitySessionCls()
        self.dmc_info_button = DmInfoButton
        self.settings_user = settings_user
