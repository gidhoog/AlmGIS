from qgis.PyQt.QtCore import Qt, QModelIndex
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QHeaderView
from sqlalchemy import func
from core.data_model import BGstZuordnung, BGst, BGstEz, \
    BGstVersion, BKatGem, BGstAwbStatus, BRechtsgrundlage, BCutKoppelGstAktuell, \
    BKomplex, BAkt, BKoppel, BKomplexVersion
from core.main_dialog import MainDialog
from core.main_table import MainTable, MaintableColumn, \
    MainTableModel, MainTableView
import typing

from core.scopes.gst.gst_zuordnung import GstZuordnung
from core.scopes.gst.gst_zuordnung_dataform import GstZuordnungDataForm


class GstDialog(MainDialog):
    """
    dialog für die anzeige einer grundstückszuordnung
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.enableApply = True

        self.dialog_window_title = 'Grundstückszuordnung'
        self.set_apply_button_text('&Speichern und Schließen')

    def accept(self):
        if self.dialogWidget.acceptEntity():
            super().accept()


class GstZuordnungMainDialog(MainDialog):
    """
    dialog mit dem eine grundstückszuordnung erstellt wird
    """

    def __init__(self, parent=None):
        super(GstZuordnungMainDialog, self).__init__(parent)

        self.parent = parent

        self.dialog_window_title = 'Grundstücke zuordnen'
        self.set_reject_button_text('&Schließen')


class GstMaintable(MainTable):
    """
    grundstückstabelle im akt
    """
    gis_relation = {"gis_id_column": 0,
                    "gis_layer_style_id": 99,
                    "gis_layer_id_column": 'id'}

    _entity_widget = GstZuordnungDataForm
    entity_dialog_class = GstDialog
    data_model_class = BGstZuordnung

    _maintable_text = ["Grundstück", "Grundstücke", "kein Grundstück"]
    _delete_window_title = ["Grundstück löschen", "Grundstücke löschen"]
    _delete_window_text_single = "Soll das ausgewählte Grundstück " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Grundstücke wirklich gelöscht werden?"]
    _delete_text = ["Das Grundstück", "kann nicht gelöscht werden, da es "
                                          "verwendet wird!"]

    _data_view = MainTableView

    gst_zuordnung_wdg_class = GstZuordnung
    gst_zuordnung_dlg_class = GstZuordnungMainDialog

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.linked_gis_widget = self.parent.guiMainGis

    def openGstZuordnung(self):
        """
        öffne den dialog um gst-zuordnungen durchführen zu können
        """

        self.gst_zuordnung_widget = self.gst_zuordnung_wdg_class(
            self, self.parent.entity_id)
        self.zuordnungs_dialog = self.gst_zuordnung_dlg_class(self)
        self.gst_zuordnung_widget.dialog_widget = self.zuordnungs_dialog

        self.zuordnungs_dialog.initDialog(self.gst_zuordnung_widget,
                                          width=1700,
                                          height=700)
        self.gst_zuordnung_widget.initWidget()

        result = self.zuordnungs_dialog.exec()

        if result:
            self.updateMaintable()

    def initUi(self):
        super().initUi()

        self.title = 'zugeordnete Grundstücke'

        self.setStretchMethod(2)

        self.insertFooterLine('im AWB eingetragen und beweidet:',
                              'ha', 7, 120, 0.0001, 4, 5, '==', 'eingetragen')
        self.insertFooterLine('beweidet:',
                              'ha', 7, 120, 0.0001, 4)
        self.insertFooterLine('im AWB eingetrage Grundstücksfläche:',
                              'ha', 9, 120, 0.0001, 4, 5, '==', 'eingetragen')
        self.insertFooterLine('zugeordnete Grundstücksgesamtfläche:',
                              'ha', 9, 120, 0.0001, 4)

        self.uiAddDataTbtn.setToolTip("ordne diesem Akt Grundstücke zu")

    def signals(self):
        super().signals()

        self.uiAddDataTbtn.clicked.connect(self.openGstZuordnung)

    def finalInit(self):
        super().finalInit()

        self.maintable_view.sortByColumn(1, Qt.AscendingOrder)

        """setzt bestimmte spaltenbreiten"""
        self.maintable_view.setColumnWidth(1, 70)
        self.maintable_view.setColumnWidth(2, 50)
        self.maintable_view.setColumnWidth(3, 70)
        self.maintable_view.setColumnWidth(4, 120)
        self.maintable_view.setColumnWidth(5, 120)
        self.maintable_view.setColumnWidth(6, 120)
        self.maintable_view.setColumnWidth(7, 80)
        """"""

        """passe die Zeilenhöhen an den Inhalt an"""
        self.maintable_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        """"""

    def setMaintableColumns(self):
        super().setMaintableColumns()

        self.maintable_columns[0] = MaintableColumn(column_type='int',
                                                    visible=False)
        self.maintable_columns[1] = MaintableColumn(heading='Gst-Nr',
                                                    column_type='str',
                                                    alignment='c')
        self.maintable_columns[2] = MaintableColumn(heading='EZ',
                                                    column_type='str',
                                                    alignment='c')
        self.maintable_columns[3] = MaintableColumn(heading='KG-Nr',
                                                    column_type='int')
        self.maintable_columns[4] = MaintableColumn(heading='KG-Name',
                                                    column_type='str',
                                                    alignment='l')
        self.maintable_columns[5] = MaintableColumn(heading='AWB',
                                                    column_type='str')
        self.maintable_columns[6] = MaintableColumn(heading='Rechtsgrundlage',
                                                    column_type='str',
                                                    alignment='l')
        self.maintable_columns[7] = MaintableColumn(heading='beweidet (ha)',
                                                    column_type='float')
        self.maintable_columns[8] = MaintableColumn(heading='beweidet (%)',
                                                    column_type='float')
        self.maintable_columns[9] = MaintableColumn(heading='Gst-Fläche (ha)',
                                                    column_type='str')
        self.maintable_columns[10] = MaintableColumn(heading='Datenstand',
                                                     column_type='str')

    def getMainQuery(self, session):
        super().getMainQuery(session)

        """subquery um die flaeche des verschnittes von koppel und 
        gst-version zu bekommen"""
        sub_cutarea = session.query(
            BCutKoppelGstAktuell.gst_version_id,
            func.sum(func.ST_Area(BCutKoppelGstAktuell.geometry)).label("bew_area"),
            func.max(BKomplexVersion.jahr)
        )\
            .select_from(BCutKoppelGstAktuell)\
            .join(BKoppel)\
            .join(BKomplexVersion)\
            .join(BKomplex)\
            .join(BAkt)\
            .filter(BAkt.id == self.parent.data_instance.id)\
            .group_by(BCutKoppelGstAktuell.gst_version_id)\
            .subquery()
        """"""

        # sub_test = session.query(
        #     BCutKoppelGstAktuell.gst_version_id,
        #     func.sum(func.ST_Area(BCutKoppelGstAktuell.geometry)).label("bew_area"),
        #     func.max(BKomplexVersion.jahr)
        # )\
        #     .select_from(BCutKoppelGstAktuell)\
        #     .join(BKoppel)\
        #     .join(BKomplexVersion)\
        #     .join(BKomplex)\
        #     .join(BAkt)\
        #     .filter(BAkt.id == self.parent.data_instance.id)\
        #     .group_by(BCutKoppelGstAktuell.gst_version_id)\
        #     .all()

        query = session.query(BGstZuordnung.id,
                              BGst.gst,
                              BGstEz.ez,
                              BGst.kgnr,
                              BKatGem.kgname,
                              BGstAwbStatus.name,
                              BRechtsgrundlage.name,
                              sub_cutarea.c.bew_area,
                              None,  # platzhalter für 'beweidet %'
                              func.ST_Area(BGstVersion.geometry),
                              func.max(BGstEz.datenstand)) \
            .select_from(BGstZuordnung) \
            .join(BGst) \
            .join(BGstVersion) \
            .join(BGstEz) \
            .join(BKatGem) \
            .join(BGstAwbStatus) \
            .join(BRechtsgrundlage) \
            .outerjoin(sub_cutarea, BGstVersion.id == sub_cutarea.c.gst_version_id) \
            .filter(BGstZuordnung.akt_id == self.parent.data_instance.id) \
            .group_by(BGstZuordnung.id)

        return query

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

        return GstModel(self, self.maintable_dataarray)


class GstModel(MainTableModel):

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.BackgroundRole:
            if index.column() == 5:
                val_5 = self.data(self.index(index.row(), index.column()), Qt.DisplayRole)
                if val_5 == 'eingetragen':
                    return QColor(189, 239, 255)
                if val_5 == 'nicht eingetragen':
                    return QColor(234, 216, 54)
                if val_5 == 'gelöscht':
                    return QColor(234, 163, 165)
                if val_5 == 'historisch':
                    return QColor(170, 170, 170)

        if role == Qt.DisplayRole:

            if index.column() == 7:  # beweidet ha
                val = self.data(index, Qt.EditRole)
                if val:
                    try:
                        return '{:.4f}'.format(
                            round(float(val) / 10000, 4)).replace(".", ",")
                    except ValueError:
                        pass
            """errechne den anteil der beweidet wird"""
            if index.column() == 8:  # beweidet %
                bew_val = self.data(self.index(index.row(), 7), Qt.EditRole)
                total_val = self.data(self.index(index.row(), 9), Qt.EditRole)
                if not bew_val:
                    return ''
                else:
                    val = (bew_val / total_val) * 100
                    try:
                        return '{:.2f}'.format(
                            round(float(val), 2)).replace(".", ",")
                    except ValueError:
                        pass
            """"""

            if index.column() == 9:  # Gst-Fläche
                val = self.data(index, Qt.EditRole)
                if val:
                    try:
                        return '{:.4f}'.format(
                            round(float(val) / 10000, 4)).replace(".", ",")
                    except ValueError:
                        pass

        return super().data(index, role)
