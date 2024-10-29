from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItemModel
from sqlalchemy import select

from app_core import entity
from app_core.data_model import BGstAwbStatus, BRechtsgrundlage, BKatGem
from app_core.scopes.gst import gst_zuordnung_dataform_UI


class GstZuordnungDataForm(gst_zuordnung_dataform_UI.Ui_GstZuordnungDataForm,
                           entity.Entity):
    """
    klasse für ein zugeordnetes grundstück
    """

    _akt = ''
    _gst_nr = ''
    _kg = ''
    _awb_status_id = 0
    _awb_status_mci = None
    _rechtsgrundlage_id = 0
    _rechtsgrundlage_mci = None

    _anmerkung = ''
    _probleme = ''
    _aufgaben = ''

    _gb_wrong = False
    _awb_wrong = False

    _last_edit = ''
    _commit_on_apply = False

    @property  # getter
    def akt(self):

        self._akt = self.uiAktLbl.text()
        return self._nr

    @akt.setter
    def akt(self, value):

        self.uiAktLbl.setText(value)
        self._akt = value

    @property  # getter
    def gst_nr(self):

        self._gst_nr = self.uiGstLbl.text()
        return self._gst_nr

    @gst_nr.setter
    def gst_nr(self, value):

        self.uiGstLbl.setText(value)
        self._gst_nr = value

    @property  # getter
    def kg(self):

        self._kg = self.uiKgLbl.text()
        return self._kg

    @kg.setter
    def kg(self, value):

        kg_mci = self.entity_session.get(BKatGem, value)

        self.uiKgLbl.setText(str(value) + ' ' + kg_mci.kgname)
        self._kg = value

    @property  # getter
    def awb_status_id(self):

        self._awb_status_id = self.uiAwbStatusCombo.currentData(Qt.UserRole + 1)
        return self._awb_status_id

    @awb_status_id.setter
    def awb_status_id(self, value):

        """finde den status_id im model des uiAwbStatusCombo"""
        match_index = self.uiAwbStatusCombo.model().match(
            self.uiAwbStatusCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiAwbStatusCombo.setCurrentIndex(match_index[0].row())
            self._awb_status_id = value
        else:
            self._awb_status_id = 0

    @property  # getter
    def awb_status_mci(self):

        status_mci = self.uiAwbStatusCombo.currentData(Qt.UserRole)
        return status_mci

    @property  # getter
    def rechtsgrundlage_id(self):

        self._rechtsgrundlage_id = self.uiRechtsgrundlageCombo.currentData(
            Qt.UserRole + 1)
        return self._rechtsgrundlage_id

    @rechtsgrundlage_id.setter
    def rechtsgrundlage_id(self, value):

        """finde den rechtsgrundlage_id im model des uiRechtsgrundlageCombo"""
        match_index = self.uiRechtsgrundlageCombo.model().match(
            self.uiRechtsgrundlageCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiRechtsgrundlageCombo.setCurrentIndex(match_index[0].row())
            self._rechtsgrundlage_id = value
        else:
            self._rechtsgrundlage_id = 0


        self._rechtsgrundlage_id = value

    @property  # getter
    def rechtsgrundlage_mci(self):

        rg_mci = self.uiRechtsgrundlageCombo.currentData(Qt.UserRole)
        return rg_mci

    @property  # getter
    def anmerkung(self):

        self._anmerkung = self.uiAnmTedit.toPlainText()
        return self._anmerkung

    @anmerkung.setter
    def anmerkung(self, value):

        self.uiAnmTedit.setPlainText(value)
        self._anmerkung = value

    @property  # getter
    def probleme(self):

        self._probleme = self.uiProblemTedit.toPlainText()
        return self._probleme

    @probleme.setter
    def probleme(self, value):

        self.uiProblemTedit.setPlainText(value)
        self._probleme = value

    @property  # getter
    def aufgaben(self):

        self._aufgaben = self.uiAufgabeTedit.toPlainText()
        return self._aufgaben

    @aufgaben.setter
    def aufgaben(self, value):

        self.uiAufgabeTedit.setPlainText(value)
        self._aufgaben = value

    @property  # getter
    def gb_wrong(self):

        if self.uiGbWrongCbox.checkState() == 2:
            self._gb_wrong = True
        else:
            self._gb_wrong = False
        return self._gb_wrong

    @gb_wrong.setter
    def gb_wrong(self, value):

        if value == True:
            self.uiGbWrongCbox.setChecked(Qt.Checked)

        self._gb_wrong = value

    @property  # getter
    def awb_wrong(self):

        if self.uiAwbWrongCbox.checkState() == 2:
            self._awb_wrong = True
        else:
            self._awb_wrong = False
        return self._awb_wrong

    @awb_wrong.setter
    def awb_wrong(self, value):

        if value == True:
            self.uiAwbWrongCbox.setChecked(Qt.Checked)

        self._awb_wrong = value

    @property  # getter
    def last_edit(self):
        return self._last_edit

    @last_edit.setter
    def last_edit(self, value):

        try:
            if value and self._entity_mci.time_edit:
                user = value
                time = self._entity_mci.time_edit[0:19]
                self._last_edit = user + '/' + str(time)
        except:
            self._last_edit = 'n.b.'

        self.uiLastEditedLbl.setText(self._last_edit)

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

    def addGstInfo(self):

        self.uiCentralLayoutHbox.addWidget(self.gst_info)

    def loadBackgroundData(self):
        super().loadBackgroundData()

        self.setStatusComboData()
        self.setRechtsgrundComboData()

    def mapEntityData(self):
        super().mapEntityData()

        self.akt = self._entity_mci.rel_akt.name
        self.gst_nr = self._entity_mci.rel_gst.gst
        self.kg = self._entity_mci.rel_gst.kgnr
        self.awb_status_id = self._entity_mci.awb_status_id
        self.rechtsgrundlage_id = self._entity_mci.rechtsgrundlage_id

        self.anmerkung = self._entity_mci.anmerkung
        self.probleme = self._entity_mci.probleme
        self.aufgaben = self._entity_mci.aufgaben
        self.gb_wrong = self._entity_mci.gb_wrong
        self.awb_wrong = self._entity_mci.awb_wrong
        self.last_edit = self._entity_mci.user_edit

    def submitEntity(self):
        super().submitEntity()

        """wichtig ist hier, dass sowohl der status_id als auch der
        status_id selbst (als mci) an '_entity_mci' übergeben werden"""
        self._entity_mci.awb_status_id = self.awb_status_id
        self._entity_mci.rel_awb_status = self.awb_status_mci

        self._entity_mci.rechtsgrundlage_id = self.rechtsgrundlage_id
        self._entity_mci.rel_rechtsgrundlage = self.rechtsgrundlage_mci
        """"""

        self._entity_mci.anmerkung = self.anmerkung
        self._entity_mci.probleme = self.probleme
        self._entity_mci.aufgaben = self.aufgaben
        self._entity_mci.gb_wrong = self.gb_wrong
        self._entity_mci.awb_wrong = self.awb_wrong

    def setStatusComboData(self):
        """
        hole die daten für die status_id-combobox aus der datenbank und füge
        sie in die combobox ein
        """
        status_stmt = select(BGstAwbStatus)
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
        self.uiAwbStatusCombo.setModel(status_model)
        """"""

    def setRechtsgrundComboData(self):
        """
        hole die daten für die rechtsgrundlage_id-combobox aus der datenbank
        und füge sie in die combobox ein
        """
        rechtsgrund_stmt = select(BRechtsgrundlage)
        rg_mci_list = self.entity_session.scalars(rechtsgrund_stmt).all()

        """erstelle ein model mit 1 spalten für das type-combo"""
        rg_model = QStandardItemModel(len(rg_mci_list), 1)
        for i in range(len(rg_mci_list)):
            rg_model.setData(rg_model.index(i, 0),
                                          rg_mci_list[i].name, Qt.DisplayRole)
            rg_model.setData(rg_model.index(i, 0),
                                          rg_mci_list[i].id, Qt.UserRole + 1)
            rg_model.setData(rg_model.index(i, 0),
                                          rg_mci_list[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiRechtsgrundlageCombo.setModel(rg_model)
        """"""