from core import db_session_cm
from core.data_model import BErfassungsart, BAbgrenzungStatus
from core.gis_item import GisItem
from core.main_dialog import MainDialog
from core.scopes.akte import abgrenzung_UI
from qgis.PyQt.QtWidgets import QWidget
# from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtCore import Qt

from sqlalchemy import select


class Abgrenzung(QWidget, abgrenzung_UI.Ui_Abgrenzung):

    _erfassungsart_id = None
    _erfassungsart_name = ''
    _status_id = None
    _status_name = ''

    @property  # getter
    def erfassungsart_id(self):

        self._erfassungsart_id = self.uiErfassCombo.currentData(Qt.UserRole)
        return self._erfassungsart_id

    @erfassungsart_id.setter
    def erfassungsart_id(self, value):

        self.uiErfassCombo.setCurrentIndex(
            self.uiErfassCombo.findData(value, Qt.UserRole)
        )
        self._erfassungsart_id = value

    @property  # getter
    def erfassungsart_name(self):

        self._erfassungsart_name = self.uiErfassCombo.currentText()
        return self._erfassungsart_name

    @property  # getter
    def status_id(self):

        self._status_id = self.uiStatusCombo.currentData(Qt.UserRole)
        return self._status_id

    @status_id.setter
    def status_id(self, value):

        self.uiStatusCombo.setCurrentIndex(
            self.uiStatusCombo.findData(value, Qt.UserRole)
        )
        # if value == 1:  # plan
        #     self.uiBezeichnungLbl.setVisible(True)
        #     self.uiBezeichnungLedit.setVisible(True)
        #
        # if value == 0:  # ist
        #     self.uiBezeichnungLbl.setVisible(False)
        #     self.uiBezeichnungLedit.setVisible(False)

        self._status_id = value

        # self.changedStatus()

    @property  # getter
    def status_name(self):

        self._status_name = self.uiStatusCombo.currentText()
        return self._status_name

    def __init__(self, parent=None, item=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent
        self.item = item

        self.uiAktNameLbl.setText(self.parent.name + ' (AZ '
                                  + str(self.parent.az) + ')')

        self.uiStatusCombo.currentIndexChanged.connect(self.changedStatus)

        self.loadCombos()

        self.mapData()

    def mapData(self):
        # self.uiStatusCombo.currentIndexChanged.connect(self.changedStatus)

        self.uiJahrSbox.setValue(self.item.data(GisItem.Jahr_Role))
        self.uiBearbeiterLedit.setText(self.item.data(GisItem.Bearbeiter_Role))
        self.uiBezeichnungLedit.setText(self.item.data(GisItem.Bezeichnung_Role))
        self.uiAnmerkungPtext.setPlainText(self.item.data(GisItem.Anmerkung_Role))

        self.erfassungsart_id = self.item.data(GisItem.ErfassungsArtId_Role)
        self.status_id = self.item.data(GisItem.StatusId_Role)

    def changedStatus(self):

        self.status_id = self.uiStatusCombo.currentData(Qt.UserRole)

        if self.status_id == 1:  # plan
            self.uiBezeichnungLbl.setVisible(True)
            self.uiBezeichnungLedit.setVisible(True)

        if self.status_id == 0:  # ist
            self.uiBezeichnungLbl.setVisible(False)
            self.uiBezeichnungLedit.setVisible(False)

    def loadCombos(self):

        with db_session_cm() as session:

            stmt = select(BErfassungsart)
            erfassungsart_di = session.scalars(stmt).all()

            stmt_status = select(BAbgrenzungStatus)
            status_di = session.scalars(stmt_status).all()

            for erfass in erfassungsart_di:
                self.uiErfassCombo.addItem(erfass.name, erfass.id)
            for status in status_di:
                self.uiStatusCombo.addItem(status.name_short, status.id)
        
    def submitData(self):
        
        self.item.setData(self.uiJahrSbox.value(), GisItem.Jahr_Role)


        """um nach einer Änderung des Statues den richtigen Wert im 
        Abgrenzungs-View darzustellen, muss zusätzlich zum id (=wichtig für
        das abspeichern) auch der Text des aktuellen Elements übergeben 
        werden"""
        self.item.setData(self.status_id, GisItem.StatusId_Role)
        self.item.setData(self.status_name, GisItem.StatusName_Role)

        self.item.setData(self.erfassungsart_id, GisItem.ErfassungsArtId_Role)
        self.item.setData(self.erfassungsart_name, GisItem.ErfassungsArtName_Role)
        """"""

        self.item.setData(self.uiBearbeiterLedit.text(), GisItem.Bearbeiter_Role)
        self.item.setData(self.uiBezeichnungLedit.text(), GisItem.Bezeichnung_Role)
        self.item.setData(self.uiAnmerkungPtext.toPlainText(), GisItem.Anmerkung_Role)


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
        # if self.dialogWidget.acceptEntity():
        #     super().accept()
        
        self.dialogWidget.submitData()
        super().accept()