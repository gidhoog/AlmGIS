import os

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
