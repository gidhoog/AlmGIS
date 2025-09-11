from enum import Enum
from pathlib import Path

from PyQt5.QtCore import QSettings
# from qga.settings import QgaSettings, QgaSettingsProject, QgaSettingsGeneral, \
#     QgaSettingsColors, QgaSettingsPaths, QgaSettingsConstants

from qga.core.settings import QgaSettingsGeneral, QgaSettingsColors, \
    QgaSettingsPaths, QgaSettingsConstants, QgaSettings, QgaSettingsProject


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

    app_version = '0.0.2'
    db_version = '0.0.1'


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

    # data_db_path = Path('G:/ALM/AlmGIS/db/dev/test/almgis_daten.alm')

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
    Einstellungen werden in eine ini-datei im benutzerverzeichnis geschrieben
    (e.g.: '/home/user/.config/NoeAbb/AlmGIS.ini'
    oder C:/Users/ZNFF/AppData/Roaming/NoeAbb/AlmGIS.ini
    oder /home/franz/IT/_distroboxes/.config/NoeAbb/AlmGIS.ini bei einer
    distrobox)
    """

    attr_list = [
        ('start_dialog', 'True'),
        ('default_start_option', 'LAST'),  # LAST, OTHER, NEW, NONE
        ('info_btn_editable', 'True'),
        ('paths/last_project_file', '--'),
        ('paths/common_db_file', '*.almgis_common.db')
    ]

    def __init__(self):
        super().__init__(QSettings.IniFormat,
                         QSettings.UserScope,
                         'NoeAbb',
                         'AlmGIS')

        self.sync()
        self.updateSettings()


class AlmSettingsApp(QgaSettings):

    attr_list = []

    def __init__(self):



        ppp = Path().absolute().joinpath('AlmGIS.ini')
        super().__init__(str(ppp), QSettings.IniFormat)

        # self.clear()
        self.sync()


class AlmSettingsProject(QgaSettingsProject): ...
