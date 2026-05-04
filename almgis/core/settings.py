from qga.core.settings import QgaSettingsManager, SettingsDef
from almgis.database.models import DmSettings


class AlmSettingsManager(QgaSettingsManager):

    USER_INI = "AlmGisUser.ini"
    APP_INI  = "AlmGisApp.ini"

    APP_MODUL_NAME = 'almgis'
    APP_DISPLAY_NAME = 'AlmGIS'
    PROJECT_FILE_SUFFIX = 'alm'

    APP_VERSION = '0.0.2'
    DB_PROJECT_VERSION = '0.0.1'

    PROJECT_SETTINGS_DMC = DmSettings

    SCHEMA = [
        #- User settings ──────────────────────────────────────────────
        SettingsDef("start_dialog",
                    'True',
                    scope="user",
                    val_type=bool,
                    label="verwende Start-Dialog"),
        SettingsDef("default_start_option",
                    1,  # one value from the class DefStartOption (0, 1, 2 or 3)
                    scope="user",
                    val_type=int,
                    label="Standardoption im Start-Dialog"),
        SettingsDef("path/last_project_file",
                    'C:/Daten/Temp/__Bev',
                    scope="user",
                    val_type=str,
                    label="BEV-Importverzeichnis"),
        SettingsDef("path/import_bev",
                    '',
                    scope="user",
                    val_type=str,
                    label="BEV-Importverzeichnis"),
        SettingsDef("info_btn_editable",
                    'False',
                    scope="user",
                    val_type=bool,
                    label="Infos bearbeitbar"),

        # ── App settings ───────────────────────────────────────────────
        SettingsDef("static_project_file",
                    '',
                    scope="app",
                    val_type=str,
                    label="statische Datenbank"),
        SettingsDef("database/type",
                    'sqlite',
                    scope="app",
                    val_type=str,
                    label="Datenbank-Typ"),
        SettingsDef("database/host",
                    'host',
                    scope="app",
                    val_type=str,
                    label="Datenbank-Host"),
        # ── App paths settings ───────────────────────────────────────────────
        SettingsDef("path/common_db_file",
                    '/home/franz/IT/Dev/Projekte/AlmGIS/almgis/database/almgis_common.db',
                    scope="app",
                    val_type=str,
                    label="zentrale Datenbank"),
        SettingsDef("path/print_template_path",
                    '../internal/print_templates',
                    scope="app",
                    val_type=str,
                    label="vorgegebenes Druckverzeichnis"),
        SettingsDef("path/base_help_url",
                    'https://portal.noe.gv.at/at.gv.noe.abb-wiki-p/wiki/DBALM',
                    scope="app",
                    val_type=str,
                    label="Hilfe-URL"),
        # ── App colors settings ───────────────────────────────────────────────
        SettingsDef("color/data_view_selection",
                    [57, 202, 171, 255],
                    scope="app",
                    val_type=str,
                    label="ausgewählte Tabelleneinträge"),
        SettingsDef("color/canvas_selection",
                    [92, 202, 183, 255],
                    scope="app",
                    val_type=str,
                    label="ausgewählte GIS-Objekte"),
    ]

    def __init__(self):
        super().__init__()

    """optional: cross-field validation"""
    def validate_all(self, data):
        errors = []
        if data.get("ui/font_size", 12) > 24 and data.get("ui/theme") == "dark":
            errors.append("Large fonts with dark theme may reduce readability.")
        return errors