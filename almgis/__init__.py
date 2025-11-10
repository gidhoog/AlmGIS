# from sqlalchemy.orm import sessionmaker
from qga import Qga

from almgis.core.settings import AlmSettingsUser

# from almgis.settings import AlmSettingsUser, AlmSettingsApp, AlmSettingsProject, \
#     AlmSettingsConstants, AlmSettingsPaths, AlmSettingsColors, \
#     AlmSettingsGeneral
# from almgis import data_model


"""verwende settings systemweit"""
# settings_general = AlmSettingsGeneral()
# settings_colors = AlmSettingsColors()
# settings_paths = AlmSettingsPaths()
# settings_constants = AlmSettingsConstants()

settings_user = AlmSettingsUser()
# settings_app = AlmSettingsApp()
# settings_project = AlmSettingsProject()
""""""

"""aktualisiere die ini-Dateien beim App-Start, falls neu Einträge eingefügt
worden sind"""
Qga.SettingsApp.updateSettings()
settings_user.updateSettings()
""""""

# ProjectSessionCls = sessionmaker()
# CommonSessionCls = sessionmaker()
