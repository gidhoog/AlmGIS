from PyQt5.QtCore import pyqtSignal
from qgis._gui import QgsOptionsPageWidget

from almgis.resources.ui_py import settings_colors_wdg_UI


class SettingPageAlmgisDlgGui(QgsOptionsPageWidget,
                             settings_colors_wdg_UI.Ui_AlmSettingsAlmgis):

    save_data_sgn = pyqtSignal(object)

    def __init__(self, ctrl=None):
        super().__init__()
        self.setupUi(self)

        self._ctrl = ctrl

        self._current_dto = None