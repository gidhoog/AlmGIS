from pathlib import Path

"""Pfade und Dateien:"""
# alm_data_db_path = Path('G:/ALM/AlmGIS/db/dev/test/alm_daten.db')
alm_data_db_path = Path('G:/ALM/AlmGIS/db/test/alm_daten_01.db')
# alm_data_db_path = Path('C:/work/Projekte/AlmGIS/almgis/data/alm_daten.db')
# alm_data_db_path = Path('/home/franz/IT/Dev/Projekte/AlmGIS/alm_daten.db')
# gdb_import_path = pathlib.Path().absolute().joinpath('import_gdb')
print_template_path = (Path().absolute()
                       .joinpath('_internal', 'print_templates'))

almgis_home_path = Path.home().joinpath('AppData', 'Roaming', 'almgis')

mod_spatialite_dll = Path().absolute().joinpath(
    '_internal', 'dll', 'mod_spatialite.dll'
)
""""""

font_family = 'Calibri'