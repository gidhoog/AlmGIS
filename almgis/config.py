from pathlib import Path

"""Pfade und Dateien:"""
data_db_path = Path('G:/ALM/AlmGIS/db/dev/test/almgis_daten.db')
# data_db_path = Path('G:/ALM/AlmGIS/db/test/alm_daten_01.db')
# data_db_path = Path('C:/work/Projekte/AlmGIS/almgis/data/alm_daten.db')
# data_db_path = Path('/home/franz/IT/Dev/Projekte/AlmGIS/alm_daten.db')
# gdb_import_path = pathlib.Path().absolute().joinpath('import_gdb')
print_template_path = (Path().absolute()
                       .joinpath('_internal', 'print_templates'))

# setting_db_path = Path().absolute().joinpath(
#     '_internal', 'almgis_settings.db')
setting_db_path = Path('G:/ALM/AlmGIS/db/dev/test/almgis_settings.db')

almgis_home_path = Path.home().joinpath('AppData', 'Roaming', 'almgis')

mod_spatialite_dll = Path().absolute().joinpath(
    '_internal', 'dll', 'mod_spatialite.dll'
)
""""""

font_family = 'Calibri'