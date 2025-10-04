from qga.core.info_button import QgaInfoButton

from almgis import CommonSessionCls
from almgis.database.models import DmInfoButton
from almgis.database.sessions import AlmCommonSessionCm


class AlmInfoButton(QgaInfoButton):

    def __init__(self, ui=None):
        super(AlmInfoButton, self).__init__(ui)

        self.dmc_info_button = DmInfoButton
        self.session = CommonSessionCls()
        self.session_cm = AlmCommonSessionCm
