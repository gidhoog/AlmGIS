# from qga.logger import getQgaLogger
from qga import Qga
from qga.core.logger import getQgaLogger

# from almgis import settings_general

def setupLoggerrrr():

    Qga.Logger = getQgaLogger(Qga.Settings.General.app_modul_name + '.log')
