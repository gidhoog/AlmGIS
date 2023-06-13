import pathlib

"""Pfade und Dateien:"""
alm_data_db_path = pathlib.Path().absolute().joinpath('data', 'alm_daten.db')
gdb_import_path = pathlib.Path().absolute().joinpath('import_gdb')
print_template_path = pathlib.Path().absolute().joinpath('core', 'print_templates')
""""""