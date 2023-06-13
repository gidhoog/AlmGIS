from PyQt5.QtCore import Qt
from sqlalchemy import func, select
from core.data_model import BAkt, BKomplex, BGstZuordnung, BGst, BGstVersion, \
    BGstEz, BCutKomplexGst, BBearbeitungsstatus
from core.main_table import MainTable, MaintableColumn, MainTableModel, \
    MainTableView
from core.main_widget import MainWidget
from core.scopes.akte.akt import Akt


class AkteAllMain(MainTable, MainWidget):

    _entity_widget = Akt

    _maintable_text = ["Akt", "Akte", "kein Akt"]
    _delete_window_title = ["Akt löschen", "Akte löschen"]
    _delete_window_text_single = "Soll der ausgewählte Akt " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Akte wirklich gelöscht werden?"]

    _data_view = MainTableView

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.data_model_class = BAkt

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

    def setMaintableColumns(self):
        super().setMaintableColumns()

        self.maintable_columns[0] = MaintableColumn(column_type='int',
                                                    visible=False)
        self.maintable_columns[1] = MaintableColumn(heading='AZ',
                                                    column_type='str',
                                                    alignment='c')
        self.maintable_columns[2] = MaintableColumn(heading='Name',
                                                    column_type='str',
                                                    alignment='l')
        self.maintable_columns[3] = MaintableColumn(heading='Alias',
                                                    column_type='str',
                                                    alignment='l')

        # self.maintable_columns[0] = MaintableColumn(column_type='int',
        #                                             visible=False)
        # self.maintable_columns[1] = MaintableColumn(heading='AZ',
        #                                             column_type='str',
        #                                             alignment='c')
        # self.maintable_columns[2] = MaintableColumn(heading='Name',
        #                                             column_type='str',
        #                                             alignment='l')
        # self.maintable_columns[3] = MaintableColumn(heading='Alias',
        #                                             column_type='str',
        #                                             alignment='l')
        # self.maintable_columns[4] = MaintableColumn(heading='Status',
        #                                             column_type='str')
        # self.maintable_columns[5] = MaintableColumn(heading='AlmBNR',
        #                                             column_type='int')
        # self.maintable_columns[6] = MaintableColumn(heading='Stammzahl',
        #                                             column_type='str',
        #                                             alignment='c')
        # self.maintable_columns[7] = MaintableColumn(heading='Weidefläche (ha)',
        #                                             column_type='float')
        # self.maintable_columns[8] = MaintableColumn(heading='im AW-Buch (ha)',
        #                                             column_type='float')
        # self.maintable_columns[9] = MaintableColumn(heading='davon bew. (ha)',
        #                                             column_type='float')

    def getMainQuery(self, session=None):

        query2 = session.execute(select(BAkt.id,
                                        BAkt.az,
                                        BAkt.name,
                                        BAkt.alias))

        # """subquery to get the area for the intersected and last gst"""
        # sub_komplex_area = session.query(
        #                     BAkt.id,
        #                     func.sum(func.ST_Area(BKomplex.geometry))
        #                     .label("komplex_area"))\
        #     .select_from(BAkt) \
        #     .join(BKomplex) \
        #     .group_by(BAkt.id)\
        #     .subquery()
        # """"""
        #
        # """die aktuellsten gst-versionen je akt"""
        # sub_gst_registered = session.query(BAkt.id,
        #                                    func.ST_Area(BGstVersion.geometry)
        #                                    .label("gst_area"),
        #                                    func.max(BGstEz.datenstand),
        #                                    BGstVersion.ez_id) \
        #     .select_from(BAkt) \
        #     .join(BGstZuordnung) \
        #     .join(BGst)\
        #     .join(BGstVersion)\
        #     .join(BGstEz) \
        #     .filter(BGstZuordnung.awb_status_id == 1)\
        #     .group_by(BGstVersion.gst_id)\
        #     .subquery()
        # """"""
        #
        # """die beweidete fläche je akt die im aw-buch eingetragen ist"""
        # sub_awb_beweidet = session.query(BAkt.id,
        #                                  func.sum(func.ST_Area(
        #                                      BCutKomplexGst.geometry))
        #                                  .label("bew_area")) \
        #     .select_from(BAkt) \
        #     .join(BGstZuordnung) \
        #     .join(BGst)\
        #     .join(BGstVersion)\
        #     .join(BCutKomplexGst) \
        #     .filter(BGstZuordnung.awb_status_id == 1) \
        #     .group_by(BAkt.id) \
        #     .subquery()
        # """"""
        #
        # query2 = session.query(BAkt.id,
        #                        BAkt.az,
        #                        BAkt.name,
        #                        BAkt.alias,
        #                        BBearbeitungsstatus.name,
        #                        BAkt.alm_bnr,
        #                        BAkt.stz,
        #                        sub_komplex_area.c.komplex_area,
        #                        func.sum(sub_gst_registered.c.gst_area),
        #                        sub_awb_beweidet.c.bew_area) \
        #     .select_from(BAkt) \
        #     .join(BBearbeitungsstatus) \
        #     .outerjoin(sub_komplex_area, BAkt.id == sub_komplex_area.c.id) \
        #     .outerjoin(sub_gst_registered, BAkt.id == sub_gst_registered.c.id)\
        #     .outerjoin(sub_awb_beweidet, BAkt.id == sub_awb_beweidet.c.id)\
        #     .group_by(BAkt.id)

        return query2

    def setMainTableModel(self):
        super().setMainTableModel()

        return AktAllModel(self, self.maintable_dataarray)

    def signals(self):
        super().signals()

        self.uiAddDataTbtn.clicked.connect(self.add_row)


class AktAllModel(MainTableModel):

    def __init__(self, parent, data_array=None):
        super(self.__class__, self).__init__(parent, data_array)

        self.parent = parent

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
