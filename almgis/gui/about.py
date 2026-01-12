from PyQt5.QtWidgets import QWidget
from qga import Qga
from qga.gui.about import QgaAboutDialog


class AlmAboutDialog(QgaAboutDialog):

    def __init__(self, parent=None):
        super(AlmAboutDialog, self).__init__(parent)

        self.about_wdg = QWidget()

        self.dialog_window_title = Qga.Settings.General.app_display_name