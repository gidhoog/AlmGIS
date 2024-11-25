#!/usr/bin/env python

import logging

# logging.basicConfig(filename="openfarm.log", filemode='w', level=logging.DEBUG,
#                              format='%(asctime)s  - %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#
# logging.getLogger('openfarm')

#def LOGGER():

# write log to log-file
# logging.basicConfig(filename="almgis.log", filemode='w', level=logging.DEBUG,
#                     format='%(asctime)s  - %(module)s.%(funcName)s: %(levelname)-9s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  - %(module)s.%(funcName)s: %(levelname)-9s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# create console handler and set level to DEBUG
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(module)s.%(funcName)s: %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

"""log sqlalchemy-log to log-file;
see https://docs.sqlalchemy.org/en/20/core/engines.html#dbengine-logging"""
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
""""""

# create error file handler and set level to error
# handler = logging.FileHandler("error.log", "w", encoding=None, delay="true")
# handler.setLevel(logging.ERROR)
# formatter = logging.Formatter("%(levelname)s - %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# create debug file handler and set level to debug
#file_handler = logging.FileHandler("all2.log", "w")
#file_handler.setLevel(logging.DEBUG)
#formatter = logging.Formatter("%(levelname)s - %(message)s")
#file_handler.setFormatter(formatter)
#logger.addHandler(file_handler)

LOGGER = logging.getLogger('almgis')

#return logger


#logger.debug("hi there")

