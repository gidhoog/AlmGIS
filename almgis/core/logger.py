import logging
from qga.core.logger import setupQgaLogger

def setupAlmLogger():

    setupQgaLogger()
    log_file_name = 'almgis.log'

    """create a 'root' logger for use in the app"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    """"""

    """create handlers"""
    file_handler = logging.FileHandler(log_file_name, mode='w')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    """"""

    # datefmt = '%Y-%m-%d %H:%M:%S'

    """create and set formater"""
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # formatter = logging.Formatter('%(asctime)s  - %(levelname)-9s: %(module)s.%(funcName)s: %(message)s')
    formatter = logging.Formatter('%(asctime)s  - %(levelname)-9s>> %(name)s: %(message)s')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    """"""

    """add handler to logger"""
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    """"""
