import os
from sqlalchemy import inspect

def convertMtoHa(m, decimal=4):
    """
    umwandlung von m² auf ha
    """

    dec_string = "{:." + str(decimal) + "f}"
    ha = dec_string.format(m / 10000).replace('.', ',')

    return ha

def getUser():
    """
    erhalte den aktuellen Benutzer

    :return: str
    """
    return os.getlogin()

def getMciState(mci):

    insp = inspect(mci)

    if insp.transient:
        return "transient"

    if insp.pending:
        return "pending"

    if insp.persistent:
        return "persistent"

    if insp.deleted:
        return "deleted"

    if insp.detached:
        return "detached"

def getMciSession(mci):

    return inspect(mci).session
