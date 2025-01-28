from PyQt5.QtGui import QIcon, QPixmap
from qgis.PyQt.QtCore import QRegExp, Qt
# from PyQt5.QtGui import QRegExpValidator
from qgis.PyQt.QtGui import QRegExpValidator, QStandardItemModel
from qgis.PyQt.QtWidgets import QWidget, QPushButton, QVBoxLayout
from sqlalchemy import select, func

from almgis.entity import AlmEntityDialog
from almgis.scopes.kontakt import kontakt_UI

from almgis.data_model import BKontakt, BKontaktTyp
from qga.tools import getMciState

from almgis.entity import AlmEntity


class Kontakt(kontakt_UI.Ui_Kontakt, AlmEntity):
    """
    klasse für einen gemeinschafts-kontakt
    """
    _type_id = 0
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

        # type_mci = self.uiTypCombo.currentData(Qt.UserRole)

        # self._type_id = type_mci.id
        self._vertreter_id = self.uiVertreterCombo.currentData(Qt.UserRole + 1)
        # self.rel_type = type_mci
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
    def vertreter_mci(self):

        vertreter_mci = self.uiVertreterCombo.currentData(Qt.UserRole + 2)
        # self.rel_type = type_mci
        return vertreter_mci

    @property  # getter
    def type_id(self):

        self._type_id = self.uiTypCombo.currentData(Qt.UserRole + 1)
        return self._type_id

    @type_id.setter
    def type_id(self, value):
        """
        setter for type_id

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
            self._type_id = value
        else:
            self.type_id = 0

    @property  # getter
    def type_mci(self):

        type_mci = self.uiTypCombo.currentData(Qt.UserRole)
        # self.rel_type = type_mci
        return type_mci

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

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        self.setupCodeUi()

        self._entity_mc = BKontakt
        # self.data_class = BKontakt

    def initItemUi(self):
        super().initItemUi()

        # reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        # reg_ex = QRegExp("[A-Z][a-z]{0,50}")
        reg_ex = QRegExp("[a-zA-Z0-9äöüÄÖÜß ]{0,10}")
        input_validator = QRegExpValidator(reg_ex, self.uiNachnameLedit)
        self.uiNachnameLedit.setValidator(input_validator)

    def setupCodeUi(self):
        super().setupCodeUi()

        self.uiVornameLedit.setVisible(False)
        self.uiVornameLbl.setVisible(False)

    def loadBackgroundData(self):
        super().loadBackgroundData()

        self.setTypeCombo()

        self.uiVertreterCombo.loadComboData(self.entity_session, gruppe='e')
        self.uiVertreterCombo.combo_widget_form = KontaktEinzel
        self.uiVertreterCombo.initCombo()

    def finalEntitySettings(self):
        super().finalEntitySettings()

        self.setMinimumWidth(650)

    def setTypeCombo(self):

        stmt = select(BKontaktTyp).where(BKontaktTyp.gemeinschaft == 1
                                         ).order_by(BKontaktTyp.sort)

        type_mci = self.entity_session.scalars(stmt).all()


        """erstelle ein model mit 1 spalten für das type-combo"""
        type_model = QStandardItemModel(len(type_mci), 1)
        for i in range(len(type_mci)):
            if type_mci[i].gemeinschaft == 1:
                type_model.setData(type_model.index(i, 0),
                                              type_mci[i].name, Qt.DisplayRole)
                type_model.setData(type_model.index(i, 0),
                                              type_mci[i].id, Qt.UserRole + 1)
                type_model.setData(type_model.index(i, 0),
                                              type_mci[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiTypCombo.setModel(type_model)
        """"""

    def setVertrKontaktCombo(self):

        vertreter_stmt = select(
            BKontakt).where(
            BKontakt.type_id == 0).order_by(
            func.lower(BKontakt.name))
        vertreter_mci_list = self.entity_session.scalars(vertreter_stmt).all()

        """erstelle ein model mit 1 spalten für das type-combo"""
        vertreter_model = QStandardItemModel(len(vertreter_mci_list), 1)
        for i in range(len(vertreter_mci_list)):
            vertreter_model.setData(vertreter_model.index(i, 0),
                                          vertreter_mci_list[i].name, Qt.DisplayRole)
            vertreter_model.setData(vertreter_model.index(i, 0),
                                          vertreter_mci_list[i].id, Qt.UserRole + 1)
            vertreter_model.setData(vertreter_model.index(i, 0),
                                          vertreter_mci_list[i], Qt.UserRole + 2)
        """"""

        """weise dem combo das model zu"""
        self.uiVertreterCombo.setModel(vertreter_model)
        """"""

    def mapEntityData(self, model=None):

        if self._entity_mci.type_id != 0:  # keine Einzelperson
            self.type_id = self._entity_mci.type_id

        self.nachname = self._entity_mci.nachname
        self.vorname = self._entity_mci.vorname
        self.strasse = self._entity_mci.strasse
        self.plz = self._entity_mci.plz
        self.ort = self._entity_mci.ort

        self.telefon1 = self._entity_mci.telefon1
        self.telefon2 = self._entity_mci.telefon2
        self.telefon3 = self._entity_mci.telefon3
        self.mail1 = self._entity_mci.mail1
        self.mail2 = self._entity_mci.mail2
        self.mail3 = self._entity_mci.mail3

        self.anm = self._entity_mci.anm

        self.vertreter_id = self._entity_mci.vertreter_id
        self.displayVertreterAdresse()

    def displayVertreterAdresse(self):

        # vertreter = self.uiVertreterCombo.currentData(ComboModel.MciRole)
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

    def getEntityMci(self, session, entity_id):

        mci = session.scalars(
            select(BKontakt)
            .where(BKontakt.id == entity_id)
        ).unique().first()

        return mci

    def submitEntity(self):
        """
        set the shown_name befor submitting
        :return:
        """
        self._entity_mci.type_id = self.type_id
        self._entity_mci.rel_type = self.type_mci
        self._entity_mci.nachname = self.nachname
        self._entity_mci.vorname = self.vorname
        self._entity_mci.strasse = self.strasse

        self._entity_mci.plz = self.plz

        self._entity_mci.ort = self.ort
        self._entity_mci.telefon1 = self.telefon1
        self._entity_mci.telefon2 = self.telefon2
        self._entity_mci.telefon3 = self.telefon3
        self._entity_mci.mail1 = self.mail1
        self._entity_mci.mail2 = self.mail2
        self._entity_mci.mail3 = self.mail3

        self._entity_mci.anm = self.anm

        self._entity_mci.vertreter_id = self.vertreter_id
        self._entity_mci.rel_vertreter = self.vertreter_mci

    def signals(self):
        super().signals()

        self.uiVertreterCombo.currentIndexChanged.connect(self.displayVertreterAdresse)


class KontaktEinzel(Kontakt):
    """
    klasse für die Kontaktdaten einer Einzelperson
    """

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupCodeUi()

    def setupCodeUi(self):
        super().setupCodeUi()

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

    def submitEntity(self):

        einzel_typ_mci = self.entity_session.get(BKontaktTyp, 0)
        leerer_kontakt = self.entity_session.get(BKontakt, 0)

        self._entity_mci.type_id = 0
        self._entity_mci.rel_type = einzel_typ_mci

        self._entity_mci.nachname = self.nachname
        self._entity_mci.vorname = self.vorname
        self._entity_mci.strasse = self.strasse

        self._entity_mci.plz = self.plz

        self._entity_mci.ort = self.ort
        self._entity_mci.telefon1 = self.telefon1
        self._entity_mci.telefon2 = self.telefon2
        self._entity_mci.telefon3 = self.telefon3
        self._entity_mci.mail1 = self.mail1
        self._entity_mci.mail2 = self.mail2
        self._entity_mci.mail3 = self.mail3

        self._entity_mci.anm = self.anm

        self._entity_mci.vertreter_id = 0
        self._entity_mci.rel_vertreter = leerer_kontakt


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

    def addKontakt(self, type):

        if type == 'einzel':
            entity_widget = KontaktEinzel(self)
        elif type == 'gem':
            entity_widget = Kontakt(self)

        entity_widget.initEntityWidget()

        mci = BKontakt()

        entity_widget.purpose = 'add'
        entity_widget._commit_on_apply = False

        self.edit_entity = mci
        self.parent.entity_session.add(mci)


        entity_widget.setEntitySession(self.parent.entity_session)
        entity_widget.editEntity(entity_mci=mci)

        entity_dialog = AlmEntityDialog(parent=self.parent.uiBewirtschafterCombo)

        """setze den entity_dialog im entity_widget"""
        entity_widget.entity_dialog = entity_dialog
        """"""

        entity_dialog.insertWidget(entity_widget)
        # entity_dialog.resize(self.minimumSizeHint())

        akt_status_vor = getMciState(self.parent._entity_mci)
        print(f'akt_status_vor: {akt_status_vor}')

        # entity_dialog.show()
        result = entity_dialog.exec()

        if result:
            self.parent.uiBewirtschafterCombo.combo_view.model().sourceModel().layoutAboutToBeChanged.emit()
            self.parent.uiBewirtschafterCombo._mci_list.append(mci)
            self.parent.uiBewirtschafterCombo.combo_view.model().sourceModel().layoutChanged.emit()

        akt_status_nach = getMciState(self.parent._entity_mci)
        print(f'akt_status_nach: {akt_status_nach}')

        print('new kontakt added!')

        self.parent.uiBewirtschafterCombo.setCurrentIndex(self.parent.uiBewirtschafterCombo.combo_view.model().sourceModel()._mci_list.index(mci))

        self.close()
