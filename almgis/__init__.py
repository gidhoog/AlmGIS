from sqlalchemy.orm import sessionmaker
from almgis.settings import AlmSettingsUser, AlmSettingsApp, AlmSettingsProject, \
    AlmSettingsConstants, AlmSettingsPaths, AlmSettingsColors, \
    AlmSettingsGeneral
from almgis import data_model


"""verwende settings systemweit"""
settings_general = AlmSettingsGeneral()
settings_colors = AlmSettingsColors()
settings_paths = AlmSettingsPaths()
settings_constants = AlmSettingsConstants()

settings_user = AlmSettingsUser()
settings_app = AlmSettingsApp()
settings_project = AlmSettingsProject()
""""""

"""aktualisiere die ini-Dateien beim App-Start, falls neu Einträge eingefügt
worden sind"""
settings_app.updateSettings()
settings_user.updateSettings()
""""""

# """init session handling
# use the instance of 'DbSession' to connect to the db"""
# DbSession = sessionmaker()
# """"""
#
# """falls wenn tabellen aus mehreren datenbanken verwendet werden, dann
# binde diese nach fogenden Schema ein; kann aber erst nach definition der
# session_engine erfolgen, also nicht hier!!!"""
# # DbSession.configure(binds={data_model.BAkt: DbSession.data_engine,
# #                            data_model.BBanu: DbSession.data_engine,
# #                            # data_model.BSettings: setting_engine,
# #                            })
# """"""
