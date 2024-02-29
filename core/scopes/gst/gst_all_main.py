import sys

from qgis.PyQt.QtCore import Qt, QModelIndex
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QLabel, QComboBox
from sqlalchemy import func

from core import db_session_cm
from core.data_model import BGstZuordnung, BGst, BGstEz, \
    BGstVersion, BKatGem, BGstAwbStatus, BRechtsgrundlage, BCutKoppelGstAktuell, \
    BKomplex, BAkt, BKoppel
from core.data_view import DataView, TableModel, TableView
import typing

from core.main_widget import MainWidget


class GstAllMain(DataView, MainWidget):
    """
    alle grundstücke die einem akt zugeordnet sind
    """

    data_model_class = BGstZuordnung

    available_filters = 'gs'

    _maintable_text = ["Grundstück", "Grundstücke", "kein Grundstück"]

    _data_view = TableView

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.parent = parent

    def initUi(self):
        super().initUi()

        self.title = 'alle zugeordneten Grundstücke'

        self.setStretchMethod(2)

        self.insertFooterLine('davon beweidet:',
                              'ha', 8, 120, 0.0001, 4, 6, '==', 'eingetragen')
        self.insertFooterLine('davon im AWB eingetragen:',
                              'ha', 10, 120, 0.0001, 4, 6, '==', 'eingetragen')
        self.insertFooterLine('zugeordnete Grundstücksgesamtfläche:',
                              'ha', 10, 120, 0.0001, 4)

        self.uiAddDataTbtn.setVisible(False)
        self.uiEditDataTbtn.setVisible(False)
        self.uiDeleteDataTbtn.setVisible(False)

    def signals(self):
        super().signals()

        self.data_view.doubleClicked.disconnect(self.edit_row)

    def finalInit(self):
        super().finalInit()

        self.data_view.sortByColumn(1, Qt.AscendingOrder)

        """setzt bestimmte spaltenbreiten"""
        self.data_view.setColumnWidth(1, 200)
        self.data_view.setColumnWidth(2, 50)
        self.data_view.setColumnWidth(3, 70)
        self.data_view.setColumnWidth(4, 50)
        self.data_view.setColumnWidth(5, 120)
        self.data_view.setColumnWidth(6, 100)
        self.data_view.setColumnWidth(7, 120)
        """"""

        self.updateMaintable()

    def setMaintableColumns(self):
        super().setMaintableColumns()

        self.maintable_columns[0] = MaintableColumn(column_type='int',
                                                    visible=False)
        self.maintable_columns[1] = MaintableColumn(heading='Akt',
                                                    column_type='str',
                                                    alignment='l')
        self.maintable_columns[2] = MaintableColumn(heading='Gst-Nr',
                                                    column_type='str',
                                                    alignment='c')
        self.maintable_columns[3] = MaintableColumn(heading='EZ',
                                                    column_type='str',
                                                    alignment='c')
        self.maintable_columns[4] = MaintableColumn(heading='KG-Nr',
                                                    column_type='int')
        self.maintable_columns[5] = MaintableColumn(heading='KG-Name',
                                                    column_type='str',
                                                    alignment='l')
        self.maintable_columns[6] = MaintableColumn(heading='AW-Buch',
                                                    column_type='str')
        self.maintable_columns[7] = MaintableColumn(heading='Rechtsgrundlage',
                                                    column_type='str',
                                                    alignment='l')
        self.maintable_columns[8] = MaintableColumn(heading='beweidet (ha)',
                                                    column_type='float')
        self.maintable_columns[9] = MaintableColumn(heading='beweidet (%)',
                                                    column_type='float')
        self.maintable_columns[10] = MaintableColumn(heading='Gst-Fläche (ha)',
                                                    column_type='str')
        self.maintable_columns[11] = MaintableColumn(heading='Datenstand',
                                                     column_type='str')

    def getMainQuery(self, session):
        super().getMainQuery(session)

        """subquery um die flaeche des verschnittes von koppeln und 
        gst-version zu bekommen"""
        sub_cutarea = session.query(
            BAkt.id.label("akt_id"),
            BCutKoppelGstAktuell.gst_version_id,
            func.sum(func.ST_Area(BCutKoppelGstAktuell.geometry)).label("bew_area"),
            func.max(BKomplexVersion.jahr)
        )\
            .select_from(BCutKoppelGstAktuell) \
            .join(BKoppel) \
            .join(BKomplexVersion) \
            .join(BKomplex) \
            .join(BAkt) \
            .group_by(BCutKoppelGstAktuell.gst_version_id,
                      BAkt.id)\
            .subquery()
        """"""
        """eigentliche Abfrage für die Darstellung der Tabelle;
        wichtig ist hier, dass auf den akt-id und (!!) auf den gst-id gruppiert
        wird"""
        query = session.query(BGstZuordnung.id,
                              BAkt.name,
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
            .select_from(BAkt) \
            .join(BGstZuordnung) \
            .join(BGst) \
            .join(BGstVersion) \
            .join(BGstEz) \
            .join(BKatGem) \
            .join(BGstAwbStatus) \
            .join(BRechtsgrundlage) \
            .outerjoin(sub_cutarea,
                       (BGstVersion.id == sub_cutarea.c.gst_version_id) &
                       (BAkt.id == sub_cutarea.c.akt_id)) \
            .group_by(BGstZuordnung.id)
        """"""

        return query

    def setMainTableModel(self):
        super().setMainTableModel()

        return GstAllModel(self, self.maintable_dataarray)

    def setFilterScopeUI(self):
        super().setFilterScopeUI()

        """ilter awb"""
        self.guiFilterAwbLbl = QLabel("AW-Buch:")
        self.guiFilterAwbCombo = QComboBox(self)

        self.uiTableFilterHLay.insertWidget(2, self.guiFilterAwbLbl)
        self.uiTableFilterHLay.insertWidget(3, self.guiFilterAwbCombo)
        """"""

    def setFilterScope(self):
        super().setFilterScope()

        self.setFilterAwb()

    def setFilterAwb(self):

        with db_session_cm() as session:
            item_query = session.query(BGstAwbStatus.name).distinct()

        try:
            self.guiFilterAwbCombo.currentTextChanged.disconnect(
                self.filterMaintable)
        except:
            pass
        finally:
            prev_typ = self.guiFilterAwbCombo.currentText()
            self.guiFilterAwbCombo.clear()

            self.guiFilterAwbCombo.addItem('- Alle -')
            for item in sorted(item_query):
                self.guiFilterAwbCombo.addItem(str(item[0]))

            self.guiFilterAwbCombo.setCurrentText(prev_typ)

            self.guiFilterAwbCombo.currentTextChanged.connect(
                self.applyFilter)

    def useFilterScope(self, source_row, source_parent):
        super().useFilterScope(source_row, source_parent)

        try:
            """filter awb"""
            table_value = self.filter_proxy.sourceModel() \
                .data(self.filter_proxy.sourceModel().index(source_row, 6),
            Qt.DisplayRole)
            if self.guiFilterAwbCombo.currentText() != "- Alle -":
                if str(table_value) != self.guiFilterAwbCombo.currentText():
                    return False
            """"""
        except:
            print("Filter Error:", sys.exc_info())

    def updateMainWidget(self):

        self.updateMaintable()



class GstAllModel(TableModel):

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.BackgroundRole:
            if index.column() == 6:
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

            if index.column() == 8:  # beweidet ha
                val = self.data(index, Qt.EditRole)
                if val:
                    try:
                        return '{:.4f}'.format(
                            round(float(val) / 10000, 4)).replace(".", ",")
                    except ValueError:
                        pass
            """errechne den anteil der beweidet wird"""
            if index.column() == 9:  # beweidet %
                bew_val = self.data(self.index(index.row(), 8), Qt.EditRole)
                total_val = self.data(self.index(index.row(), 10), Qt.EditRole)
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

            if index.column() == 10:  # Gst-Fläche
                val = self.data(index, Qt.EditRole)
                if val:
                    try:
                        return '{:.4f}'.format(
                            round(float(val) / 10000, 4)).replace(".", ",")
                    except ValueError:
                        pass

        return super().data(index, role)
