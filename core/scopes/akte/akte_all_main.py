from qgis.PyQt.QtCore import Qt, QModelIndex, QAbstractTableModel
from qgis.PyQt.QtGui import QColor
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from core import db_session_cm
from core.data_model import BAkt, BKomplex, BGstZuordnung, BGst, BGstVersion, \
    BGstEz, BCutKoppelGstAktuell, BBearbeitungsstatus
from core.main_table import MainTable, MaintableColumn, MainTableModel, \
    MainTableView
from core.main_widget import MainWidget
from core.scopes.akte.akt import Akt


class AkteAllMainWidget(MainWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.uiTitleLbl.setText('alle Akte')

        self.akt_all_table = AkteAllMain()

    def initMainWidget(self):
        super().initMainWidget()

        self.uiMainVLay.addWidget(self.akt_all_table)
        self.akt_all_table.initMaintable()


# class AktAllModel(MainTableModel):
class AktAllModel(QAbstractTableModel):

    def __init__(self, parent, mci_list=None):
        super(self.__class__, self).__init__()

        self.parent = parent
        self.mci_list = mci_list

        self.header = ['AZ',
                       'Name',
                       'Status',
                       'Stz',
                       'Anmerkung']

    def data(self, index: QModelIndex, role: int = ...):

        """
        erzeuge ein basis-model
        """
        row = index.row()
        col = index.column()

        if role == Qt.TextAlignmentRole:

            # if index.column() in [2, 6, 7, 8, 9]:
            #
            #     return Qt.AlignRight | Qt.AlignVCenter

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

    def rowCount(self, parent: QModelIndex = ...):
        """
        definiere die zeilenanzahl
        """

        if self.mci_list:
            return len(self.mci_list)
        else:
            return 0

    def columnCount(self, parent: QModelIndex = ...):
        """
        definiere die spaltenanzahl
        """
        return len(self.header)

    def headerData(self, column, orientation, role=None):
        """
        wenn individuelle überschriften gesetzt sind (in 'maintable_columns')
        dann nehme diese
        """
        super().headerData(column, orientation, role)

        if self.header:
            if role == Qt.DisplayRole and orientation == Qt.Horizontal:

                return self.header[column]
        # else:
        #     return super().headerData(column, orientation, role)


class AkteAllMain(MainTable):

    _entity_widget = Akt

    _maintable_text = ["Akt", "Akte", "kein Akt"]
    _delete_window_title = ["Akt löschen", "Akte löschen"]
    _delete_window_text_single = "Soll der ausgewählte Akt " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Akte wirklich gelöscht werden?"]

    _data_view = MainTableView

    _main_table_model_class = AktAllModel

    # _main_table_mci = []

    @property  # getter
    def main_table_mci(self):

        with db_session_cm() as session:
            stmt = select(BAkt).options(
                joinedload(BAkt.rel_bearbeitungsstatus)
            )

            self._main_table_mci = session.scalars(stmt).unique().all()

        return self._main_table_mci

    # @main_table_mci.setter
    # def main_table_mci(self, value):
    #
    #     self._main_table_mci = value

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.data_model_class = BAkt

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
    #     self.main_table_model = self.main_table_model_class(
    #         self,
    #         self.main_table_mci)
    #
    #     self.filter_proxy.setSourceModel(self.main_table_model)
    #     self.maintable_view.setModel(self.filter_proxy)
    #
    #     self.updateFooter()
    #     self.setFilter()
    #
    #     self.setAddEntityMenu()
    #     self.setMaintableLayout()
    #
    #     self.signals()
    #
    #     self.finalInit()

    def initUi(self):
        super().initUi()

        self.title = 'alle Akte'

        self.setStretchMethod(2)

        # self.insertFooterLine('davon beweidet', 'ha', 9, 120, 0.0001, 4)
        # self.insertFooterLine('im NÖ Alm- und Weidebuch eingetragen',
        #                       'ha', 8, 120, 0.0001, 4)
        # self.insertFooterLine('Gesamtweidefläche', 'ha', 7, 120, 0.0001, 4)

        self.uiAddDataTbtn.setVisible(False)
        self.uiDeleteDataTbtn.setVisible(False)

    def updateMainWidget(self):

        self.updateMaintable()

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


# # class AktAllModel(MainTableModel):
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
