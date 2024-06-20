from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core import entity, db_session_cm
from core.scopes.kontakt import kontakt_UI

from core.data_model import BKontakt, BKontaktTyp


class Kontakt(kontakt_UI.Ui_Kontakt, entity.Entity):
    """
    class for a contact-item
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

    @property  # getter
    def type_id(self):

        # type_mci = self.uiTypCombo.currentData(Qt.UserRole)

        # self._type_id = type_mci.id
        self._type_id = self.uiTypCombo.currentData(Qt.UserRole)
        # self.rel_type = type_mci
        return self._type_id

    @type_id.setter
    def type_id(self, value):

        self.uiTypCombo.setCurrentIndex(
            self.uiTypCombo.findData(value, Qt.UserRole)
        )
        self._type_id = value

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

    # @property  # getter
    # def shown_name(self):
    #
    #     name = ''
    #
    #     name = name + self.uiLastNameLedit.text()
    #     if self.uiLastNameLedit.text() != ''\
    #             and self.uiFirstNameLedit.text() != '':
    #         name = name + ' '
    #     name = name + self.uiFirstNameLedit.text()
    #
    #     if self.uiCompanyLedit.text() != '' and name == '':
    #         self._shown_name = self.uiCompanyLedit.text()
    #
    #     if self.uiCompanyLedit.text() != '' and name != '':
    #         self._shown_name = self.uiCompanyLedit.text() + ' (' + name + ')'
    #
    #     if self.uiCompanyLedit.text() == '' and name != '':
    #         self._shown_name = name
    #
    #     return self._shown_name
    #
    # @shown_name.setter
    # def shown_name(self, value):
    #
    #     self._shown_name = value

    @property  # getter
    def plz(self):

        if self.uiPlzLedit.text() is None or self.uiPlzLedit.text() == 'None':
            self._plz = 0
        else:
            self._plz = int(self.uiPlzLedit.text())
        return self._plz

    @plz.setter
    def plz(self, value):

        self.uiPlzLedit.setText(str(value))
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

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        self._entity_mc = BKontakt
        # self.data_class = BKontakt

    def initItemUi(self):
        super().initItemUi()

        # reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        # reg_ex = QRegExp("[A-Z][a-z]{0,50}")
        reg_ex = QRegExp("[a-zA-Z0-9äöüÄÖÜß ]{0,10}")
        input_validator = QRegExpValidator(reg_ex, self.uiNachnameLedit)
        self.uiNachnameLedit.setValidator(input_validator)

    def initEntityWidget(self):
        super().initEntityWidget()

        print(f'init entity widget')

        self.setTypeCombo()

    def setTypeCombo(self):

        type_items = sorted(self._custom_entity_data['typ'],
                              key=lambda x:x.sort)

        # with db_session_cm() as session:
        #
        #     stmt = select(BKontaktTyp).order_by(BKontaktTyp.sort)
        #
        #     type_mci = session.scalars(stmt).all()

        for type in type_items:
            self.uiTypCombo.addItem(type.name, type.id)

    def mapData(self, model=None):

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

    def getEntityMci(self, session, entity_id):

        mci = session.scalars(
            select(BKontakt)
            .where(BKontakt.id == entity_id)
        ).unique().first()

        # mci = session.scalars(
        #     select(BKontakt)
        #     .options(joinedload(BKontakt.rel_type))
        #     .where(BKontakt.id == entity_id)
        # ).unique().first()

        return mci

    def submitEntity(self):
        """
        set the shown_name befor submitting
        :return:
        """
        self._entity_mci.type_id = self.type_id
        # self._entity_mci.type_id = self.typ
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

        # super().submitEntity()
