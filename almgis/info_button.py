from contextlib import contextmanager
from pathlib import Path

from qga.info_button import InfoButton
from sqlalchemy import create_engine

from almgis import InfoBtnSessionCls
from almgis.data_model import McInfoButton
from almgis.data_session import session_cm

info_btn_db = (Path().absolute()
                           .joinpath('almgis',
                                     'info_button_alm.db'))

engine_string = 'sqlite:///' + str(info_btn_db)
app_engine = create_engine(engine_string, echo=False)
# listen(app_engine,
#        'connect',
#        (lambda x, l=logger: loadSpatialite(x, l))
#        )
InfoBtnSessionCls.configure(bind=app_engine)

@contextmanager
def info_session_cm():
    session = InfoBtnSessionCls()
    try:
        yield session
        session.commit()
    except:
        print(f'cannot use info_session_cm')
        session.rollback()
        raise
    finally:
        session.close()

class AlmInfoButton(InfoButton):

    def __init__(self, parent=None):
        super(AlmInfoButton, self).__init__(parent)

        self.session_cm = info_session_cm
        self.session = InfoBtnSessionCls()
        self.mc_info_button = McInfoButton

        # self.init_tool_tip()
