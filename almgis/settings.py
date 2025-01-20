from enum import Enum
from pathlib import Path

from PyQt5.QtCore import QSettings
from qga.settings import QgaSettings, QgaSettingsProject, QgaSettingsGeneral, \
    QgaSettingsColors, QgaSettingsPaths, QgaSettingsConstants

from almgis.data_model import McSettings


class AlmSettingsGeneral(QgaSettingsGeneral):

    app_modul_name = 'almgis'
    allow_project_start_selector = False


class AlmSettingsColors(QgaSettingsColors): pass


class AlmSettingsPaths(QgaSettingsPaths):

    data_db_path = Path('G:/ALM/AlmGIS/db/dev/test/almgis_daten.db')

    print_template_path = (Path().absolute()
                           .joinpath('../_internal',
                                     'print_templates'))


class AlmSettingsConstants(QgaSettingsConstants):

    class CostCenterType(Enum):
        SITE = 1
        CROP = 4

    class AttributeDataType(Enum):
        TEXT = 0
        INTEGER = 1
        FLOAT = 2
        LIST = 3

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

    attr_list = [
        ('project_start_selector', 'False')
    ]

    def __init__(self):

        ppp = Path().absolute().joinpath('AlmGIS.ini')
        super().__init__(str(ppp), QSettings.IniFormat)

        # self.clear()
        self.sync()


class AlmSettingsProject(QgaSettingsProject):

    # session_cm = session_cm
    settings_datamodel = McSettings
