from qga.gui.info_button_gui import QgaInfoButtonGui

from almgis import settings_user
from almgis.core.info_button import AlmInfoButton


class AlmInfoButtonGui(QgaInfoButtonGui):

    def __init__(self, parent=None):
        super(AlmInfoButtonGui, self).__init__(parent)

        self.ctrl = AlmInfoButton(self)

        self.settings_user = settings_user