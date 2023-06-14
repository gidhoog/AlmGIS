from PyQt5.QtCore import Qt
from core import entity, DbSession
from core.data_model import BGstAwbStatus, BRechtsgrundlage
from core.gis_tools import cut_koppel_gstversion
from core.scopes.gst import gst_zuordnung_dataform_UI


class GstZuordnungDataForm(gst_zuordnung_dataform_UI.Ui_GstZuordnungDataForm,
                           entity.Entity):
    """
    klasse für ein zugeordnetes grundstück
    """

    _akt = ''
    _gst_nr = ''
    _kg = ''
    _awb_status = 0
    _rechtsgrundlage = 0

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
    def awb_status(self):

        self._awb_status = self.uiAwbStatusCombo.currentData(Qt.UserRole)
        return self._awb_status

    @awb_status.setter
    def awb_status(self, value):

        self.uiAwbStatusCombo.setCurrentIndex(
            self.uiAwbStatusCombo.findData(value, Qt.UserRole)
        )
        self._awb_status = value

    @property  # getter
    def rechtsgrundlage(self):

        self._rechtsgrundlage = self.uiRechtsgrundlageCombo.currentData(Qt.UserRole)
        return self._rechtsgrundlage

    @rechtsgrundlage.setter
    def rechtsgrundlage(self, value):

        self.uiRechtsgrundlageCombo.setCurrentIndex(
            self.uiRechtsgrundlageCombo.findData(value, Qt.UserRole)
        )
        self._rechtsgrundlage = value

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        """lade die listenelemente für die comboboxen"""
        with DbSession.session_scope() as session:

            status_items = session.query(BGstAwbStatus).\
                order_by(BGstAwbStatus.sort).\
                all()
            recht_items = session.query(BRechtsgrundlage).\
                order_by(BRechtsgrundlage.sort).\
                all()

        for item in status_items:
            self.uiAwbStatusCombo.addItem(item.name, item.id)
        for r_item in recht_items:
            self.uiRechtsgrundlageCombo.addItem(r_item.name, r_item.id)
        """"""

    def mapData(self):
        super().mapData()

        self.akt = self.data_instance.rel_akt.name
        self.gst_nr = self.data_instance.rel_gst.gst
        self.kg = self.data_instance.rel_gst.kgnr
        self.awb_status = self.data_instance.awb_status_id
        self.rechtsgrundlage = self.data_instance.rechtsgrundlage_id

    def submitEntity(self):
        super().submitEntity()

        self.data_instance.awb_status_id = self.awb_status
        self.data_instance.rechtsgrundlage_id = self.rechtsgrundlage

    def commitEntity(self):
        super().commitEntity()

        cut_koppel_gstversion()
        self.parent.parent.guiMainGis.uiCanvas.refresh()
        self.parent.parent.komplex_table.updateMaintable()
