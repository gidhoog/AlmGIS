from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from almgis.resources.ui_py.kontakt import kontakt_UI


class KontaktEinzelGui(QMainWindow, kontakt_UI.Ui_KontaktGui):

    acceptEntitySignal = pyqtSignal(object)

    _gem_type_id = 0
    _nachname = ''
    _vorname = ''
    _strasse = ''
    _plz = ''
    _ort = ''
    _telefon1 = ''
    _telefon2 = ''
    _telefon3 = ''
    _mail1 = ''
    _mail2 = ''
    _mail3 = ''
    _anm = ''
    _vertreter_id = 0

    @property  # getter
    def vertreter_id(self):

        # type_dmi = self.uiTypCombo.currentData(Qt.UserRole)

        # self._type_id = type_dmi.id
        self._vertreter_id = self.uiVertreterCombo.currentData(Qt.UserRole + 1)
        # self.rel_type = type_dmi
        return self._vertreter_id

    @vertreter_id.setter
    def vertreter_id(self, value):

        # self.uiVertreterCombo.setCurrentIndex(
        #     self.uiVertreterCombo.findData(value, Qt.UserRole)
        # )
        # self._vertreter_id = value


        """finde den type_id im model des uiTypeCombo"""
        match_index = self.uiVertreterCombo.model().match(
            self.uiVertreterCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiVertreterCombo.setCurrentIndex(match_index[0].row())
            self._vertreter_id = value
        else:
            self._vertreter_id = 0

    @property  # getter
    def vertreter_dmi(self):

        vertreter_dmi = self.uiVertreterCombo.currentData(Qt.UserRole + 2)
        # self.rel_type = type_dmi
        return vertreter_dmi

    @property  # getter
    def gem_type_id(self):

        self._gem_type_id = self.uiTypCombo.currentData(Qt.UserRole + 1)
        return self._gem_type_id

    @gem_type_id.setter
    def gem_type_id(self, value):
        """
        setter for gem_type_id

        :param value:
        :return:
        """

        """finde den type_id im model des uiTypeCombo"""
        match_index = self.uiTypCombo.model().match(
            self.uiTypCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiTypCombo.setCurrentIndex(match_index[0].row())
            self._gem_type_id = value
        else:
            self._gem_type_id = 0

    @property  # getter
    def gem_type_dmi(self):

        gem_type_dmi = self.uiTypCombo.currentData(Qt.UserRole)
        # self.rel_type = type_dmi
        return gem_type_dmi

    @property  # getter
    def nachname(self):

        if self.uiNachnameLedit.text() == 'asd':
            text = "Name darf nicht 'asd' sein!"
            self.showInvalidityMsg(text)
            self.valid = False

        self._nachname = self.uiNachnameLedit.text()
        return self._nachname

    @nachname.setter
    def nachname(self, value):

        self.uiNachnameLedit.setText(value)
        self._nachname = value

    @property  # getter
    def vorname(self):

        self._vorname = self.uiVornameLedit.text()
        return self._vorname

    @vorname.setter
    def vorname(self, value):

        self.uiVornameLedit.setText(value)
        self._vorname = value

    @property  # getter
    def strasse(self):

        self._strasse = self.uiStrasseLedit.text()
        return self._strasse

    @strasse.setter
    def strasse(self, value):

        self.uiStrasseLedit.setText(value)
        self._strasse = value

    @property  # getter
    def plz(self):

        self._plz = self.uiPlzLedit.text()
        return self._plz

    @plz.setter
    def plz(self, value):

        self.uiPlzLedit.setText(value)
        self._plz = value

    @property  # getter
    def ort(self):

        self._ort = self.uiOrtLedit.text()
        return self._ort

    @ort.setter
    def ort(self, value):

        self.uiOrtLedit.setText(value)
        self._ort = value

    @property  # getter
    def telefon1(self):

        self._telefon1 = self.uiTelefon1Ledit.text()
        return self._telefon1

    @telefon1.setter
    def telefon1(self, value):

        self.uiTelefon1Ledit.setText(value)
        self._telefon1 = value

    @property  # getter
    def telefon2(self):

        self._telefon2 = self.uiTelefon2Ledit.text()
        return self._telefon2

    @telefon2.setter
    def telefon2(self, value):

        self.uiTelefon2Ledit.setText(value)
        self._telefon2 = value

    @property  # getter
    def telefon3(self):

        self._telefon3 = self.uiTelefon3Ledit.text()
        return self._telefon3

    @telefon3.setter
    def telefon3(self, value):

        self.uiTelefon3Ledit.setText(value)
        self._telefon3 = value

    @property  # getter
    def mail1(self):

        self._mail1 = self.uiMail1Ledit.text()
        return self._mail1

    @mail1.setter
    def mail1(self, value):

        self.uiMail1Ledit.setText(value)
        self._mail1 = value

    @property  # getter
    def mail2(self):

        self._mail2 = self.uiMail2Ledit.text()
        return self._mail2

    @mail2.setter
    def mail2(self, value):

        self.uiMail2Ledit.setText(value)
        self._mail2 = value

    @property  # getter
    def mail3(self):

        self._mail3 = self.uiMail3Ledit.text()
        return self._mail3

    @mail3.setter
    def mail3(self, value):

        self.uiMail3Ledit.setText(value)
        self._mail3 = value

    @property  # getter
    def anm(self):

        self._anm = self.uiAnmPedit.toPlainText()
        return self._anm

    @anm.setter
    def anm(self, value):

        self.uiAnmPedit.setPlainText(value)
        self._anm = value

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

        # self.ctrl.updateVornameSignal.connect(self.uiVornameLedit.setText)
        self.ctrl.updateVornameSignal.connect(self.setVorname)

        self.ctrl.entity_dialog.accepted.emit(self.acceptEntitySignal)

    def setVorname(self, value):

        self._vorname = value
        self.uiVornameLedit.setText(value)


class KontaktGemGui(QMainWindow, kontakt_UI.Ui_KontaktGui):

    def __init__(self, ctrl=None):
        super(KontaktGemGui, self).__init__()
        self.setupUi(self)

        self.ctrl = ctrl