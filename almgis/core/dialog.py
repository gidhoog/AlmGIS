from qga.core.dialog import QgaDialog

from almgis import settings_general


class AlmDialog(QgaDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui.setWindowTitle(settings_general.app_display_name)
        self.enableAccept = True