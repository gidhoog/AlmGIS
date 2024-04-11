import sys
from _operator import attrgetter

from qgis.PyQt.QtCore import Qt, QModelIndex, QAbstractTableModel
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QLabel, QComboBox
from qgis.core import QgsGeometry

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from core import db_session_cm
from core.data_model import BAkt, BKomplex, BGstZuordnung, BGst, BGstVersion, \
    BGstEz, BCutKoppelGstAktuell, BBearbeitungsstatus, BAbgrenzung
from core.entity import EntityDialog
from core.data_view import DataView, TableModel, TableView
from core.gis_layer import AktAllLayer, Feature
from core.main_widget import MainWidget
from core.scopes.akte.akt import Akt


class AkteAllMainWidget(MainWidget):
    """
    MainWidget für die Darstellung eines DataView's mit allen Akten
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.uiTitleLbl.setText('alle Akte')

        self.akt_all_table = AkteAllMain(self)

    def initMainWidget(self):
        super().initMainWidget()

        self.uiMainVLay.addWidget(self.akt_all_table)

        # self.akt_all_table.loadData()
        # self.akt_all_table.initDataView()


class AktAllModel(TableModel):

    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)

        self.header = ['AZ',
                       'Name',
                       'Status',
                       'Stz',
                       'Anmerkung',
                       'WWP',
                       'WWP-Jahr',
                       'AWB-Fläche (GB)',
                       'davon beweidet',
                       'Weidefläche']

    def data(self, index: QModelIndex, role: int = ...):

        """
        erzeuge ein basis-model
        """
        row = index.row()
        col = index.column()

        if role == Qt.TextAlignmentRole:

            if index.column() in [7, 8, 9]:

                return Qt.AlignRight | Qt.AlignVCenter

            if index.column() in [0, 2, 3, 5, 6]:

                return Qt.AlignHCenter | Qt.AlignVCenter

        if role == Qt.BackgroundRole:

            if index.column() == 2:

                if self.mci_list[row].rel_bearbeitungsstatus is not None:

                    color_str = self.mci_list[row].rel_bearbeitungsstatus.color
                    color_list = color_str.split(", ")

                    return QColor(int(color_list[0]),
                                  int(color_list[1]),
                                  int(color_list[2]))


        if index.column() == 0:
            if role == Qt.DisplayRole:
                return self.mci_list[row].az
            # if role == Qt.EditRole:
            #     return self.parent._mci_list[row].az

        if index.column() == 1:
            if role == Qt.DisplayRole:
                return self.mci_list[row].name
            # if role == Qt.EditRole:
            #     return self.mci_list[row].name

        if index.column() == 2:

            if self.mci_list[row].rel_bearbeitungsstatus is not None:

                if role == Qt.DisplayRole:
                    return self.mci_list[row].rel_bearbeitungsstatus.name

        if index.column() == 3:
            if role == Qt.DisplayRole:
                return self.mci_list[row].stz

        if index.column() == 4:
            if role == Qt.DisplayRole:
                return self.mci_list[row].anm

        if index.column() == 5:
            if role == Qt.DisplayRole:
                if self.mci_list[row].wwp == 1:
                    return 'X'

        if index.column() == 6:
            if role == Qt.DisplayRole:
                if self.mci_list[row].wwp == 1:
                    if self.mci_list[row].wwp_jahr is not None:
                        return self.mci_list[row].wwp_jahr
                    else:
                        return '---'
                return ''

        if index.column() == 7:
            # anz = 0
            gst_area = 0
            for gst_zuord in self.mci_list[row].rel_gst_zuordnung:
                # anz += 1
                if gst_zuord.awb_status_id == 1:
                    gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
                    last_gst = max(gst_versionen_list,
                                   key=attrgetter('rel_alm_gst_ez.datenstand'))
                    # print(f'last gst: {last_gst.import_time}')
                    gst_m = 0
                    for ba in last_gst.rel_alm_gst_nutzung:
                        gst_m = gst_m + ba.area
                    gst_area = gst_area + gst_m

            if role == Qt.DisplayRole:
                gst_area_ha = '{:.4f}'.format(round(float(gst_area) / 10000, 4)).replace(".", ",") + ' ha'
                return gst_area_ha
            if role == Qt.EditRole:
                return gst_area

        if index.column() == 8:

            cut_area = 0
            for gst_zuord in self.mci_list[row].rel_gst_zuordnung:
                # anz += 1
                if gst_zuord.awb_status_id == 1:
                    gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
                    last_gst = max(gst_versionen_list,
                                   key=attrgetter('rel_alm_gst_ez.datenstand'))

                    for cut in last_gst.rel_cut_koppel_gst:
                        cut_area = cut_area + last_gst.rel_cut_koppel_gst.cutarea
                    # print(f'last gst: {last_gst.import_time}')
                    # gst_m = 0
                    # for ba in last_gst.rel_alm_gst_nutzung:
                    #     gst_m = gst_m + ba.area
                    # gst_area = gst_area + gst_m

            if role == Qt.DisplayRole:
                cut_area_ha = '{:.4f}'.format(round(float(cut_area) / 10000, 4)).replace(".", ",") + ' ha'
                return cut_area_ha

        if index.column() == 9:

            if role in [Qt.DisplayRole, Qt.EditRole]:

                kop_area = 0.00

                # print(f'self.mci_list[row].rel_abgrenzung: {self.mci_list[row].rel_abgrenzung}')

                if self.mci_list[row].rel_abgrenzung != []:

                    last_abgrenzung = max(self.mci_list[row].rel_abgrenzung,
                                      key=attrgetter('jahr'))


                    for komplex in last_abgrenzung.rel_komplex:
                        for koppel in komplex.rel_koppel:
                            kop_area = kop_area + koppel.koppel_area

                    if role == Qt.DisplayRole:
                        kop_area_ha = '{:.4f}'.format(
                            round(float(kop_area) / 10000, 4)).replace(".",
                                                                       ",") + ' ha'
                        return kop_area_ha
                    if role == Qt.EditRole:
                        return kop_area

                else:
                    if role == Qt.DisplayRole:
                        return '---'
                    if role == Qt.EditRole:
                        return 0


class AkteAllMain(DataView):

    entity_widget_class = Akt
    _entity_mc = BAkt

    _model_class = AktAllModel

    _maintable_text = ["Akt", "Akte", "kein Akt"]
    _delete_window_title = ["Akt löschen", "Akte löschen"]
    _delete_window_text_single = "Soll der ausgewählte Akt " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Akte wirklich gelöscht werden?"]


    _main_table_model_class = AktAllModel

    """verfügbare filter für diese tabelle"""
    _available_filters = 'gs'
    """"""

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.loadData()
        self.setLayer()
        self.setTableView()

        self.updateFooter()

        self.signals()

        print(f'...')

    def initUi(self):
        super().initUi()

        self.title = 'alle Akte'

        self.setStretchMethod(2)

        self.insertFooterLine('Gesamtweidefläche',
                              'ha', 9, 120,
                              0.0001, 4)
        self.insertFooterLine('davon beweidet',
                              'ha', 8, 120,
                              0.0001, 4)
        self.insertFooterLine('im NÖ Alm- und Weidebuch eingetragen',
                              'ha', 7, 120,
                              0.0001, 4)

        self.uiAddDataTbtn.setVisible(False)
        self.uiDeleteDataTbtn.setVisible(False)

    def getMciList(self, session):

        # with db_session_cm() as session:
        stmt = (select(BAkt)
        .options(
            joinedload(BAkt.rel_bearbeitungsstatus)
        )
        .options(
            joinedload(BAkt.rel_gst_zuordnung)
            .joinedload(BGstZuordnung.rel_gst)
            .joinedload(BGst.rel_alm_gst_version)
            .joinedload(BGstVersion.rel_alm_gst_ez)
        )
        .options(
            joinedload(BAkt.rel_gst_zuordnung)
            .joinedload(BGstZuordnung.rel_gst)
            .joinedload(BGst.rel_alm_gst_version)
            .joinedload(BGstVersion.rel_alm_gst_nutzung)
        )
        .options(
            joinedload(BAkt.rel_gst_zuordnung)
            .joinedload(BGstZuordnung.rel_gst)
            .joinedload(BGst.rel_alm_gst_version)
            .joinedload(BGstVersion.rel_cut_koppel_gst)
        )
        .options(
            joinedload(BAkt.rel_abgrenzung)
            .joinedload(BAbgrenzung.rel_komplex)
            .joinedload(BKomplex.rel_koppel)
        )
        )
        mci = session.scalars(stmt).unique().all()

        """test um direkter mit geometrien arbeiten zu können"""
        # # ).where(BAkt.id == 1090)
        # mci = session.scalars(stmt).unique().all()
        # geom = mci[0].rel_gst_zuordnung[3].rel_gst.rel_alm_gst_version[0].geometry
        # g = QgsGeometry()
        # # wkb = geom.hex()
        # # wkb = geom.tobytes()
        # g.fromWkb(geom)
        # print(g.asWkt())
        # print(f'...')
        """"""

        return mci

    def setLayer(self):
        super().setLayer()

        self._gis_layer = AktAllLayer(
            "None",
            "AktAllLay",
            "memory"
        )

        for akt in self._mci_list:

            feat = Feature(self._gis_layer.fields(), self)
            feat.setAttributes([
                akt.id,
                akt.az,
                akt.name,
                0,
                '',
                akt.stz,
                akt.wwp,
                akt.wwp_jahr,
                1,
                2,
                3
            ])

            self._gis_layer.data_provider.addFeatures([feat])

    def getCustomData(self, session):

        custom_data = {}

        status_stmt = select(BBearbeitungsstatus)
        status_mci = session.scalars(status_stmt).all()

        custom_data['status'] = status_mci

        return custom_data

    def updateMainWidget(self):

        self.updateMaintable()

    def setFilterScopeUI(self):
        super().setFilterScopeUI()

        self.uicAktStatusFilterLbl = QLabel(self)
        self.uicAktStatusFilterLbl.setText('Status:')

        self.uicAktStatusFilterCombo = QComboBox(self)

        self.uiTableFilterHLay.insertWidget(2, self.uicAktStatusFilterLbl)
        self.uiTableFilterHLay.insertWidget(3, self.uicAktStatusFilterCombo)

    def setFilterScope(self):
        super().setFilterScope()

        self.setFilterStatus()

    def setFilterStatus(self):

        try:
            self.uicAktStatusFilterCombo.currentTextChanged.disconnect(
                self.filterMaintable)
        except:
            pass
        finally:
            prev_typ = self.uicAktStatusFilterCombo.currentText()
            self.uicAktStatusFilterCombo.clear()

            self.uicAktStatusFilterCombo.addItem('- Alle -')

            status_list = self._custom_data['status']
            status_sorted = sorted(status_list,
                                    key=lambda x: x.sort)

            for status in status_sorted:
                self.uicAktStatusFilterCombo.addItem(str(status.name))

            self.uicAktStatusFilterCombo.setCurrentText(prev_typ)

            self.uicAktStatusFilterCombo.currentTextChanged.connect(
                self.applyFilter)

    def useFilterScope(self, source_row, source_parent):
        super().useFilterScope(source_row, source_parent)

        try:
            """filter status"""
            table_value = self.filter_proxy.sourceModel() \
                .data(self.filter_proxy.sourceModel().index(source_row, 2),
            Qt.DisplayRole)
            if self.uicAktStatusFilterCombo.currentText() != "- Alle -":
                if str(table_value) != self.uicAktStatusFilterCombo.currentText():
                    return False
            """"""
        except:
            print("Filter Error:", sys.exc_info())

    def signals(self):
        super().signals()

        self.uiAddDataTbtn.clicked.connect(self.add_row)
