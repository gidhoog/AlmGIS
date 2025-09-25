from qga.core.info_button import QgaInfoButton

from almgis import CommunitySessionCls
from almgis.database.models import DmInfoButton


class AlmInfoButton(QgaInfoButton):

    def __init__(self, ui=None):
        super(AlmInfoButton, self).__init__(ui)

        self.dmc_info_button = DmInfoButton
        self.session = CommunitySessionCls()
