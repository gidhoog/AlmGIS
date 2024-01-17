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
    _status_id = None

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
    def status_id(self):

        self._status_id = self.uiStatusCombo.currentData(Qt.UserRole)
        return self._status_id

    @status_id.setter
    def status_id(self, value):

        self.uiStatusCombo.setCurrentIndex(
            self.uiStatusCombo.findData(value, Qt.UserRole)
        )
        self._status_id = value

    def __init__(self, parent=None, item=None):
        super(__class__, self).__init__()
        self.setupUi(self)
        
        self.item = item

        self.loadCombos()

        self.mapData()

    def mapData(self):

        self.uiJahrSbox.setValue(self.item.data(GisItem.Jahr_Role))

        self.erfassungsart_id = self.item.data(GisItem.ErfassungsArtId_Role)
        self.status_id = self.item.data(GisItem.StatusId_Role)

    def loadCombos(self):

        with db_session_cm() as session:

            stmt = select(BErfassungsart)
            erfassungsart_di = session.scalars(stmt).all()

            stmt_status = select(BAbgrenzungStatus)
            status_di = session.scalars(stmt_status).all()

            for erfass in erfassungsart_di:
                self.uiErfassCombo.addItem(erfass.name, erfass.id)
            for status in status_di:
                self.uiStatusCombo.addItem(status.name, status.id)
        
    def submitData(self):
        
        self.item.setData(self.uiJahrSbox.value(), GisItem.Jahr_Role)

        self.item.setData(self.erfassungsart_id, GisItem.ErfassungsArtId_Role)
        self.item.setData(self.status_id, GisItem.StatusId_Role)


class AbgrenzungDialog(MainDialog):
    """
    dialog für ein entity-widget (Entity)
    """

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.parent = parent
        self.enableApply = True
        self.set_apply_button_text('&Speichern und Schließen')

        self.setMaximumWidth(500)

    def accept(self):
        """
        wenn 'acceptEntity' des entity-widget True zurückgibt (die daten sind
        gültig) dann rufe QDialog.accept() auf
        """
        # if self.dialogWidget.acceptEntity():
        #     super().accept()
        
        self.dialogWidget.submitData()
        super().accept()