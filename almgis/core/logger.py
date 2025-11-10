# from qga.logger import getQgaLogger
from qga import Qga
from qga.core.logger import getQgaLogger

# from almgis import settings_general

"""definiere logger"""
Logger = getQgaLogger(Qga.SettingsGeneral.app_modul_name + '.log')
""""""
