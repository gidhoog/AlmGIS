from core import db_session_cm
from core.data_model import BErfassungsart, BAbgrenzungStatus, BKomplexName
from core.entity import Entity
from core.gis_item import GisItem
from core.main_dialog import MainDialog
from core.scopes.koppel import koppel_UI
from qgis.PyQt.QtWidgets import QWidget
# from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItemModel

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
    _komplex_id = 0
    _komplex_mci = None

    _commit_on_apply = False

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

    @property  # getter
    def komplex_id(self):

        self._komplex_id = self.uiKomplexCombo.currentData(Qt.UserRole + 1)
        return self._komplex_id

    @komplex_id.setter
    def komplex_id(self, value):

        """finde den status_id im model des uiAwbStatusCombo"""
        match_index = self.uiKomplexCombo.model().match(
            self.uiKomplexCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiKomplexCombo.setCurrentIndex(match_index[0].row())
            self._komplex_id = value
        else:
            self._komplex_id = 0

    @property  # getter
    def komplex_mci(self):

        mci = self.uiKomplexCombo.currentData(Qt.UserRole)
        return mci

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
        self.komplex_id = self._entity_mci.rel_komplex.komplex_name_id

        # self.uiAreaLbl.setText(str(self._entity_mci.koppel_area))
        self.uiAreaLbl.setText(
            '{:.4f}'.format(
                round(float(self._entity_mci.koppel_area) / 10000, 4))
            .replace(".", ",") + ' ha')

    def loadBackgroundData(self):
        super().loadBackgroundData()

        self.setKomplexComboData()

    def setKomplexComboData(self):
        """
        hole die daten für die status_id-combobox aus der datenbank und füge
        sie in die combobox ein
        """
        akt_id = self._entity_mci.rel_komplex.rel_abgrenzung.rel_akt.id
        # oder: akt_id = self.parent.parent.entity_id
        pass
        komplexe_stmt = select(BKomplexName).where(BKomplexName.akt_id == akt_id).order_by(BKomplexName.nr)
        komplexe_mci_list = self.entity_session.scalars(komplexe_stmt).all()

        """erstelle ein model mit 1 spalten für das type-combo"""
        komplex_model = QStandardItemModel(len(komplexe_mci_list), 1)
        for i in range(len(komplexe_mci_list)):

            if komplexe_mci_list[i].nr == 0 or komplexe_mci_list[i].nr is None:
                nr = 0
            else:
                nr = komplexe_mci_list[i].nr

            text = f'{str(nr)}: {komplexe_mci_list[i].name}'
            komplex_model.setData(komplex_model.index(i, 0),
                                          text, Qt.DisplayRole)
            komplex_model.setData(komplex_model.index(i, 0),
                                          komplexe_mci_list[i].id, Qt.UserRole + 1)
            komplex_model.setData(komplex_model.index(i, 0),
                                          komplexe_mci_list[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiKomplexCombo.setModel(komplex_model)
        """"""

    def submitEntity(self):

        self._entity_mci.name = self.name
        self._entity_mci.nr = self.nr
        self._entity_mci.nicht_weide = self.nicht_weide
        self._entity_mci.anmerkung = self.anm

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