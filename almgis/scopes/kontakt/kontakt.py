from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from qgis.PyQt.QtCore import QRegExp, Qt
from qgis.PyQt.QtGui import QRegExpValidator, QStandardItemModel
from qgis.PyQt.QtWidgets import QWidget, QPushButton, QVBoxLayout
from sqlalchemy import select, func

from almgis.core.entity import AlmEntity
from almgis.database.models import DmKontaktEinzel, DmKontakt
from almgis.gui.kontakt.kontakt_gui import KontaktEinzelGui, KontaktGemGui


class Kontakt(AlmEntity):
    """
    klasse für einen gemeinschafts-kontakt
    """
    # commitDataSgn = pyqtSignal()

    # updateVornameSignal = pyqtSignal(str)
    setTypSgn = pyqtSignal(object)
    setNachnameSgn = pyqtSignal(str)
    setVornameSgn = pyqtSignal(str)
    setStrasseSgn = pyqtSignal(str)
    setPlzSgn = pyqtSignal(str)
    setOrtSgn = pyqtSignal(str)
    setTelefon1Sgn = pyqtSignal(str)
    setTelefon2Sgn = pyqtSignal(str)
    setTelefon3Sgn = pyqtSignal(str)
    setMail1Sgn = pyqtSignal(str)
    setMail2Sgn = pyqtSignal(str)
    setMail3Sgn = pyqtSignal(str)
    setVertreterSgn = pyqtSignal(int)
    setAnmSgn = pyqtSignal(str)

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

    def __init__(self, parent=None, session=None, entity_dlg=None):
        super(__class__, self).__init__(parent, session, entity_dlg)

        self.ui = KontaktGemGui(self)

        self._entity_dmc = DmKontakt

        # self.commitDataSgn.connect(self.commitData)

        # self.ui.getNachnameSgn.connect()

    # def commitNachname(self, value):
    #
    #     self._entity_dmi.nachname = value
    #     print(f'new entity dmi: {self._entity_dmi}')
    #
    # # def commitNachname(self, value):
    # #
    # #     self._entity_dmi.nachname = value
    #
    # def commitData(self):
    #
    #     print(f'commit entity data!')
    #     self.ui.commitDataSgn.emit()

    def setupEntity(self):
        """
        method to setup the kontakt entity
        """

        """connect the ui update-signals to update the entity when
        data in the gui changes"""
        self.ui.updateDmiTypeSgn.connect(self.updateDmiType)
        self.ui.updateDmiNachnameSgn.connect(self.updateDmiNachname)
        self.ui.updateDmiVornameSgn.connect(self.updateDmiVorname)
        self.ui.updateDmiStrasseSgn.connect(self.updateDmiStrasse)
        self.ui.updateDmiPlzSgn.connect(self.updateDmiPlz)
        self.ui.updateDmiOrtSgn.connect(self.updateDmiOrt)

        self.ui.updateDmiTelefon1Sgn.connect(self.updateDmiTelefon1)
        self.ui.updateDmiTelefon2Sgn.connect(self.updateDmiTelefon2)
        self.ui.updateDmiTelefon3Sgn.connect(self.updateDmiTelefon3)
        self.ui.updateDmiMail1Sgn.connect(self.updateDmiMail1)
        self.ui.updateDmiMail2Sgn.connect(self.updateDmiMail2)
        self.ui.updateDmiMail3Sgn.connect(self.updateDmiMail3)

        # self.ui.updateDmiVertreterSgn.connect(self.updateDmiVertreter)

        self.ui.updateDmiAnmSgn.connect(self.updateDmiAnm)
        """"""

    def updateDmiType(self, value):
        self._entity_dmi.rel_gem_type = value

    def updateDmiNachname(self, value):
        self._entity_dmi.nachname = value

    def updateDmiVorname(self, value):
        self._entity_dmi.vorname = value

    def updateDmiStrasse(self, value):
        self._entity_dmi.strasse = value

    def updateDmiPlz(self, value):
        self._entity_dmi.plz = value

    def updateDmiOrt(self, value):
        self._entity_dmi.ort = value

    def updateDmiTelefon1(self, value):
        self._entity_dmi.telefon1 = value

    def updateDmiTelefon2(self, value):
        self._entity_dmi.telefon2 = value

    def updateDmiTelefon3(self, value):
        self._entity_dmi.telefon3 = value

    def updateDmiMail1(self, value):
        self._entity_dmi.mail1 = value

    def updateDmiMail2(self, value):
        self._entity_dmi.mail2 = value

    def updateDmiMail3(self, value):
        self._entity_dmi.mail3 = value

    def updateDmiAnm(self, value):
        self._entity_dmi.anm = value

    def emitSignals(self):
        super().emitSignals()

        self.setTypSgn.emit(self._entity_dmi.rel_gem_type)
        self.setNachnameSgn.emit(self._entity_dmi.nachname)
        self.setVornameSgn.emit(self._entity_dmi.vorname)
        self.setStrasseSgn.emit(self._entity_dmi.strasse)
        self.setPlzSgn.emit(self._entity_dmi.plz)
        self.setOrtSgn.emit(self._entity_dmi.ort)

        self.setTelefon1Sgn.emit(self._entity_dmi.telefon1)
        self.setTelefon2Sgn.emit(self._entity_dmi.telefon2)
        self.setTelefon3Sgn.emit(self._entity_dmi.telefon3)
        self.setMail1Sgn.emit(self._entity_dmi.mail1)
        self.setMail2Sgn.emit(self._entity_dmi.mail2)
        self.setMail3Sgn.emit(self._entity_dmi.mail3)

        # self.setVertreterSgn.emit(self._entity_dmi.strasse)

        self.setAnmSgn.emit(self._entity_dmi.anm)


    # def setDefaultValues(self, **kwargs):
    #     super().setDefaultValues()
    #
    #     self.uiVertreterCombo.setCurrentIndex(
    #         self.uiVertreterCombo.fallback_index)

    # def initItemUi(self):
    #     super().initItemUi()
    #
    #     # reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
    #     # reg_ex = QRegExp("[A-Z][a-z]{0,50}")
    #     reg_ex = QRegExp("[a-zA-Z0-9äöüÄÖÜß ]{0,10}")
    #     input_validator = QRegExpValidator(reg_ex, self.uiNachnameLedit)
    #     self.uiNachnameLedit.setValidator(input_validator)

    # def setupCodeUi(self):
    #     super().setupCodeUi()
    #
    #     self.uiVornameLedit.setVisible(False)
    #     self.uiVornameLbl.setVisible(False)

    # def loadBackgroundData(self):
    #     super().loadBackgroundData()
    #
    #     self.setGeminschaftsTypeCombo()
    #
    #     self.uiVertreterCombo.loadComboData(self.session, gruppe='e')
    #     self.uiVertreterCombo.combo_wdg_cls = KontaktEinzel
    #     self.uiVertreterCombo.initCombo()

    # def finalEntitySettings(self):
    #     super().finalEntitySettings()
    #
    #     self.setMinimumWidth(650)

    def setGeminschaftsTypeCombo(self):

        stmt = select(DmKontaktGemTyp).order_by(DmKontaktGemTyp.sort)
        gem_type_dmi = self.session.scalars(stmt).all()


        """erstelle ein model mit 1 spalten für das type-combo"""
        type_model = QStandardItemModel(len(gem_type_dmi), 1)
        for i in range(len(gem_type_dmi)):
            type_model.setData(type_model.index(i, 0),
                                          gem_type_dmi[i].name, Qt.DisplayRole)
            type_model.setData(type_model.index(i, 0),
                                          gem_type_dmi[i].id, Qt.UserRole + 1)
            type_model.setData(type_model.index(i, 0),
                                          gem_type_dmi[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiTypCombo.setModel(type_model)
        """"""

    # def setVertrKontaktCombo(self):
    #
    #     vertreter_stmt = select(
    #         BKontakt).where(
    #         BKontakt.type_id == 0).order_by(
    #         func.lower(BKontakt.name))
    #     vertreter_dmi_list = self.entity_session.scalars(vertreter_stmt).all()
    #
    #     """erstelle ein model mit 1 spalten für das type-combo"""
    #     vertreter_model = QStandardItemModel(len(vertreter_dmi_list), 1)
    #     for i in range(len(vertreter_dmi_list)):
    #         vertreter_model.setData(vertreter_model.index(i, 0),
    #                                       vertreter_dmi_list[i].name, Qt.DisplayRole)
    #         vertreter_model.setData(vertreter_model.index(i, 0),
    #                                       vertreter_dmi_list[i].id, Qt.UserRole + 1)
    #         vertreter_model.setData(vertreter_model.index(i, 0),
    #                                       vertreter_dmi_list[i], Qt.UserRole + 2)
    #     """"""
    #
    #     """weise dem combo das model zu"""
    #     self.uiVertreterCombo.setModel(vertreter_model)
    #     """"""

    # def mapEntityData(self, model=None):
    #
    #     if self._entity_dmi.gem_type_id != 0:  # keine Einzelperson
    #         self.gem_type_id = self._entity_dmi.gem_type_id
    #
    #     self.nachname = self._entity_dmi.nachname
    #     self.vorname = self._entity_dmi.vorname
    #     self.strasse = self._entity_dmi.strasse
    #     self.plz = self._entity_dmi.plz
    #     self.ort = self._entity_dmi.ort
    #
    #     self.telefon1 = self._entity_dmi.telefon1
    #     self.telefon2 = self._entity_dmi.telefon2
    #     self.telefon3 = self._entity_dmi.telefon3
    #     self.mail1 = self._entity_dmi.mail1
    #     self.mail2 = self._entity_dmi.mail2
    #     self.mail3 = self._entity_dmi.mail3
    #
    #     self.anm = self._entity_dmi.anm
    #
    #     self.vertreter_id = self._entity_dmi.vertreter_id
    #     self.displayVertreterAdresse()

    def displayVertreterAdresse(self):

        # vertreter = self.uiVertreterCombo.currentData(ComboModel.DmiRole)
        vertreter = self.uiVertreterCombo.currentData(Qt.UserRole + 2)

        if vertreter is None:

            self.uiVertreterAdresse1Lbl.setText('')
            self.uiVertreterAdresse2Lbl.setText('')
            self.uiVertreterTelefonLbl.setText('')
            self.uiVertreterMailLbl.setText('')

        else:

            self.uiVertreterAdresse1Lbl.setText(vertreter.strasse)
            if vertreter.plz is not None:
                self.uiVertreterAdresse2Lbl.setText(vertreter.plz + ' ' + vertreter.ort)
            self.uiVertreterTelefonLbl.setText(vertreter.telefon_all)
            self.uiVertreterMailLbl.setText(vertreter.mail_all)


    def checkValidity(self):
        super().checkValidity()

        if self.uiNachnameLedit.text() == '' and \
                self.uiVornameLedit.text() == '':

            text = "Es muss zumindest für eines der Felder<br>" \
                   "<br>'     Nachname' oder " \
                   "<br>'     Vorname' " \
                   "<br><br>eine Angabe gemacht werden!"

            self.showInvalidityMsg(text)
            self.valid = False

        if self.uiMail1Ledit.text() != '':
            mail_rex = QRegExp("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b")
            mail_rex.setCaseSensitivity(Qt.CaseInsensitive)
            mail_rex.setPatternSyntax(QRegExp.RegExp)

            if mail_rex.exactMatch(self.uiMail1Ledit.text()) == False:

                text = "e-Mail ist nicht korrekt!"

                self.showInvalidityMsg(text)
                self.uiMail1Ledit.setFocus()
                self.valid = False

        if self.uiMail2Ledit.text() != '':
            mail_rex = QRegExp("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b")
            mail_rex.setCaseSensitivity(Qt.CaseInsensitive)
            mail_rex.setPatternSyntax(QRegExp.RegExp)

            if mail_rex.exactMatch(self.uiMail2Ledit.text()) == False:

                text = "e-Mail ist nicht korrekt!"

                self.showInvalidityMsg(text)
                self.uiMail2Ledit.setFocus()
                self.valid = False

        if self.uiMail3Ledit.text() != '':
            mail_rex = QRegExp("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b")
            mail_rex.setCaseSensitivity(Qt.CaseInsensitive)
            mail_rex.setPatternSyntax(QRegExp.RegExp)

            if mail_rex.exactMatch(self.uiMail3Ledit.text()) == False:

                text = "e-Mail ist nicht korrekt!"

                self.showInvalidityMsg(text)
                self.uiMail3Ledit.setFocus()
                self.valid = False

    def getEntityDmi(self, session, entity_id):

        dmi = session.scalars(
            select(DmKontakt)
            .where(DmKontakt.id == entity_id)
        ).unique().first()

        return dmi

    # def submitEntity(self):
    #     """
    #     set the shown_name befor submitting
    #     :return:
    #     """
    #     self._entity_dmi.gem_type_id = self.gem_type_id
    #     self._entity_dmi.rel_gem_type = self.gem_type_dmi
    #     self._entity_dmi.nachname = self.nachname
    #     self._entity_dmi.vorname = self.vorname
    #     self._entity_dmi.strasse = self.strasse
    #
    #     self._entity_dmi.plz = self.plz
    #
    #     self._entity_dmi.ort = self.ort
    #     self._entity_dmi.telefon1 = self.telefon1
    #     self._entity_dmi.telefon2 = self.telefon2
    #     self._entity_dmi.telefon3 = self.telefon3
    #     self._entity_dmi.mail1 = self.mail1
    #     self._entity_dmi.mail2 = self.mail2
    #     self._entity_dmi.mail3 = self.mail3
    #
    #     self._entity_dmi.anm = self.anm
    #
    #     self._entity_dmi.vertreter_id = self.vertreter_id
    #     self._entity_dmi.rel_vertreter = self.vertreter_dmi

    def signals(self):
        super().signals()

        self.uiVertreterCombo.currentIndexChanged.connect(self.displayVertreterAdresse)


class KontaktEinzel(Kontakt):
    """
    klasse für die Kontaktdaten einer Einzelperson
    """

    def __init__(self, parent=None, session=None, entity_dlg=None):
        super(__class__, self).__init__(parent, session, entity_dlg)
        # self.setupCodeUi()

        self.entity_dlg = entity_dlg

        self.ui = KontaktEinzelGui(self)

        self._entity_dmc = DmKontaktEinzel

    # def setupCodeUi(self):
    #     super().setupCodeUi()
    #
    #     self.uiTypLbl.setVisible(False)
    #     self.uiTypCombo.setVisible(False)
    #
    #     self.uiVornameLedit.setVisible(True)
    #     self.uiVornameLbl.setVisible(True)
    #
    #     self.uiVertreterCombo.setVisible(False)
    #     self.uiVertreterLbl.setVisible(False)
    #
    #     self.uiVertreterAdresse1Lbl.setVisible(False)
    #     self.uiVertreterAdresse2Lbl.setVisible(False)
    #     self.uiVertreterTelefonLbl.setVisible(False)
    #     self.uiVertreterMailLbl.setVisible(False)
    #
    #     self.uiNachnameLbl.setText('Nachname')

    # def submitEntity(self):
    #
    #     # einzel_typ_dmi = self.session.get(BKontaktGemTyp, 0)
    #     # leerer_kontakt = self.session.get(BKontakt, 0)
    #
    #     # self._entity_dmi.type_id = 0
    #     # self._entity_dmi.rel_type = einzel_typ_dmi
    #
    #     self._entity_dmi.nachname = self.nachname
    #     self._entity_dmi.vorname = self.vorname
    #     self._entity_dmi.strasse = self.strasse
    #
    #     self._entity_dmi.plz = self.plz
    #
    #     self._entity_dmi.ort = self.ort
    #     self._entity_dmi.telefon1 = self.telefon1
    #     self._entity_dmi.telefon2 = self.telefon2
    #     self._entity_dmi.telefon3 = self.telefon3
    #     self._entity_dmi.mail1 = self.mail1
    #     self._entity_dmi.mail2 = self.mail2
    #     self._entity_dmi.mail3 = self.mail3
    #
    #     self._entity_dmi.anm = self.anm
    #
    #     # self._entity_dmi.vertreter_id = 0
    #     # self._entity_dmi.rel_vertreter = leerer_kontakt
    #
    #     self._entity_dmi.gem_type_id = 0


class KontaktNewSelector(QWidget):
    """
    widget zum auswählen, ob ein neuer Einzelkontakt oder Gemeinschaftskontakt
    angelegt werden soll;
    für das Akt-Formular
    """

    def __init__(self, parent=None):
        super(KontaktNewSelector, self).__init__()

        self.parent = parent

        self.main_layout = QVBoxLayout(self)

        self.setLayout(self.main_layout)

        self.uiEinzelPbtn = QPushButton(self)
        self.uiEinzelPbtn.setText('Einzelkontakt')
        self.main_layout.addWidget(self.uiEinzelPbtn)

        self.uiGemeinschaftPbtn = QPushButton(self)
        self.uiGemeinschaftPbtn.setText('Gemeinschaftskontakt')
        self.main_layout.addWidget(self.uiGemeinschaftPbtn)

        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('neuer Kontakt')
        self.setWindowIcon(QIcon(QPixmap(1, 1)))
        # todo: besser wäre hier: sub->setWindowIcon( QIcon("your_transparent_icon") );

        self.uiEinzelPbtn.clicked.connect(lambda: self.addKontakt('einzel'))
        self.uiGemeinschaftPbtn.clicked.connect(lambda: self.addKontakt('gem'))

    # def addKontakt(self, type):
    #
    #     if type == 'einzel':
    #         entity_widget = KontaktEinzel(self)
    #     elif type == 'gem':
    #         entity_widget = Kontakt(self)
    #
    #     entity_widget.initEntityWidget()
    #
    #     dmi = BKontakt()
    #
    #     entity_widget.purpose = 'add'
    #     entity_widget._commit_on_apply = False
    #
    #     self.edit_entity = dmi
    #     self.parent.session.add(dmi)
    #
    #
    #     entity_widget.setEntitySession(self.parent.session)
    #     entity_widget.editEntity(entity_dmi=dmi)
    #
    #     entity_dialog = AlmEntityDialog(parent=self.parent.uiBewirtschafterCombo)
    #
    #     """setze den entity_dialog im entity_widget"""
    #     entity_widget.entity_dialog = entity_dialog
    #     """"""
    #
    #     entity_dialog.insertWidget(entity_widget)
    #     # entity_dialog.resize(self.minimumSizeHint())
    #
    #     akt_status_vor = getDmiState(self.parent._entity_dmi)
    #     print(f'akt_status_vor: {akt_status_vor}')
    #
    #     # entity_dialog.show()
    #     result = entity_dialog.exec()
    #
    #     if result:
    #         self.parent.uiBewirtschafterCombo.combo_view.model().sourceModel().layoutAboutToBeChanged.emit()
    #         self.parent.uiBewirtschafterCombo._dmi_list.append(dmi)
    #         self.parent.uiBewirtschafterCombo.combo_view.model().sourceModel().layoutChanged.emit()
    #
    #     akt_status_nach = getDmiState(self.parent._entity_dmi)
    #     print(f'akt_status_nach: {akt_status_nach}')
    #
    #     print('new kontakt added!')
    #
    #     self.parent.uiBewirtschafterCombo.setCurrentIndex(self.parent.uiBewirtschafterCombo.combo_view.model().sourceModel()._dmi_list.index(dmi))
    #
    #     self.close()
