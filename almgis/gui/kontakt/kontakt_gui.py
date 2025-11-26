from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from qga.gui.entity_gui import QgaEntityGui
from qga.database.session import QgaProjectSessionCm
from sqlalchemy import select

from almgis.database.models import DmKontaktType, DmKontaktGemTyp
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

    updateDmiVertreterSgn = pyqtSignal(str)  # this is the uuid

    updateDmiAnmSgn = pyqtSignal(str)

    # acceptEntitySgn = pyqtSignal()

    # commitDataSgn = pyqtSignal()

    # getTypSgn = pyqtSignal(int)
    # getNachnameSgn = pyqtSignal(str)
    # getVornameSgn = pyqtSignal(str)
    # getStrasseSgn = pyqtSignal(str)
    # getPlzSgn = pyqtSignal(str)
    # getOrtSgn = pyqtSignal(str)
    # getTelefon1Sgn = pyqtSignal(str)
    # getTelefon2Sgn = pyqtSignal(str)
    # getTelefon3Sgn = pyqtSignal(str)
    # getMail1Sgn = pyqtSignal(str)
    # getMail2Sgn = pyqtSignal(str)
    # getMail3Sgn = pyqtSignal(str)
    # getVertreterSgn = pyqtSignal(int)
    # getAnmSgn = pyqtSignal(str)

    def __init__(self, ctrl=None):
        # super(KontaktGui, self).__init__()
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

        # self.ctrl.setVertreterSgn.connect(self.setStrasse)

        self.ctrl.setAnmSgn.connect(self.setAnm)
        """"""

        self.setMinimumWidth(650)

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
        # self.updateDmiVertreterSgn.emit(self.uiStrasseLedit.text())
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

    def setNachname(self, value):
        self.uiNachnameLedit.setText(value)

    def getNachname(self):
        return self.uiNachnameLedit.text()

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

    # _gem_type_id = 0
    # _nachname = ''
    # _vorname = ''
    # _strasse = ''
    # _plz = ''
    # _ort = ''
    # _telefon1 = ''
    # _telefon2 = ''
    # _telefon3 = ''
    # _mail1 = ''
    # _mail2 = ''
    # _mail3 = ''
    # _anm = ''
    # _vertreter_id = 0
    #
    # @property  # getter
    # def vertreter_id(self):
    #
    #     # type_dmi = self.uiTypCombo.currentData(Qt.UserRole)
    #
    #     # self._type_id = type_dmi.id
    #     self._vertreter_id = self.uiVertreterCombo.currentData(Qt.UserRole + 1)
    #     # self.rel_type = type_dmi
    #     return self._vertreter_id
    #
    # @vertreter_id.setter
    # def vertreter_id(self, value):
    #
    #     # self.uiVertreterCombo.setCurrentIndex(
    #     #     self.uiVertreterCombo.findData(value, Qt.UserRole)
    #     # )
    #     # self._vertreter_id = value
    #
    #
    #     """finde den type_id im model des uiTypeCombo"""
    #     match_index = self.uiVertreterCombo.model().match(
    #         self.uiVertreterCombo.model().index(0, 0),
    #         Qt.UserRole + 1,
    #         value,
    #         -1,
    #         Qt.MatchExactly)
    #     """"""
    #
    #     if match_index:
    #
    #         self.uiVertreterCombo.setCurrentIndex(match_index[0].row())
    #         self._vertreter_id = value
    #     else:
    #         self._vertreter_id = 0
    #
    # @property  # getter
    # def vertreter_dmi(self):
    #
    #     vertreter_dmi = self.uiVertreterCombo.currentData(Qt.UserRole + 2)
    #     # self.rel_type = type_dmi
    #     return vertreter_dmi
    #
    # @property  # getter
    # def gem_type_id(self):
    #
    #     self._gem_type_id = self.uiTypCombo.currentData(Qt.UserRole + 1)
    #     return self._gem_type_id
    #
    # @gem_type_id.setter
    # def gem_type_id(self, value):
    #     """
    #     setter for gem_type_id
    #
    #     :param value:
    #     :return:
    #     """
    #
    #     """finde den type_id im model des uiTypeCombo"""
    #     match_index = self.uiTypCombo.model().match(
    #         self.uiTypCombo.model().index(0, 0),
    #         Qt.UserRole + 1,
    #         value,
    #         -1,
    #         Qt.MatchExactly)
    #     """"""
    #
    #     if match_index:
    #
    #         self.uiTypCombo.setCurrentIndex(match_index[0].row())
    #         self._gem_type_id = value
    #     else:
    #         self._gem_type_id = 0
    #
    # @property  # getter
    # def gem_type_dmi(self):
    #
    #     gem_type_dmi = self.uiTypCombo.currentData(Qt.UserRole)
    #     # self.rel_type = type_dmi
    #     return gem_type_dmi
    #
    # @property  # getter
    # def nachname(self):
    #
    #     if self.uiNachnameLedit.text() == 'asd':
    #         text = "Name darf nicht 'asd' sein!"
    #         self.showInvalidityMsg(text)
    #         self.valid = False
    #
    #     self._nachname = self.uiNachnameLedit.text()
    #     return self._nachname
    #
    # @nachname.setter
    # def nachname(self, value):
    #
    #     self.uiNachnameLedit.setText(value)
    #     self._nachname = value
    #
    # @property  # getter
    # def vorname(self):
    #
    #     self._vorname = self.uiVornameLedit.text()
    #     return self._vorname
    #
    # @vorname.setter
    # def vorname(self, value):
    #
    #     self.uiVornameLedit.setText(value)
    #     self._vorname = value
    #
    # @property  # getter
    # def strasse(self):
    #
    #     self._strasse = self.uiStrasseLedit.text()
    #     return self._strasse
    #
    # @strasse.setter
    # def strasse(self, value):
    #
    #     self.uiStrasseLedit.setText(value)
    #     self._strasse = value
    #
    # @property  # getter
    # def plz(self):
    #
    #     self._plz = self.uiPlzLedit.text()
    #     return self._plz
    #
    # @plz.setter
    # def plz(self, value):
    #
    #     self.uiPlzLedit.setText(value)
    #     self._plz = value
    #
    # @property  # getter
    # def ort(self):
    #
    #     self._ort = self.uiOrtLedit.text()
    #     return self._ort
    #
    # @ort.setter
    # def ort(self, value):
    #
    #     self.uiOrtLedit.setText(value)
    #     self._ort = value
    #
    # @property  # getter
    # def telefon1(self):
    #
    #     self._telefon1 = self.uiTelefon1Ledit.text()
    #     return self._telefon1
    #
    # @telefon1.setter
    # def telefon1(self, value):
    #
    #     self.uiTelefon1Ledit.setText(value)
    #     self._telefon1 = value
    #
    # @property  # getter
    # def telefon2(self):
    #
    #     self._telefon2 = self.uiTelefon2Ledit.text()
    #     return self._telefon2
    #
    # @telefon2.setter
    # def telefon2(self, value):
    #
    #     self.uiTelefon2Ledit.setText(value)
    #     self._telefon2 = value
    #
    # @property  # getter
    # def telefon3(self):
    #
    #     self._telefon3 = self.uiTelefon3Ledit.text()
    #     return self._telefon3
    #
    # @telefon3.setter
    # def telefon3(self, value):
    #
    #     self.uiTelefon3Ledit.setText(value)
    #     self._telefon3 = value
    #
    # @property  # getter
    # def mail1(self):
    #
    #     self._mail1 = self.uiMail1Ledit.text()
    #     return self._mail1
    #
    # @mail1.setter
    # def mail1(self, value):
    #
    #     self.uiMail1Ledit.setText(value)
    #     self._mail1 = value
    #
    # @property  # getter
    # def mail2(self):
    #
    #     self._mail2 = self.uiMail2Ledit.text()
    #     return self._mail2
    #
    # @mail2.setter
    # def mail2(self, value):
    #
    #     self.uiMail2Ledit.setText(value)
    #     self._mail2 = value
    #
    # @property  # getter
    # def mail3(self):
    #
    #     self._mail3 = self.uiMail3Ledit.text()
    #     return self._mail3
    #
    # @mail3.setter
    # def mail3(self, value):
    #
    #     self.uiMail3Ledit.setText(value)
    #     self._mail3 = value
    #
    # @property  # getter
    # def anm(self):
    #
    #     self._anm = self.uiAnmPedit.toPlainText()
    #     return self._anm
    #
    # @anm.setter
    # def anm(self, value):
    #
    #     self.uiAnmPedit.setPlainText(value)
    #     self._anm = value

    def __init__(self, ctrl=None):
        super(KontaktEinzelGui, self).__init__(ctrl)
        # QgaEntityGui.__init__(self, ctrl)
        self.setupUi(self)

        self.ctrl = ctrl

        self.uiTypLbl.setVisible(False)
        self.uiTypCombo.setVisible(False)
        self.uiInfoBtnType.setVisible(False)

        # self.uiVornameLedit.setVisible(True)
        # self.uiVornameLbl.setVisible(True)

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

    # def setVorname(self, value):
    #
    #     self._vorname = value
    #     self.uiVornameLedit.setText(value)


class KontaktGemGui(KontaktGui):

    def __init__(self, ctrl=None):
        super(KontaktGemGui, self).__init__(ctrl)
        self.setupUi(self)

        self.ctrl = ctrl

        self.kontakt_type_dmi = []

        self.uiVornameLbl.setVisible(False)
        self.uiVornameLedit.setVisible(False)
        self.uiInfoBtnVorname.setVisible(False)

        self.setupTypCombo()

        # """catch the signals from the ctrl and set the gui widgets"""
        # self.ctrl.setTypSgn.connect(self.setType)
        # """"""

    def acceptWdg(self):

        self.updateDmiTypeSgn.emit(
            self.uiTypCombo.itemData(self.uiTypCombo.currentIndex()))

        super().acceptWdg()

    def setType(self, value):

        type_id = value.id
        for i in range(self.uiTypCombo.count()):
            combo_type = self.uiTypCombo.itemData(i, role=Qt.UserRole)
            if combo_type is not None and combo_type.id == type_id:
                self.uiTypCombo.setCurrentIndex(i)
                break

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
