from pathlib import Path

from qga.config import Config as Cnfg, PathsAndFiles as PaF
# from qga import Config as Cnfg, PathsAndFiles as PaF

# import yaml

# from qga import app_config


class PathsAndFiles(PaF):
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
        '../_internal', 'dll', 'mod_spatialite.dll'
    )


class Config(Cnfg):

    app_modul_name = 'almggis'

    # @staticmethod
    # def homePath(app_modul_str):
    #
    #     if app_config['debug']:
    #         return Path().joinpath('_internal')
    #     else:
    #         return Path.home().joinpath('AppData', 'Roaming', app_modul_str)
    #
    # @staticmethod
    # def userConfigFile():
    #     """
    #     path to the user-config-file (usualy in the user-home-path)
    #     :return:
    #     """
    #
    #     return Config.homePath(app_config['app_modul_name']).joinpath('user_config.yaml')
    #
    # @staticmethod
    # def userConfig():
    #     """
    #     content of the user-config-file
    #     :return:
    #     """
    #
    #     with open(Config.userConfigFile(), 'r') as file_object:
    #         user_config = yaml.load(file_object, yaml.SafeLoader)
    #
    #     return user_config
    #
    # @staticmethod
    # def appConfig():
    #     """
    #     content of the app-config-file
    #     :return:
    #     """
    #     return app_config
