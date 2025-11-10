# from qga.about import QgaAboutDialog
from qga import Qga
from qga.gui.about import QgaAboutDialog

# from almgis import AlmSettingsGeneral
from almgis.core.logger import Logger


# from almgis.logger import Logger


class AlmAboutDialog(QgaAboutDialog):

    def __init__(self, parent=None):
        super(AlmAboutDialog, self).__init__(parent)

        self.logger = Logger

        self.dialog_window_title = Qga.SettingsGeneral.app_display_name