# from qga.logger import getQgaLogger
from qga.core.logger import getQgaLogger

from almgis import settings_general

"""definiere logger"""
Logger = getQgaLogger(settings_general.app_modul_name + '.log')
""""""
