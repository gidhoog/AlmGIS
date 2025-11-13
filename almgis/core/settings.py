from enum import Enum
from pathlib import Path

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QColor
# from qga.settings import QgaSettings, QgaSettingsProject, QgaSettingsGeneral, \
#     QgaSettingsColors, QgaSettingsPaths, QgaSettingsConstants
from qga import Qga
from qga.core.logger import getQgaLogger
from qga.core.settings import QgaSettingsGeneral, QgaSettingsColors, \
    QgaSettingsPaths, QgaSettingsConstants, QgaSettingsProject, \
    QgaSettingsUser, QgaSettingsApp

from almgis.database.models import DmSettings


def setupSettings():
    """
    set here AlmGIS specific settings
    """

    Qga.Settings.General = AlmSettingsGeneral()
    Qga.Settings.Colors = AlmSettingsColors()
    Qga.Settings.Paths = AlmSettingsPaths()
    Qga.Settings.Constants = AlmSettingsConstants()

    Qga.Settings.Project = AlmSettingsProject()
    Qga.Settings.User = AlmSettingsUser()
    Qga.Settings.App = AlmSettingsApp()

    # Qga.SettingsGeneral = AlmSettingsGeneral()
    # Qga.SettingsColors = AlmSettingsColors()
    # Qga.SettingsPaths = AlmSettingsPaths()
    # Qga.SettingsConstants = AlmSettingsConstants()
    # Qga.SettingsProject = AlmSettingsProject()
    #
    # Qga.SettingsUser = AlmSettingsUser()
    # Qga.SettingsApp = AlmSettingsApp()

    # """definiere logger"""
    # Logger = getQgaLogger(Qga.SettingsGeneral.app_modul_name + '.log')
    # """"""


class AlmSettingsGeneral(QgaSettingsGeneral):

    app_modul_name = 'almgis'
    app_display_name = 'AlmGIS'
    project_file_suffix = 'alm'

    help_url = 'https://portal.noe.gv.at/at.gv.noe.abb-wiki-p/wiki/DBALM'

    app_version = '0.0.2'
    db_version = '0.0.1'


class AlmSettingsColors(QgaSettingsColors):

    # data_view_selection = QColor(100, 100, 100)  # grau
    pass

class AlmSettingsPaths(QgaSettingsPaths): ...

class AlmSettingsConstants(QgaSettingsConstants): ...

class AlmSettingsProject(QgaSettingsProject):

    settings_dmc = DmSettings


class AlmSettingsUser(QgaSettingsUser):

    company_name = 'NoeAbb'
    app_name = 'AlmGIS'


class AlmSettingsApp(QgaSettingsApp):

    ini_file_name = "AlmGIS.ini"

    attr_list = [
        ('use_project_start_selector', 'True'),
        ('static_project_file', ''),
        ('database/type', 'sqlite'),  # see https://docs.sqlalchemy.org/en/20/core/engines.html
        ('database/host', 'host')
    ]


# class AlmSettingsUser(QgaSettings):
#     """
#     klasse für benutzer-spezifischen Einstellungen;
#     Einstellungen werden in eine ini-datei im benutzerverzeichnis geschrieben
#     (e.g.: '/home/user/.config/NoeAbb/AlmGIS.ini'
#     oder C:/Users/ZNFF/AppData/Roaming/NoeAbb/AlmGIS.ini
#     oder /home/franz/IT/_distroboxes/.config/NoeAbb/AlmGIS.ini bei einer
#     distrobox)
#     """
#
#     attr_list = [
#         ('start_dialog', 'True'),
#         ('default_start_option', 'LAST'),  # LAST, OTHER, NEW, NONE
#         ('info_btn_editable', 'True'),
#         ('paths/last_project_file', '--'),
#         ('paths/common_db_file', '*.almgis_common.db')
#     ]
#
#     def __init__(self):
#         super().__init__(QSettings.IniFormat,
#                          QSettings.UserScope,
#                          'NoeAbb',
#                          'AlmGIS')
#
#         self.sync()
#         self.updateSettings()


# class AlmSettingsApp(QgaSettings):
#
#     attr_list = [
#         ('use_project_start_selector', 'True'),
#         ('static_project_file', ''),
#         ('database/type', 'sqlite'),  # see https://docs.sqlalchemy.org/en/20/core/engines.html
#         ('database/host', 'host')
#     ]
#
#     def __init__(self):
#
#         ppp = Path().absolute().joinpath('AlmGIS.ini')
#         super().__init__(str(ppp), QSettings.IniFormat)
#
#         # self.clear()
#         self.sync()

