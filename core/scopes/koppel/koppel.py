from core import db_session_cm
from core.data_model import BErfassungsart, BAbgrenzungStatus
from core.entity import Entity
from core.gis_item import GisItem
from core.main_dialog import MainDialog
from core.scopes.koppel import koppel_UI
from qgis.PyQt.QtWidgets import QWidget
# from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtCore import Qt

from sqlalchemy import select


class Koppel(koppel_UI.Ui_Koppel, Entity):

    # _erfassungsart_name = ''
    # _status_id = None
    # _status_name = ''
    #
    _name = ''
    _nr = 0
    _nicht_weide = 0
    _anm = ''

    @property  # getter
    def name(self):

        self._name = self.uiNameLedit.text()
        return self._name

    @name.setter
    def name(self, value):

        self.uiNameLedit.setText(value)
        self._name = value

    @property  # getter
    def nr(self):

        self._nr = self.uiNrSbox.value()
        return self._nr

    @nr.setter
    def nr(self, value):

        self.uiNrSbox.setValue(value)
        self._nr = value

    @property  # getter
    def nicht_weide(self):

        if self.uiNichtWeideCbox.isChecked():
            self._nicht_weide = 1
        else:
            self._nicht_weide = 0

        return self._nicht_weide

    @nicht_weide.setter
    def nicht_weide(self, value):

        if value == 1:
            self.uiNichtWeideCbox.setChecked(Qt.Checked)
        else:
            self.uiNichtWeideCbox.setChecked(Qt.Unchecked)

        self._nicht_weide = value

    @property  # getter
    def anm(self):

        self._anm = self.uiAnmerkungPtext.toPlainText()
        return self._anm

    @anm.setter
    def anm(self, value):

        self.uiAnmerkungPtext.setPlainText(value)
        self._anm = value

    def __init__(self, parent=None, item=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

        # self.uiAktNameLbl.setText(self.parent.name + ' (AZ '
        #                           + str(self.parent.az) + ')')

        # komplex_name = self.item.parent().data(GisItem.Name_Role)
        # self.uiKomplexNameLbl.setText(komplex_name)

    #     self.uiStatusCombo.currentIndexChanged.connect(self.changedStatus)
    #
    #     self.loadCombos()

    def mapEntityData(self):
        # self.uiStatusCombo.currentIndexChanged.connect(self.changedStatus)

        self.name = self._entity_mci.name
        self.nr = self._entity_mci.nr
        self.nicht_weide = self._entity_mci.nicht_weide
        self.anm = self._entity_mci.anmerkung

        # self.uiAreaLbl.setText(str(self._entity_mci.koppel_area))
        self.uiAreaLbl.setText(
            '{:.4f}'.format(
                round(float(self._entity_mci.koppel_area) / 10000, 4))
            .replace(".", ",") + ' ha')

    # def changedStatus(self):
    #
    #     self.status_id = self.uiStatusCombo.currentData(Qt.UserRole)
    #
    #     if self.status_id == 1:  # plan
    #         self.uiBezeichnungLbl.setVisible(True)
    #         self.uiBezeichnungLedit.setVisible(True)
    #
    #     if self.status_id == 0:  # ist
    #         self.uiBezeichnungLbl.setVisible(False)
    #         self.uiBezeichnungLedit.setVisible(False)
    #
    # def loadCombos(self):
    #
    #     with db_session_cm() as session:
    #
    #         stmt = select(BErfassungsart)
    #         erfassungsart_di = session.scalars(stmt).all()
    #
    #         stmt_status = select(BAbgrenzungStatus)
    #         status_di = session.scalars(stmt_status).all()
    #
    #         for erfass in erfassungsart_di:
    #             self.uiErfassCombo.addItem(erfass.name, erfass.id)
    #         for status_id in status_di:
    #             self.uiStatusCombo.addItem(status_id.name_short, status_id.id)
    #
    def submitData(self):

        self.item.setData(self.uiNameLedit.text(), GisItem.Name_Role)
        self.item.setData(self.uiNrSbox.value(), GisItem.Nr_Role)

        self.item.setData(self.nicht_weide, GisItem.NichtWeide_Role)

        self.item.setData(self.uiAnmerkungPtext.toPlainText(),
                          GisItem.Anmerkung_Role)



        # """um nach einer Änderung des Statues den richtigen Wert im
        # Abgrenzungs-View darzustellen, muss zusätzlich zum id (=wichtig für
        # das abspeichern) auch der Text des aktuellen Elements übergeben
        # werden"""
        # self.item.setData(self.status_id, GisItem.StatusId_Role)
        # self.item.setData(self.status_name, GisItem.StatusName_Role)
        #
        # self.item.setData(self.erfassungsart_id, GisItem.ErfassungsArtId_Role)
        # self.item.setData(self.erfassungsart_name,
        #                   GisItem.ErfassungsArtName_Role)
        # """"""
        #
        # self.item.setData(self.uiBearbeiterLedit.text(),
        #                   GisItem.Bearbeiter_Role)
        # self.item.setData(self.uiBezeichnungLedit.text(),
        #                   GisItem.Bezeichnung_Role)
        # self.item.setData(self.uiAnmerkungPtext.toPlainText(),
        #                   GisItem.Anmerkung_Role)


class KoppelDialog(MainDialog):
    """
    dialog für ein entity-widget (Entity)
    """

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.parent = parent
        self.enableApply = True
        self.set_apply_button_text('&Speichern und Schließen')

        self.setMinimumWidth(250)
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