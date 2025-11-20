from qga import Qga
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
