from PyQt5.QtCore import pyqtSignal
from qga.core.base import QgaBaseObject

from almgis.gui.settings_wdg_gui import SettingPageAlmgisDlgGui


class SettingsAlmgisDlg(QgaBaseObject):

    # _dto_cls = SettingPageStartDlgDTO

    update_data_sgn = pyqtSignal(object)
    apply_data_sgn = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = SettingPageAlmgisDlgGui(self)

    def load_data(self):
        pass