from core.scopes.akte import abgrenzung_UI
from qgis.PyQt.QtWidgets import QWidget


class Abgrenzung(QWidget, abgrenzung_UI.Ui_Abgrenzung):

    def __init__(self, parent=None, item=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)