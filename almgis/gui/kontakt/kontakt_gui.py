from PyQt5.QtWidgets import QMainWindow

from almgis.resources.ui_py.kontakt import kontakt_UI


class KontaktEinzelGui(QMainWindow, kontakt_UI.Ui_KontaktGui):

    def __init__(self, ctrl=None):
        super(KontaktEinzelGui, self).__init__()
        self.setupUi(self)

        self.ctrl = ctrl

        self.uiTypLbl.setVisible(False)
        self.uiTypCombo.setVisible(False)

        self.uiVornameLedit.setVisible(True)
        self.uiVornameLbl.setVisible(True)

        self.uiVertreterCombo.setVisible(False)
        self.uiVertreterLbl.setVisible(False)

        self.uiVertreterAdresse1Lbl.setVisible(False)
        self.uiVertreterAdresse2Lbl.setVisible(False)
        self.uiVertreterTelefonLbl.setVisible(False)
        self.uiVertreterMailLbl.setVisible(False)

        self.uiNachnameLbl.setText('Nachname')


class KontaktGemGui(QMainWindow, kontakt_UI.Ui_KontaktGui):

    def __init__(self, ctrl=None):
        super(KontaktGemGui, self).__init__()
        self.setupUi(self)

        self.ctrl = ctrl