from enum import Enum
from pathlib import Path

from PyQt5.QtCore import QSettings
from qga.settings import QgaSettings, QgaSettingsProject, QgaSettingsGeneral, \
    QgaSettingsColors, QgaSettingsPaths, QgaSettingsConstants

from almgis.data_model import McSettings


class AlmSettingsGeneral(QgaSettingsGeneral):
    """
    Klasse für alle allgemeinen Einstellungen;

        - Einstellungen die bei kompilierten/gepackten Programmen
         verändert werden können müssen in der Klasse 'AlmSettingsApp'
         geschrieben werden;

        - Einstellungen die vom User verändert werden können müssen
        in der Klasse 'AlmSettingsUser' geschrieben werden;
    """

    app_modul_name = 'almgis'
    app_display_name = 'AlmGIS'
    project_file_suffix = 'alm'

    help_url = 'https://portal.noe.gv.at/at.gv.noe.abb-wiki-p/wiki/DBALM'


class AlmSettingsColors(QgaSettingsColors):
    """
    Klasse für alle Einstellungen die Farben betreffen;

        - Einstellungen die bei kompilierten/gepackten Programmen
         verändert werden können müssen in der Klasse 'AlmSettingsApp'
         geschrieben werden;

        - Einstellungen die vom User verändert werden können müssen
        in der Klasse 'AlmSettingsUser' geschrieben werden;
    """


class AlmSettingsPaths(QgaSettingsPaths):
    """
    Klasse für alle Einstellungen die Pfade und Speicherorte von Dateien
     betreffen;

        - Einstellungen die bei kompilierten/gepackten Programmen
         verändert werden können müssen in der Klasse 'AlmSettingsApp'
         geschrieben werden;

        - Einstellungen die vom User verändert werden können müssen
        in der Klasse 'AlmSettingsUser' geschrieben werden;
    """

    data_db_path = Path('G:/ALM/AlmGIS/db/dev/test/almgis_daten.alm')

    print_template_path = (Path().absolute()
                           .joinpath('../_internal',
                                     'print_templates'))


class AlmSettingsConstants(QgaSettingsConstants):
    """
    Klasse für konstante Werte;
    """

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
    klasse für benutzer-spezifischen Einstellungen;
    Einstellungen werden in eine ini-datei im benutzerverzeichnis geschrieben (
    e.g.: '/home/user/.config/NoeAbb/AlmGIS.ini' oder
    'C:\Users\ZNFF\AppData\Roaming\NoeAbb.AlmGIS.ini')
    """


    attr_list = [
        ('paths/last_project_file', '')
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
        ('use_project_start_selector', 'False'),
        ('static_project_file', 'G:/ALM/AlmGIS/db/dev/test/almgis_daten.alm')
    ]

    def __init__(self):

        ppp = Path().absolute().joinpath('AlmGIS.ini')
        super().__init__(str(ppp), QSettings.IniFormat)

        # self.clear()
        self.sync()


class AlmSettingsProject(QgaSettingsProject):

    # session_cm = session_cm
    settings_mc = McSettings
