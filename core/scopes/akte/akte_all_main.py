import sys
from _operator import attrgetter

from qgis.PyQt.QtCore import Qt, QModelIndex, QAbstractTableModel
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QLabel, QComboBox

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from core import db_session_cm
from core.data_model import BAkt, BKomplex, BGstZuordnung, BGst, BGstVersion, \
    BGstEz, BCutKoppelGstAktuell, BBearbeitungsstatus, BAbgrenzung
from core.entity import EntityDialog
from core.data_view import DataView, TableModel, TableView
from core.main_widget import MainWidget
from core.scopes.akte.akt import Akt


# class AkteAllEntityDialog(EntityDialog):
#
#     def __init__(self, parent=None):
#         super(self.__class__, self).__init__(parent)
#
#         self.set_apply_button_text('&Speichern und Schließen_Akt')
#
#     def accept(self):
#         # super().accept()
#
#         if self.dialogWidget.acceptEntity():
#
#             self.parent.updateMaintableNew()
#         #
#         #     self.parent._main_table_mci.clear()
#         #
#         #     for inst in self.parent.getDataMci():
#         #         self.parent._main_table_mci.append(inst)
#         #
#         #     self.parent.data_view.model().layoutChanged.emit()
#
#
#
#         QDialog.accept(self)


class AkteAllMainWidget(MainWidget):
    """
    MainWidget für die Darstellung eines DataView's mit allen Akten
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.uiTitleLbl.setText('alle Akte')

        self.akt_all_table = AkteAllMain()

    def initMainWidget(self):
        super().initMainWidget()

        self.uiMainVLay.addWidget(self.akt_all_table)
        self.akt_all_table.initMaintable()


class AktAllModel(TableModel):
# class AktAllModel(QAbstractTableModel):

    def __init__(self, parent, mci_list=[]):
        super(self.__class__, self).__init__(parent, mci_list=mci_list)

        # self.parent = parent
        # self.mci_list = mci_list

        self.header = ['AZ',
                       'Name',
                       'Status',
                       'Stz',
                       'Anmerkung',
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

            if index.column() in [5, 6, 7]:

                return Qt.AlignRight | Qt.AlignVCenter

            if index.column() in [0, 2, 3]:

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
            #     return self.mci_list[row].az

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

        if index.column() == 6:

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

        if index.column() == 7:

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




    # def data(self, index, role=None):
    #
    #     if role == Qt.DisplayRole:
    #
    #         if index.column() == 7:  # purchase_value
    #             val = self.data(index, Qt.EditRole)
    #             if val:
    #                 try:
    #                     return '{:.4f}'.format(
    #                         round(float(val) / 10000, 4)).replace(".", ",")
    #                 except ValueError:
    #                     pass
    #         if index.column() == 8:  # purchase_value
    #             val = self.data(index, Qt.EditRole)
    #             if val:
    #                 try:
    #                     return '{:.4f}'.format(
    #                         round(float(val) / 10000, 4)).replace(".", ",")
    #                 except ValueError:
    #                     pass
    #         if index.column() == 9:  # purchase_value
    #             val = self.data(index, Qt.EditRole)
    #             if val:
    #                 try:
    #                     return '{:.4f}'.format(
    #                         round(float(val) / 10000, 4)).replace(".", ",")
    #                 except ValueError:
    #                     pass
    #
    #     return super().data(index, role)

    # def rowCount(self, parent: QModelIndex = ...):
    #     """
    #     definiere die zeilenanzahl
    #     """
    #
    #     if self.mci_list:
    #         return len(self.mci_list)
    #     else:
    #         return 0
    #
    # def columnCount(self, parent: QModelIndex = ...):
    #     """
    #     definiere die spaltenanzahl
    #     """
    #     return len(self.header)
    #
    # def headerData(self, column, orientation, role=None):
    #     """
    #     wenn individuelle überschriften gesetzt sind (in 'maintable_columns')
    #     dann nehme diese
    #     """
    #     super().headerData(column, orientation, role)
    #
    #     if self.header:
    #         if role == Qt.DisplayRole and orientation == Qt.Horizontal:
    #
    #             return self.header[column]
    #     # else:
    #     #     return super().headerData(column, orientation, role)


class AkteAllMain(DataView):

    entity_widget_class = Akt

    _maintable_text = ["Akt", "Akte", "kein Akt"]
    _delete_window_title = ["Akt löschen", "Akte löschen"]
    _delete_window_text_single = "Soll der ausgewählte Akt " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Akte wirklich gelöscht werden?"]

    # _data_view = TableView

    _main_table_model_class = AktAllModel
    # entity_dialog_class = AkteAllEntityDialog

    """verfügbare filter für diese tabelle"""
    _available_filters = 'gs'
    """"""

    # _main_table_mci = []

    # @property  # getter
    # def main_table_mci(self):
    #
    #     with db_session_cm() as session:
    #         stmt = select(BAkt).options(
    #             joinedload(BAkt.rel_bearbeitungsstatus)
    #         )
    #
    #         self._main_table_mci = session.scalars(stmt).unique().all()
    #
    #     return self._main_table_mci

    # @main_table_mci.setter
    # def main_table_mci(self, value):
    #
    #     self._main_table_mci = value

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        # self.data_model_class = BAkt

        # with db_session_cm() as session:
        #
        #     test_inst = session.get(BGst, 12499)
        #
        #     print(f'test_inst: {test_inst}')
        #
        #     area = func.ST_Area(test_inst.rel_alm_gst_version[0].geometry)
        #
        #     print(f'area: {area}')
        #     print('........')
        #
        #     test_02_inst = select(BGst, BGstVersion.geometry.ST_Area()).join(BGstVersion).where(BGst.id == 12499)
        #     test_03_inst = session.scalars(test_02_inst)
        #
        #     print(f'----------------------')

    # def initMaintable(self, session=None, di_list=[]):
    #     # super().initMaintable(session, di_list)
    #
    #     self.initUi()
    #
    #     # with db_session_cm() as session:
    #     #
    #     #     stmt = select(BAkt).options(
    #     #         joinedload(BAkt.rel_bearbeitungsstatus)
    #     #     )
    #     #
    #     #     aaa = session.scalars(stmt).unique().all()
    #
    #     self.data_view_model = self.main_table_model_class(
    #         self,
    #         self.main_table_mci)
    #
    #     self.filter_proxy.setSourceModel(self.data_view_model)
    #     self.data_view.setModel(self.filter_proxy)
    #
    #     self.updateFooter()
    #     self.setFilter()
    #
    #     self.setAddEntityMenu()
    #     self.setDataViewLayout()
    #
    #     self.signals()
    #
    #     self.finalInit()

    def initUi(self):
        super().initUi()

        self.title = 'alle Akte'

        self.setStretchMethod(2)

        self.insertFooterLine('Gesamtweidefläche',
                              'ha', 7, 120,
                              0.0001, 4)
        self.insertFooterLine('davon beweidet',
                              'ha', 6, 120,
                              0.0001, 4)
        self.insertFooterLine('im NÖ Alm- und Weidebuch eingetragen',
                              'ha', 5, 120,
                              0.0001, 4)

        self.uiAddDataTbtn.setVisible(False)
        self.uiDeleteDataTbtn.setVisible(False)

    def getDataMci(self, session):

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

        return mci

    def getCostumMci(self, session):

        status_stmt = select(BBearbeitungsstatus)
        status_mci = session.scalars(status_stmt).all()

        self._costum_mci['status'] = status_mci

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

        # with db_session_cm() as session:
        #     item_query = session.query(BGstAwbStatus.name).distinct()

        try:
            self.uicAktStatusFilterCombo.currentTextChanged.disconnect(
                self.filterMaintable)
        except:
            pass
        finally:
            prev_typ = self.uicAktStatusFilterCombo.currentText()
            self.uicAktStatusFilterCombo.clear()

            self.uicAktStatusFilterCombo.addItem('- Alle -')

            status_list = self._costum_mci['status']
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


    # def setMaintableColumns(self):
    #     super().setMaintableColumns()
    #
    #     self.maintable_columns[0] = MaintableColumn(column_type='int',
    #                                                 visible=False)
    #     self.maintable_columns[1] = MaintableColumn(heading='AZ',
    #                                                 column_type='str',
    #                                                 alignment='c')
    #     self.maintable_columns[2] = MaintableColumn(heading='Name',
    #                                                 column_type='str',
    #                                                 alignment='l')
    #     self.maintable_columns[3] = MaintableColumn(heading='Alias',
    #                                                 column_type='str',
    #                                                 alignment='l')
    #
    #     # self.maintable_columns[0] = MaintableColumn(column_type='int',
    #     #                                             visible=False)
    #     # self.maintable_columns[1] = MaintableColumn(heading='AZ',
    #     #                                             column_type='str',
    #     #                                             alignment='c')
    #     # self.maintable_columns[2] = MaintableColumn(heading='Name',
    #     #                                             column_type='str',
    #     #                                             alignment='l')
    #     # self.maintable_columns[3] = MaintableColumn(heading='Alias',
    #     #                                             column_type='str',
    #     #                                             alignment='l')
    #     # self.maintable_columns[4] = MaintableColumn(heading='Status',
    #     #                                             column_type='str')
    #     # self.maintable_columns[5] = MaintableColumn(heading='AlmBNR',
    #     #                                             column_type='int')
    #     # self.maintable_columns[6] = MaintableColumn(heading='Stammzahl',
    #     #                                             column_type='str',
    #     #                                             alignment='c')
    #     # self.maintable_columns[7] = MaintableColumn(heading='Weidefläche (ha)',
    #     #                                             column_type='float')
    #     # self.maintable_columns[8] = MaintableColumn(heading='im AW-Buch (ha)',
    #     #                                             column_type='float')
    #     # self.maintable_columns[9] = MaintableColumn(heading='davon bew. (ha)',
    #     #                                             column_type='float')
    #
    # def getMainQuery(self, session=None):
    #
    #     query2 = session.execute(select(BAkt.id,
    #                                     BAkt.az,
    #                                     BAkt.name,
    #                                     BAkt.alias))
    #
    #     # akt_inst = query2.all()
    #     # print(f'###')
    #
    #     # """subquery to get the area for the intersected and last gst"""
    #     # sub_komplex_area = session.query(
    #     #                     BAkt.id,
    #     #                     func.sum(func.ST_Area(BKomplex.geometry))
    #     #                     .label("komplex_area"))\
    #     #     .select_from(BAkt) \
    #     #     .join(BKomplex) \
    #     #     .group_by(BAkt.id)\
    #     #     .subquery()
    #     # """"""
    #     #
    #     # """die aktuellsten gst-versionen je akt"""
    #     # sub_gst_registered = session.query(BAkt.id,
    #     #                                    func.ST_Area(BGstVersion.geometry)
    #     #                                    .label("gst_area"),
    #     #                                    func.max(BGstEz.datenstand),
    #     #                                    BGstVersion.ez_id) \
    #     #     .select_from(BAkt) \
    #     #     .join(BGstZuordnung) \
    #     #     .join(BGst)\
    #     #     .join(BGstVersion)\
    #     #     .join(BGstEz) \
    #     #     .filter(BGstZuordnung.awb_status_id == 1)\
    #     #     .group_by(BGstVersion.gst_id)\
    #     #     .subquery()
    #     # """"""
    #     #
    #     # """die beweidete fläche je akt die im aw-buch eingetragen ist"""
    #     # sub_awb_beweidet = session.query(BAkt.id,
    #     #                                  func.sum(func.ST_Area(
    #     #                                      BCutKoppelGstAktuell.geometry))
    #     #                                  .label("bew_area")) \
    #     #     .select_from(BAkt) \
    #     #     .join(BGstZuordnung) \
    #     #     .join(BGst)\
    #     #     .join(BGstVersion)\
    #     #     .join(BCutKoppelGstAktuell) \
    #     #     .filter(BGstZuordnung.awb_status_id == 1) \
    #     #     .group_by(BAkt.id) \
    #     #     .subquery()
    #     # """"""
    #     #
    #     # query2 = session.query(BAkt.id,
    #     #                        BAkt.az,
    #     #                        BAkt.name,
    #     #                        BAkt.alias,
    #     #                        BBearbeitungsstatus.name,
    #     #                        BAkt.alm_bnr,
    #     #                        BAkt.stz,
    #     #                        sub_komplex_area.c.komplex_area,
    #     #                        func.sum(sub_gst_registered.c.gst_area),
    #     #                        sub_awb_beweidet.c.bew_area) \
    #     #     .select_from(BAkt) \
    #     #     .join(BBearbeitungsstatus) \
    #     #     .outerjoin(sub_komplex_area, BAkt.id == sub_komplex_area.c.id) \
    #     #     .outerjoin(sub_gst_registered, BAkt.id == sub_gst_registered.c.id)\
    #     #     .outerjoin(sub_awb_beweidet, BAkt.id == sub_awb_beweidet.c.id)\
    #     #     .group_by(BAkt.id)
    #
    #     return query2
    #
    # def setMainTableModel(self):
    #     super().setMainTableModel()
    #
    #     return AktAllModel(self, self.maintable_dataarray)

    def signals(self):
        super().signals()

        self.uiAddDataTbtn.clicked.connect(self.add_row)


# # class AktAllModel(TableModel):
# class AktAllModel(QAbstractTableModel):
#
#     def __init__(self, parent, mci_list=None):
#         super(self.__class__, self).__init__()
#
#         self.parent = parent
#         self.mci_list = mci_list
#
#         self.header = ['AZ',
#                        'Name',
#                        'Status']
#
#     def data(self, index: QModelIndex, role: int = ...):
#
#         """
#         erzeuge ein basis-model
#         """
#         row = index.row()
#         col = index.column()
#
#         if role == Qt.TextAlignmentRole:
#
#             # if index.column() in [2, 6, 7, 8, 9]:
#             #
#             #     return Qt.AlignRight | Qt.AlignVCenter
#
#             if index.column() in [0]:
#
#                 return Qt.AlignHCenter | Qt.AlignVCenter
#
#         if index.column() == 0:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].az
#
#         if index.column() == 1:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].name
#
#         if index.column() == 2:
#
#             if self.mci_list[row].rel_bearbeitungsstatus is not None:
#
#                 if role == Qt.DisplayRole:
#                     return self.mci_list[row].rel_bearbeitungsstatus.name
#
#     # def data(self, index, role=None):
#     #
#     #     if role == Qt.DisplayRole:
#     #
#     #         if index.column() == 7:  # purchase_value
#     #             val = self.data(index, Qt.EditRole)
#     #             if val:
#     #                 try:
#     #                     return '{:.4f}'.format(
#     #                         round(float(val) / 10000, 4)).replace(".", ",")
#     #                 except ValueError:
#     #                     pass
#     #         if index.column() == 8:  # purchase_value
#     #             val = self.data(index, Qt.EditRole)
#     #             if val:
#     #                 try:
#     #                     return '{:.4f}'.format(
#     #                         round(float(val) / 10000, 4)).replace(".", ",")
#     #                 except ValueError:
#     #                     pass
#     #         if index.column() == 9:  # purchase_value
#     #             val = self.data(index, Qt.EditRole)
#     #             if val:
#     #                 try:
#     #                     return '{:.4f}'.format(
#     #                         round(float(val) / 10000, 4)).replace(".", ",")
#     #                 except ValueError:
#     #                     pass
#     #
#     #     return super().data(index, role)
#
#     def rowCount(self, parent: QModelIndex = ...):
#         """
#         definiere die zeilenanzahl
#         """
#
#         if self.mci_list:
#             return len(self.mci_list)
#         else:
#             return 0
#
#     def columnCount(self, parent: QModelIndex = ...):
#         """
#         definiere die spaltenanzahl
#         """
#         return len(self.header)
#
#     def headerData(self, column, orientation, role=None):
#         """
#         wenn individuelle überschriften gesetzt sind (in 'maintable_columns')
#         dann nehme diese
#         """
#         super().headerData(column, orientation, role)
#
#         if self.header:
#             if role == Qt.DisplayRole and orientation == Qt.Horizontal:
#
#                 return self.header[column]
#         # else:
#         #     return super().headerData(column, orientation, role)
