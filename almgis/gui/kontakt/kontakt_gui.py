from PyQt5.QtCore import Qt, pyqtSignal
from qga.gui.entity_gui import QgaEntityGui
from sqlalchemy import select, and_, or_

from almgis.database.models import DmKontaktGemTyp, DmKontakt
from almgis.resources.ui_py.kontakt import kontakt_UI


class KontaktGui(QgaEntityGui, kontakt_UI.Ui_KontaktGui):

    updateDmiTypeSgn = pyqtSignal(object)

    updateDmiNachnameSgn = pyqtSignal(str)
    updateDmiVornameSgn = pyqtSignal(str)
    updateDmiStrasseSgn = pyqtSignal(str)
    updateDmiPlzSgn = pyqtSignal(str)
    updateDmiOrtSgn = pyqtSignal(str)

    updateDmiTelefon1Sgn = pyqtSignal(str)
    updateDmiTelefon2Sgn = pyqtSignal(str)
    updateDmiTelefon3Sgn = pyqtSignal(str)
    updateDmiMail1Sgn = pyqtSignal(str)
    updateDmiMail2Sgn = pyqtSignal(str)
    updateDmiMail3Sgn = pyqtSignal(str)

    updateDmiVertreterSgn = pyqtSignal(object)

    updateDmiAnmSgn = pyqtSignal(str)

    def __init__(self, ctrl=None):
        QgaEntityGui.__init__(self, ctrl)
        self.setupUi(self)

        self.info_wdg = 'KontaktGui'

        """catch the signals from the ctrl and set the gui widgets"""
        self.ctrl.setTypSgn.connect(self.setType)

        self.ctrl.setNachnameSgn.connect(self.setNachname)
        self.ctrl.setVornameSgn.connect(self.setVorname)
        self.ctrl.setStrasseSgn.connect(self.setStrasse)
        self.ctrl.setPlzSgn.connect(self.setPlz)
        self.ctrl.setOrtSgn.connect(self.setOrt)

        self.ctrl.setTelefon1Sgn.connect(self.setTelefon1)
        self.ctrl.setTelefon2Sgn.connect(self.setTelefon2)
        self.ctrl.setTelefon3Sgn.connect(self.setTelefon3)
        self.ctrl.setMail1Sgn.connect(self.setMail1)
        self.ctrl.setMail2Sgn.connect(self.setMail2)
        self.ctrl.setMail3Sgn.connect(self.setMail3)

        self.ctrl.setVertreterSgn.connect(self.setVertreter)

        self.ctrl.setAnmSgn.connect(self.setAnm)
        """"""

        self.setMinimumWidth(650)

    def setFirstFocus(self):

        self.uiNachnameLedit.setFocus()

    def acceptWdg(self):

        print(f'accept entity gui!!')

        self.updateDmiTypeSgn.emit(
            self.uiTypCombo.itemData(self.uiTypCombo.currentIndex()))

        self.updateDmiNachnameSgn.emit(self.uiNachnameLedit.text())
        self.updateDmiVornameSgn.emit(self.uiVornameLedit.text())
        self.updateDmiStrasseSgn.emit(self.uiStrasseLedit.text())
        self.updateDmiPlzSgn.emit(self.uiPlzLedit.text())
        self.updateDmiOrtSgn.emit(self.uiOrtLedit.text())

        self.updateDmiTelefon1Sgn.emit(self.uiTelefon1Ledit.text())
        self.updateDmiTelefon2Sgn.emit(self.uiTelefon2Ledit.text())
        self.updateDmiTelefon3Sgn.emit(self.uiTelefon3Ledit.text())
        self.updateDmiMail1Sgn.emit(self.uiMail1Ledit.text())
        self.updateDmiMail2Sgn.emit(self.uiMail2Ledit.text())
        self.updateDmiMail3Sgn.emit(self.uiMail3Ledit.text())

        self.updateDmiVertreterSgn.emit(
            self.uiVertreterCombo.itemData(self.uiVertreterCombo.currentIndex()))

        self.updateDmiAnmSgn.emit(self.uiAnmPedit.toPlainText())

        super().acceptWdg()

    def setType(self, value):

        if value:
            type_id = value.id
            for i in range(self.uiTypCombo.count()):
                combo_type = self.uiTypCombo.itemData(i, role=Qt.UserRole)
                if combo_type is not None and combo_type.id == type_id:
                    self.uiTypCombo.setCurrentIndex(i)
                    break

    def setVertreter(self, value):

        if value:
            vertreter_id = value.id
            for i in range(self.uiVertreterCombo.count()):
                combo_vertreter = self.uiVertreterCombo.itemData(i, role=Qt.UserRole)
                if combo_vertreter is not None and combo_vertreter.id == vertreter_id:
                    self.uiVertreterCombo.setCurrentIndex(i)
                    break

    def setNachname(self, value):
        self.uiNachnameLedit.setText(value)

    # def getNachname(self):
    #     return self.uiNachnameLedit.text()

    def setVorname(self, value):
        self.uiVornameLedit.setText(value)

    def setStrasse(self, value):
        self.uiStrasseLedit.setText(value)

    def setPlz(self, value):
        self.uiPlzLedit.setText(value)

    def setOrt(self, value):
        self.uiOrtLedit.setText(value)

    def setTelefon1(self, value):
        self.uiTelefon1Ledit.setText(value)

    def setTelefon2(self, value):
        self.uiTelefon2Ledit.setText(value)

    def setTelefon3(self, value):
        self.uiTelefon3Ledit.setText(value)

    def setMail1(self, value):
        self.uiMail1Ledit.setText(value)

    def setMail2(self, value):
        self.uiMail2Ledit.setText(value)

    def setMail3(self, value):
        self.uiMail3Ledit.setText(value)

    def setAnm(self, value):
        self.uiAnmPedit.setPlainText(value)


class KontaktEinzelGui(KontaktGui):

    def __init__(self, ctrl=None):
        super(KontaktEinzelGui, self).__init__(ctrl)
        # self.setupUi(self)

        self.ctrl = ctrl

        self.uiTypLbl.setVisible(False)
        self.uiTypCombo.setVisible(False)
        self.uiInfoBtnType.setVisible(False)

        self.uiVertreterLbl.setVisible(False)
        self.uiVertreterCombo.setVisible(False)
        self.uiInfoBtnVertreter.setVisible(False)

        self.uiVertreterAdresse1Lbl.setVisible(False)
        self.uiVertreterAdresse2Lbl.setVisible(False)
        self.uiVertreterTelefonLbl.setVisible(False)
        self.uiVertreterMailLbl.setVisible(False)
        self.uiInfoBtnVertreterAdr.setVisible(False)

        self.uiVertreterAdresse1Lbl.setVisible(False)
        self.uiVertreterAdresse2Lbl.setVisible(False)
        self.uiVertreterTelefonLbl.setVisible(False)
        self.uiVertreterMailLbl.setVisible(False)

        self.uiNachnameLbl.setText('Nachname')

class KontaktGemGui(KontaktGui):

    def __init__(self, ctrl=None):
        super(KontaktGemGui, self).__init__(ctrl)
        # self.setupUi(self)

        self.ctrl = ctrl

        self.kontakt_type_dmi = []

        self.uiVornameLbl.setVisible(False)
        self.uiVornameLedit.setVisible(False)
        self.uiInfoBtnVorname.setVisible(False)

        self.setupTypCombo()
        self.setupVertreterCombo()

        # self.uiVertreterCombo.setCurrentIndex(-1)

    def acceptWdg(self):

        self.updateDmiTypeSgn.emit(
            self.uiTypCombo.itemData(self.uiTypCombo.currentIndex()))

        super().acceptWdg()

    def setupTypCombo(self):
        """
        lade kontakt-typen von der Datenbank
        """

        """add items to the combo
        see: https://www.perplexity.ai/search/how-to-add-items-to-a-qcombobo-TvWSAWxPQvKsc1mFZlsFhg"""
        stmt = select(DmKontaktGemTyp).order_by(DmKontaktGemTyp.sort)
        for kontakt in self.ctrl.session.scalars(stmt).all():
            self.uiTypCombo.addItem(kontakt.name, kontakt)
        """"""

    def setupVertreterCombo(self):

        stmt2 = select(DmKontakt).where(
            or_(DmKontakt.type_id == 0, DmKontakt.blank_value == 1)
        ).order_by(DmKontakt.nachname)

        for vertreter in self.ctrl.session.scalars(stmt2).all():
            self.uiVertreterCombo.addItem(vertreter.name, vertreter)


