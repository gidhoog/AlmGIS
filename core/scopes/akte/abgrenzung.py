from core import entity
from core.data_model import BErfassungsart, BAbgrenzungStatus
from core.main_dialog import MainDialog
from core.scopes.akte import abgrenzung_UI
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItemModel

from sqlalchemy import select


class Abgrenzung(abgrenzung_UI.Ui_Abgrenzung,
                 entity.Entity):

    _jahr = 2000
    _bearbeiter = ''
    _anm = ''
    _bez = ''
    _awb = 0

    _erfassungsart_id = 0
    _erfassungsart_mci = None
    _status_id = 0
    _status_mci = None

    _commit_on_apply = False

    @property  # getter
    def jahr(self):

        self._jahr = self.uiJahrSbox.value()
        return self._jahr

    @jahr.setter
    def jahr(self, value):

        self.uiJahrSbox.setValue(value)
        self._jahr = value

    @property  # getter
    def bearbeiter(self):

        self._bearbeiter = self.uiBearbeiterLedit.text()
        return self._bearbeiter

    @bearbeiter.setter
    def bearbeiter(self, value):

        self.uiBearbeiterLedit.setText(value)
        self._bearbeiter = value

    @property  # getter
    def anm(self):

        self._anm = self.uiAnmerkungPtext.toPlainText()
        return self._anm

    @anm.setter
    def anm(self, value):

        self.uiAnmerkungPtext.setPlainText(value)
        self._anm = value

    @property  # getter
    def bez(self):

        self._bez = self.uiBezeichnungLedit.text()
        return self._bez

    @bez.setter
    def bez(self, value):

        self.uiBezeichnungLedit.setText(value)
        self._bez = value

    @property  # getter
    def awb(self):

        if self.uiAwbCkBox.isChecked():
            self._awb = 1
        else:
            self._awb = 0

        return self._awb

    @awb.setter
    def awb(self, value):

        if value == 1:
            self.uiAwbCkBox.setCheckState(Qt.Checked)
        else:
            self.uiAwbCkBox.setCheckState(Qt.Unchecked)

        self._awb = value

    @property  # getter
    def erfassungsart_id(self):

        self._erfassungsart_id = self.uiErfassCombo.currentData(Qt.UserRole + 1)
        return self._erfassungsart_id

    @erfassungsart_id.setter
    def erfassungsart_id(self, value):

        """finde den status_id im model des uiAwbStatusCombo"""
        match_index = self.uiErfassCombo.model().match(
            self.uiErfassCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiErfassCombo.setCurrentIndex(match_index[0].row())
            self._erfassungsart_id = value
        else:
            self._erfassungsart_id = 0

    @property  # getter
    def erfassungsart_mci(self):

        erfass_mci = self.uiErfassCombo.currentData(Qt.UserRole)

        return erfass_mci

    @property  # getter
    def status_id(self):

        self._status_id = self.uiStatusCombo.currentData(Qt.UserRole + 1)
        return self._status_id

    @status_id.setter
    def status_id(self, value):

        """finde den status_id im model des uiAwbStatusCombo"""
        match_index = self.uiStatusCombo.model().match(
            self.uiStatusCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiStatusCombo.setCurrentIndex(match_index[0].row())
            self._status_id = value
        else:
            self._status_id = 0

    @property  # getter
    def status_mci(self):

        status_mci = self.uiStatusCombo.currentData(Qt.UserRole)

        return status_mci

    def __init__(self, parent=None):
        super(Abgrenzung, self).__init__(parent)
        self.setupUi(self)

    def initEntityWidget(self):

        self.setErfassungComboData()
        self.setStatusComboData()

    def mapEntityData(self):

        self.uiAktLbl.setText(self.parent.parent.name + ' (AZ '
                              + str(self.parent.parent.az) + ')')

        self.jahr = self._entity_mci.jahr
        self.awb = self._entity_mci.awb
        self.bearbeiter = self._entity_mci.bearbeiter
        self.anm = self._entity_mci.anmerkung
        self.bez = self._entity_mci.bezeichnung

        self.erfassungsart_id = self._entity_mci.erfassungsart_id
        self.status_id = self._entity_mci.status_id

    def changedStatus(self):
        """
        steuere die sichtbarkeit des bezeichnungs-lineedit wenn der status der
        abgrenzung geändert wird
        :return:
        """

        self.status_id = self.uiStatusCombo.currentData(Qt.UserRole)

        if self.status_id == 1:  # plan
            self.uiBezeichnungLbl.setVisible(True)
            self.uiBezeichnungLedit.setVisible(True)

        if self.status_id == 0:  # ist
            self.uiBezeichnungLbl.setVisible(False)
            self.uiBezeichnungLedit.setVisible(False)

    def setErfassungComboData(self):
        """
        hole die daten für die erfassungsart_id-combobox aus der datenbank und
        füge sie in die combobox ein
        """
        erfass_stmt = select(BErfassungsart)
        erfass_mci_list = self.entity_session.scalars(erfass_stmt).all()

        """erstelle ein model mit 1 spalten für das type-combo"""
        erfass_model = QStandardItemModel(len(erfass_mci_list), 1)
        for i in range(len(erfass_mci_list)):
            erfass_model.setData(erfass_model.index(i, 0),
                                          erfass_mci_list[i].name, Qt.DisplayRole)
            erfass_model.setData(erfass_model.index(i, 0),
                                          erfass_mci_list[i].id, Qt.UserRole + 1)
            erfass_model.setData(erfass_model.index(i, 0),
                                          erfass_mci_list[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiErfassCombo.setModel(erfass_model)
        """"""

    def setStatusComboData(self):
        """
        hole die daten für die erfassungsart_id-combobox aus der datenbank und
        füge sie in die combobox ein
        """
        status_stmt = select(BAbgrenzungStatus)
        status_mci_list = self.entity_session.scalars(status_stmt).all()

        """erstelle ein model mit 1 spalten für das type-combo"""
        status_model = QStandardItemModel(len(status_mci_list), 1)
        for i in range(len(status_mci_list)):
            status_model.setData(status_model.index(i, 0),
                                          status_mci_list[i].name, Qt.DisplayRole)
            status_model.setData(status_model.index(i, 0),
                                          status_mci_list[i].id, Qt.UserRole + 1)
            status_model.setData(status_model.index(i, 0),
                                          status_mci_list[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiStatusCombo.setModel(status_model)
        """"""
        
    def submitEntity(self):

        self._entity_mci.jahr = self.jahr
        self._entity_mci.awb = self.awb
        self._entity_mci.bearbeiter = self.bearbeiter
        self._entity_mci.anmerkung = self.anm
        self._entity_mci.bezeichnung = self.bez

        self._entity_mci.erfassungsart_id = self.erfassungsart_id
        self._entity_mci.rel_erfassungsart = self.erfassungsart_mci
        self._entity_mci.status_id = self.status_id
        self._entity_mci.rel_status = self.status_mci

    def signals(self):

        self.uiStatusCombo.currentIndexChanged.connect(self.changedStatus)


class AbgrenzungDialog(MainDialog):
    """
    dialog für ein entity-widget (Entity)
    """

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.parent = parent
        self.enableApply = True
        self.set_apply_button_text('&Speichern und Schließen')

        self.setMinimumWidth(500)
        self.setMaximumWidth(800)

    def accept(self):
        """
        wenn 'acceptEntity' des entity-widget True zurückgibt (die daten sind
        gültig) dann rufe QDialog.accept() auf
        """

        self.dialogWidget.submitData()
        super().accept()