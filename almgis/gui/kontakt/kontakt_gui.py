from PyQt5.QtWidgets import QMainWindow

from almgis.resources.ui_py.kontakt import kontakt_UI


class KontaktGui(QMainWindow, kontakt_UI.Ui_KontaktGui):

    def __init__(self, ctrl=None):
        super(KontaktGui, self).__init__()
        self.setupUi(self)