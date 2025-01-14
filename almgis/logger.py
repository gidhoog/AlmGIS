#!/usr/bin/env python

# import logging

from qga.logger import getQgaLogger

from almgis import Config

"""definiere config"""
config = Config()
""""""

"""definiere logger"""
Logger = getQgaLogger(config.app_modul_name + '.log')
""""""


# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s  - %(module)s.%(funcName)s: %(levelname)-9s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#
# # create console handler and set level to DEBUG
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(module)s.%(funcName)s: %(levelname)s - %(message)s")
# console_handler.setFormatter(formatter)
# logging.getLogger().addHandler(console_handler)
#
# """log sqlalchemy-log to log-file;
# see https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging"""
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# """"""
#
# LOGGER = logging.getLogger('almgis')
