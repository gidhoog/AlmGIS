from qga import Qga
from qga.core.dialog import QgaDialog


class AlmDialog(QgaDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # self.ui.setWindowTitle(Qga.Settings.General.app_display_name)
        self.enableAccept = True
