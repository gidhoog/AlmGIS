from pathlib import Path

from PyQt5.QtGui import QColor
from qga.config import Config as Cnfg


class Config(Cnfg):

    app_modul_name = 'almgis'
    allow_project_start_selector = False

    class PathsAndFiles(Cnfg.PathsAndFiles):
        """
        Pfade und Dateien
        """

        data_db_path = Path('G:/ALM/AlmGIS/db/dev/test/almgis_daten.db')
        # data_db_path = Path('G:/ALM/AlmGIS/db/test/alm_daten_01.db')
        # data_db_path = Path('C:/work/Projekte/AlmGIS/almgis/data/alm_daten.db')
        # data_db_path = Path('/home/franz/IT/Dev/Projekte/AlmGIS/alm_daten.db')
        # gdb_import_path = pathlib.Path().absolute().joinpath('import_gdb')

        # setting_db_path =
        print_template_path = (Path().absolute()
                               .joinpath('../_internal', 'print_templates'))

        # setting_db_path = Path().absolute().joinpath(
        #     '_internal', 'almgis_settings.db')
        # setting_db_path = Path().absolute().joinpath(
        #     '_internal', 'agn_setting.db')

        almgis_home_path = Path.home().joinpath('AppData', 'Roaming', '')

        mod_spatialite_dll = Path().absolute().joinpath(
            '_internal', 'dll', 'mod_spatialite.dll'
        )

    class Colors(Cnfg.Colors):

        data_view_selection = QColor(57, 202, 171)  # tuerkis
        canvas_selection = QColor(92, 202, 183)  # tuerkis

        deleted_data = QColor(240, 180, 180)  # schaches rot
        edited_data = QColor(250, 230, 120)  # schaches gelb
        added_data = QColor(220, 240, 160)  # schwaches grün
