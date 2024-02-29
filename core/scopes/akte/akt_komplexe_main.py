from qgis.PyQt.QtCore import Qt, QModelIndex
from qgis.PyQt.QtWidgets import QHeaderView
from sqlalchemy import func, and_, select

from core.data_model import BGstZuordnung, BGst, BGstEz, \
    BGstVersion, BKomplex, \
    BCutKoppelGstAktuell
from core.main_dialog import MainDialog
from core.data_view import DataView, TableModel, TableView

from core.scopes.komplex.komplex_dataform import KomplexDataForm


class KomplexDialog(MainDialog):

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent
        self.enableApply = True

        self.dialog_window_title = 'Komplex'
        self.set_apply_button_text('&Speichern und Schließen')

    def accept(self):

        if self.dialogWidget.acceptEntity():
            super().accept()


class KomplexMaintable(DataView):
    """
    tabelle mit den weidekomplexen im akt
    """
    gis_relation = {"gis_id_column": 0,
                    "gis_layer_style_id": 104,
                    "gis_layer_id_column": 'id'}

    _entity_widget = KomplexDataForm
    entity_dialog_class = KomplexDialog
    data_model_class = BKomplex


    _maintable_text = ["Komplex", "Komplexe", "kein Komplex"]
    _delete_window_title = ["Komplex löschen", "Komplexe löschen"]
    _delete_window_text_single = "Soll der ausgewählte Komplex " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Komplexe wirklich gelöscht werden?"]
    _delete_text = ["Der Komplex", "kann nicht gelöscht werden, da er "
                                          "verwendet wird!"]

    _data_view = TableView

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.linked_gis_widget = self.parent.guiMainGis

    def initUi(self):
        super().initUi()

        self.title = 'Weidekomplexe'

        self.uiAddDataTbtn.setVisible(False)

        self.setStretchMethod(2)

        # self.insertFooterLine('davon im AWB eingetragen:',
        #                       'ha', 5, 120, 0.0001, 4)
        # self.insertFooterLine('Gesamtfläche:',
        #                       'ha', 7, 120, 0.0001, 4)

    def finalInit(self):
        super().finalInit()

        self.data_view.sortByColumn(1, Qt.AscendingOrder)

        """setzt bestimmte spaltenbreiten"""
        self.data_view.setColumnWidth(1, 70)
        self.data_view.setColumnWidth(2, 150)
        self.data_view.setColumnWidth(3, 70)
        self.data_view.setColumnWidth(4, 120)
        self.data_view.setColumnWidth(5, 90)
        self.data_view.setColumnWidth(6, 90)
        self.data_view.setColumnWidth(7, 90)
        """"""

        """passe die Zeilenhöhen an den Inhalt an"""
        self.data_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        """"""

    # def getRowInstance(self, index, session):
    #
    #     inst = session.query(self.data_model_class) \
    #         .filter(self.data_model_class.id ==
    #                 self.maintable_dataarray[index.row()][0]) \
    #         .first()
    #
    #     return inst

    def setMaintableColumns(self):
        super().setMaintableColumns()

        self.maintable_columns[0] = MaintableColumn(heading='id',
                                                    column_type='int',
                                                    alignment='c')
        self.maintable_columns[1] = MaintableColumn(heading='Name',
                                                    column_type='str',
                                                    alignment='l')

        # self.maintable_columns[0] = MaintableColumn(column_type='int',
        #                                             visible=False)
        # self.maintable_columns[1] = MaintableColumn(heading='Nr',
        #                                             column_type='int',
        #                                             alignment='c')
        # self.maintable_columns[2] = MaintableColumn(heading='Name',
        #                                             column_type='str',
        #                                             alignment='l')
        # self.maintable_columns[3] = MaintableColumn(heading='Jahr',
        #                                             column_type='int',
        #                                             alignment='c')
        # self.maintable_columns[4] = MaintableColumn(heading='Bearbeiter',
        #                                             column_type='str',
        #                                             alignment='l')
        # self.maintable_columns[5] = MaintableColumn(heading='AW-Buch (ha)',
        #                                             column_type='str')
        # self.maintable_columns[6] = MaintableColumn(heading='AW-Buch (%)',
        #                                             column_type='float')
        # self.maintable_columns[7] = MaintableColumn(heading='Fläche (ha)',
        #                                             column_type='str')

    def getMainQuery(self, session=None):
        super().getMainQuery(session)

        # query = session.scalars(select(BKomplex)
        #                         .where(BKomplex.akt_id == self.parent._entity_mci.id))

        query = session.execute(select(BKomplex.id, BKomplex.name)
                                .where(BKomplex.akt_id == self.parent._entity_mci.id))

        test_inst = query.all()

        print(f'##')

        # query = session.query(BKomplex.id,
        #                       BKomplex.nr,
        #                       BKomplex.name,
        #                       BKomplex.jahr,
        #                       BKomplex.bearbeiter,
        #                       func.sum(func.ST_Area(BCutKoppelGstAktuell.geometry)),
        #                       None,  # placeholder for %
        #                       func.ST_Area(BKomplex.geometry)) \
        #     .select_from(BKomplex) \
        #     .outerjoin(BCutKoppelGstAktuell) \
        #     .outerjoin(BGstVersion) \
        #     .outerjoin(BGstEz) \
        #     .outerjoin(BGst) \
        #     .outerjoin(BGstZuordnung,
        #                and_((BGstZuordnung.awb_status_id == 1),
        #                     (BGst.id == BGstZuordnung.gst_id))) \
        #     .filter(BKomplex.akt_id == self.parent._entity_mci.id) \
        #     .group_by(BKomplex.id)

        return test_inst

    def loadDataBySession(self):
        """
        frage die daten mittels der maintable_session aus der datenbank ab;
        verwende dafür main_query
        """

        self.maintable_dataarray = self.getMainQuery(self.maintable_session)

        # if self.main_query:
        #     self.maintable_dataarray = self.main_query.all()

        self.main_table_model = self.setMainTableModel()

    def updateMaintable(self):
        super().updateMaintable()

    def getDeleteInfo(self, index=None):
        super().getDeleteInfo(index)

        del_info = self.filter_proxy.data(
            self.filter_proxy.index(
                index.row(), 1))

        return del_info

    def setMainTableModel(self):
        super().setMainTableModel()

        return KomplexModel(self, self.maintable_dataarray)


class KomplexModel(TableModel):

    def data(self, index: QModelIndex, role: int = ...):

        # val = self.data(index, Qt.EditRole)
        #
        # if role == Qt.DisplayRole:
        #
        #     if index.column() == 0:
        #         return val.id
        #
        #     if index.column() == 1:
        #         return val.name

            # if index.column() == 5:  # AW-Buch
            #     val = self.data(index, Qt.EditRole)
            #     if val:
            #         try:
            #             return '{:.4f}'.format(
            #                 round(float(val) / 10000, 4)).replace(".", ",")
            #         except ValueError:
            #             pass
            #
            # if index.column() == 6:  # AW-Buch %
            #     gst_val = self.data(self.index(index.row(), 5), Qt.EditRole)
            #     total_val = self.data(self.index(index.row(), 7), Qt.EditRole)
            #     if not gst_val:
            #         return ''
            #     else:
            #         val = (gst_val / total_val) * 100
            #         try:
            #             return '{:.2f}'.format(
            #                 round(float(val), 2)).replace(".", ",")
            #         except ValueError:
            #             pass
            #
            # if index.column() == 7:  # Komplexfläche
            #     val = self.data(index, Qt.EditRole)
            #     if val:
            #         try:
            #             return '{:.4f}'.format(
            #                 round(float(val) / 10000, 4)).replace(".", ",")
            #         except ValueError:
            #             pass

        return super().data(index, role)
