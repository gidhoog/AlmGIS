# from sqlalchemy.orm import sessionmaker

from almgis.core.settings import AlmSettingsPaths, AlmSettingsConstants, AlmSettingsUser, AlmSettingsApp, \
    AlmSettingsProject

# from almgis.settings import AlmSettingsUser, AlmSettingsApp, AlmSettingsProject, \
#     AlmSettingsConstants, AlmSettingsPaths, AlmSettingsColors, \
#     AlmSettingsGeneral
# from almgis import data_model


"""verwende settings systemweit"""
# settings_general = AlmSettingsGeneral()
# settings_colors = AlmSettingsColors()
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

# ProjectSessionCls = sessionmaker()
# CommonSessionCls = sessionmaker()
