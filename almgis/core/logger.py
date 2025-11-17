# from qga.logger import getQgaLogger
from qga import Settings
from qga.core.logger import getQgaLogger

# from almgis import settings_general

def setupLoggerrrr():

    Qga.Logger = getQgaLogger(Settings.General.app_modul_name + '.log')
