from pathlib import Path

from PyQt5.QtCore import QSettings
from qga.settings import QgaSettings, QgaSettingsProject

from almgis.data_model import BSettings
# from almgis.data_session import db_session_cm
# from almgis import db_session_cm


class AlmSettingsUser(QgaSettings):
    """
    klasse für die benutzer-spezifischen settings;
    settings werden in eine ini-datei im benutzerverzeichnis geschrieben (
    e.g.: /home/user/.config/NoeAbb/AlmGIS.ini)
    """

    attr_list = [
        ('h1', 'h1'),
        ('h2', 'h2'),
        ('agn/h1', 'agn-h1'),
        ('agn/h3', 'agn-h3'),
        ('agn/project_start_selector', 'True'),
        ('paths/last_project_file', 'ggg')
    ]

    def __init__(self):
        super().__init__(QSettings.IniFormat,
                         QSettings.UserScope,
                         'NoeAbb',
                         'AlmGIS')

        self.sync()
        self.updateSettings()


class AlmSettingsApp(QgaSettings):

    def __init__(self):

        ppp = Path().absolute().joinpath('AlmGIS.ini')
        super().__init__(str(ppp), QSettings.IniFormat)

        # self.clear()
        self.sync()


class AgnSettingsProject(QgaSettingsProject):

    # db_session_cm = db_session_cm
    settings_datamodel = BSettings
