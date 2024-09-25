from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItemModel
from sqlalchemy import select

from core import entity, db_session_cm
from core.data_model import BGstAwbStatus, BRechtsgrundlage
from core.gis_tools import cut_koppel_gstversion
from core.scopes.gst import gst_zuordnung_dataform_UI
from core.scopes.gst.gst import Gst


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
    _rechtsgrundlage = 0

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

        self.uiKgLbl.setText(str(value))
        self._kg = value

    @property  # getter
    def awb_status_id(self):

        self._awb_status_id = self.uiAwbStatusCombo.currentData(Qt.UserRole + 1)
        return self._awb_status_id

    @awb_status_id.setter
    def awb_status_id(self, value):

        # self.uiAwbStatusCombo.setCurrentIndex(
        #     self.uiAwbStatusCombo.findText(value.name))
        # self._awb_status_id = value

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
    def rechtsgrundlage(self):

        self._rechtsgrundlage = self.uiRechtsgrundlageCombo.currentData(Qt.UserRole)
        return self._rechtsgrundlage

    @rechtsgrundlage.setter
    def rechtsgrundlage(self, value):

        # self.uiRechtsgrundlageCombo.setCurrentIndex(
        #     self.uiRechtsgrundlageCombo.findData(value, Qt.UserRole)
        # )
        self.uiRechtsgrundlageCombo.setCurrentIndex(
            self.uiRechtsgrundlageCombo.findText(value.name))
        self._rechtsgrundlage = value

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

    # @property  # getter
    # def last_edit(self):
    #     return self._last_edit
    #
    # @last_edit.setter
    # def last_edit(self, value):
    #
    #     if value and self._entity_mci.time_edit:
    #         user = value
    #         time = self._entity_mci.time_edit[0:19]
    #         le = user + '/' + str(time)
    #         self.uiLastEditedLbl.setText(le)
    #
    #     self._last_edit = value

    def __init__(self, parent=None, session=None):
        super(__class__, self).__init__(parent, session)
        self.setupUi(self)

        """lade die listenelemente für die comboboxen"""
        # with db_session_cm() as session:
        #
        #     status_items = session.query(BGstAwbStatus).\
        #         order_by(BGstAwbStatus.sort).\
        #         all()
        #     recht_items = session.query(BRechtsgrundlage).\
        #         order_by(BRechtsgrundlage.sort).\
        #         all()

        # for item in status_items:
        #     self.uiAwbStatusCombo.addItem(item.name, item)
        # for r_item in recht_items:
        #     self.uiRechtsgrundlageCombo.addItem(r_item.name, r_item)
        """"""

    def loadSubWidgets(self):
        super().loadSubWidgets()

        # self.gst_info = Gst(self)
        # self.gst_info.editEntity(self._entity_mci.rel_gst, None)
        # self.addGstInfo()

    def addGstInfo(self):

        self.uiCentralLayoutHbox.addWidget(self.gst_info)

    def initEntityWidget(self):

        self.setStatusComboData()

    def mapData(self):
        super().mapData()

        # for item in self._custom_entity_data['awb_status']:
        #     self.uiAwbStatusCombo.addItem(item.name, item)
        #
        # for item in self._custom_entity_data['recht_status']:
        #     self.uiRechtsgrundlageCombo.addItem(item.name, item)

        self.akt = self._entity_mci.rel_akt.name
        self.gst_nr = self._entity_mci.rel_gst.gst
        self.kg = self._entity_mci.rel_gst.kgnr
        self.awb_status_id = self._entity_mci.awb_status_id
        # self.rechtsgrundlage = self._entity_mci.rel_rechtsgrundlage

        self.anmerkung = self._entity_mci.anmerkung
        self.probleme = self._entity_mci.probleme
        self.aufgaben = self._entity_mci.aufgaben
        self.gb_wrong = self._entity_mci.gb_wrong
        self.awb_wrong = self._entity_mci.awb_wrong
        # self.last_edit = self._entity_mci.user_edit

    def submitEntity(self):
        super().submitEntity()

        """wichtig ist hier, dass sowohl der status_id als auch der
        status_id selbst (als mci) an '_entity_mci' übergeben werden"""
        self._entity_mci.awb_status_id = self.awb_status_id
        self._entity_mci.rel_awb_status = self.awb_status_mci

        # self._entity_mci.rechtsgrundlage_id = self.rechtsgrundlage.id
        # self._entity_mci.rel_rechtsgrundlage = self.rechtsgrundlage
        """"""

        self._entity_mci.anmerkung = self.anmerkung
        self._entity_mci.probleme = self.probleme
        self._entity_mci.aufgaben = self.aufgaben
        self._entity_mci.gb_wrong = self.gb_wrong
        self._entity_mci.awb_wrong = self.awb_wrong

        print(f'...')

    def setStatusComboData(self):
        """
        hole die daten für die status_id-combobox aus der datenbank und füge
        sie in die combobox ein
        """
        # status_items = sorted(self._custom_entity_data['bearbeitungsstatus'],
        #                       key=lambda x:x.sort)

        # with db_session_cm(name='query akt bearbeitungsstatuse',
        #                    expire_on_commit=False) as session:

        status_stmt = select(BGstAwbStatus)
        status_mci_list = self.entity_session.scalars(status_stmt).all()

            # for item in status_items:
            #     self.uiStatusCombo.addItem(item.name, item.id)

        """erstelle ein model mit 1 spalten für das type-combo"""
        status_model = QStandardItemModel(len(status_mci_list), 1)
        for i in range(len(status_mci_list)):
            # id = type_items[i].id
            # name = type_items[i].name
            status_model.setData(status_model.index(i, 0),
                                          status_mci_list[i].name, Qt.DisplayRole)
            status_model.setData(status_model.index(i, 0),
                                          status_mci_list[i].id, Qt.UserRole + 1)
            status_model.setData(status_model.index(i, 0),
                                          status_mci_list[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiAwbStatusCombo.setModel(status_model)
        # self.uiTypCombo.setModelColumn(1)
        """"""