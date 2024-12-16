from pathlib import Path

from PyQt5.QtCore import QSettings
from qga.settings import QgaSettings


class AlmSettingsUser(QgaSettings):

    def __init__(self):
        super().__init__(QSettings.IniFormat,
                         QSettings.UserScope,
                         'NoeAbb',
                         'AlmGIS')

        # self.clear()
        self.sync()

        # self.setValue('user-sett-1', '111')


class AlmSettingsSys(QgaSettings):

    def __init__(self):

        ppp = Path().absolute().joinpath('AlmGIS.ini')
        super().__init__(str(ppp), QSettings.IniFormat)

        # self.clear()
        self.sync()
