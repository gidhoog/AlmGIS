import csv

from qgis.PyQt.QtCore import QAbstractTableModel, Qt, QModelIndex, \
    QSortFilterProxyModel, QItemSelectionModel, QItemSelection, \
    QItemSelectionRange
from qgis.PyQt.QtGui import QPalette, QColor
from qgis.PyQt.QtWidgets import QWidget, QHeaderView, QMenu, QAction, QToolButton, \
    QAbstractItemView, QFileDialog, QMessageBox, QTableView, QLabel, QLineEdit, \
    QDialog

from qgis.gui import (QgsAttributeTableModel, QgsAttributeTableView,
                      QgsAttributeTableFilterModel, QgsIFeatureSelectionManager)
from qgis.core import QgsVectorLayerCache

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from core import data_view_UI, db_session_cm
from core.entity import EntityDialog
from core.footer_line import FooterLine
from core.main_widget import MainWidget


class GisTableView(QgsAttributeTableView):

    def __init__(self, parent):
        super(GisTableView, self).__init__(parent)

        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.doubleClicked.connect(self.test_click)

    def test_click(self):

        print(f'++++++ double clicked +++++++')

        # self.verticalHeader().setSectionsClickable(True)
        #
        # self.setAlternatingRowColors(True)

    # def selectionMode(self):
    #
    #     return QAbstractItemView.ExtendedSelection
    #
    # def selectionBehavior(self):
    #
    #     return QAbstractItemView.SelectRows


class GisTableModel(QgsAttributeTableModel):

    def __init__(self, layerCache, parent=None):
        super(GisTableModel, self).__init__(layerCache, parent)

    # def data(self, index: QModelIndex, role: int = ...):
    #
    #     """
    #     erzeuge ein basis-model
    #     """
    #     # row = index.row()
    #     # col = index.column()
    #     #
    #     # if role == Qt.TextAlignmentRole:
    #     #
    #     #     if index.column() in [2, 6, 7, 8, 9]:
    #     #
    #     #         return Qt.AlignRight | Qt.AlignVCenter
    #     #
    #     #     if index.column() in [1, 10]:
    #     #
    #     #         return Qt.AlignHCenter | Qt.AlignVCenter
    #
    #     if index.column() == 7:
    #
    #         val = self.layer().getFeature(index.row()+1).geometry().area()
    #
    #         if role == Qt.DisplayRole:
    #
    #             # attr = self.layer().getFeature(index.row()+1).attributes()[index.column()]
    #
    #             print(f'val: {val}')
    #             # return self.mci_list[row].rel_gst.gst
    #             return val
    #
    #         if role == Qt.DisplayRole:
    #
    #             return val
    #
    #     return super().data(index, role)




class TableView(QTableView):
    """
    baseclass für ein data_view
    """

    def __init__(self, parent):
        super(TableView, self).__init__(parent)

        self.parent = parent

        self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()

    def keyPressEvent(self, event):
        """
        aktionen die bei tastendruck durchgeführt werden sollen
        """

        if event.key() == Qt.Key_Delete:
            self.parent.delRowMain()
        # elif event.key() == Qt.Key_Insert:
        #     self.parent.addRowMain()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.parent.edit_row()
        else:
            super().keyPressEvent(event)


class DataViewEntityDialog(EntityDialog):
    """
    Dialog für ein Entity, dass aus einem DataView geöffnet wird
    """

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.set_apply_button_text('&Speichern und Schließen_dv')

    def accept(self):
        super().accept()

        self.parent.updateMaintableNew()

        QDialog.accept(self)


class TableModel(QAbstractTableModel):
    """
    baseclass für ein model für ein data_view

    bei der initialisierung wird ein einfaches data_array übergeben (das z.b.
    mit einer SQLAlchemy-abfrage erzeugt wurde); aus diesem data_array wird auf
    basis des 'QAbstractTableModel' ein 'TableModel' erzeugt
    """

    def __init__(self, parent):
        super(TableModel, self).__init__(parent)

        self.parent = parent
        self.mci_list = []

        self.header = []

    def data(self, index: QModelIndex, role: int = ...): ...

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
        super().headerData(column, orientation, role)

        if self.header:
            if role == Qt.DisplayRole and orientation == Qt.Horizontal:

                return self.header[column]


class DataView(QWidget, data_view_UI.Ui_DataView):
    """
    baseclass für maintables
    """

    """klasse des entity_widgets"""
    entity_widget_class = None
    """"""
    """klasse des dialoges"""
    entity_dialog_class = DataViewEntityDialog
    _type_mc = None
    _entity_mc = None

    _model_class = TableModel
    _main_table_model_class = None

    _gis_table_model_class = GisTableModel

    _data_view_mc = None

    _mci_list = []
    _gis_layer = None
    _canvas = None

    _custom_data = {}

    data_view_class = TableView

    """verfügbare filter für diese tabelle"""
    _available_filters = 'g'
    """"""

    """standardeinstellung für den filter"""
    filter_activated = False

    """titel für den main_tabel"""
    _title = ''
    """"""
    _maintable_text = ["Eintrag", "Einträge", "kein Eintrag"]
    _delete_window_title = ["Eintrag löschen", "Einträge löschen"]
    _delete_window_text_single = "Soll der ausgewählte Eintrag " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Einträge wirklich gelöscht werden?"]
    _delete_text = ["Der Eintrag", "kann nicht gelöscht werden, da er "
                                   "verwendet wird!"]

    _commit_entity = True
    edit_entity_by = 'id'  # or 'mci'

    """einige einstellungen für diese klasse"""
    _select_behaviour = 'row'  # standardverhalten was ausgewählt werden soll
    _edit_behaviour = 'dialog'  # standardverhalten um tabelleneinträge zu bearbeiten
    _display_vertical_header = True  # steuert die sichtbarkeit des vertical_header
    _selected_rows_id = []  # liste der id's der ausgewählten zeilen
    _selected_rows_number = 0  # anzahl der ausgewählten zeilen
    _footer_line = FooterLine  # klasse des fuß-widgets
    """"""

    @property  # getter
    def display_vertical_header(self):
        return self._display_vertical_header

    @display_vertical_header.setter
    def display_vertical_header(self, value):
        self._display_vertical_header = value

    @property  # getter
    def edit_behaviour(self):
        return self._edit_behaviour

    @edit_behaviour.setter
    def edit_behaviour(self, edit_behaviour):
        if edit_behaviour in ['dialog', 'row']:
            self._edit_behaviour = edit_behaviour

    @property  # getter
    def select_behaviour(self):
        return self._select_behaviour

    @select_behaviour.setter
    def select_behaviour(self, select_behaviour):
        if select_behaviour in ['row', 'cell']:
            self._select_behaviour = select_behaviour

    @property  # getter
    def entity_typ_parent_ids(self):

        return self._entity_typ_parent_ids

    @entity_typ_parent_ids.setter
    def entity_typ_parent_ids(self, entity_typ_parent_ids):

        self._entity_typ_parent_ids = entity_typ_parent_ids

    @property  # getter
    def entity_widget(self):

        return self._entity_widget

    @entity_widget.setter
    def entity_widget(self, entity_widget):

        self._entity_widget = entity_widget

    @property  # getter
    def available_filters(self):
        return self._available_filters

    @available_filters.setter
    def available_filters(self, available_filters):
        """
        definiere die verfügbaren filtertypen
        (derzeit ist nur der 'g' und 's' filter verfügbar)

        possible options:
        g = general (ein suchfeld filter alle spalten in der tabelle)
        s = scope   (ein oder mehrere filter-widgets filter definierte spalten;
                     die filter-widget müssen speziell angelegt werden)
        d = detail  (ein spezieller filter mit dem individuell ein oder mehrere
                     spalten nach 'and' oder 'or' gefiltert weden können)
        c = custom  (ein vordefinieter und komplexer filter der aktiviert oder
                     deaktiviert werden kann)

        es können auch mehrere filtertypen verwendet werden
        z.b.: 'gs' or 'gc' or 'gsd'
        """

        self._available_filters = available_filters

    @property  # getter
    def displayed_rows(self):
        return self._displayed_rows

    @displayed_rows.setter
    def displayed_rows(self, displayed_rows):
        """
        die anzahl der zeilen dieser tabelle;
        gleichzeitig wird dieser wert im tabellenfuss angezeigt
        """

        if displayed_rows == 0:
            text = self._maintable_text[2] + ' vorhanden'
        if displayed_rows == 1:
            text = '1 ' + self._maintable_text[0]
        if displayed_rows > 1:
            text = str(displayed_rows) + ' ' + self._maintable_text[1]

        self.uiTableFooterTextLbl.setText(text)
        self._displayed_rows = displayed_rows

    @property  # getter
    def selected_rows_id(self):
        """
        getter für die ausgewählten zeilen dieser tabelle

        :return: liste der id's der ausgewählten zeilen
        """
        self._selected_rows_id = []
        _selected_rows_idx = []

        if self.view.selectionModel():
            _selected_rows_idx = self.view.selectionModel().selectedRows()

            for row_idx in _selected_rows_idx:

                row = self.filter_proxy.mapToSource(row_idx).row()
                self._selected_rows_id.append(
                    self.model.data(
                        self.model.index(row, self.id_column), Qt.EditRole))

        return self._selected_rows_id

    @selected_rows_id.setter
    def selected_rows_id(self, value):
        """
        setter für die ausgewählten zeilen;
        zeilen können mit der liste der indexes gewählt werden

        :param value: liste der id's der ausgewählten zeilen
        :return:
        """
        selection_model = self.view.selectionModel()
        selection_model.clearSelection()

        self.view.setSelectionBehavior(
            QAbstractItemView.SelectRows)

        sel_idx = QItemSelection()

        for data_id in value:
            for row in range(self.model.rowCount()):
                if data_id == self.model.data(
                        self.model.index(row, 0),
                        Qt.EditRole):
                    ix = QItemSelectionRange(
                        self.filter_proxy.mapFromSource(
                            self.model.index(row, 0)))
                    sel_idx.append(ix)

        selection_model.select(sel_idx,
                               QItemSelectionModel.Rows | QItemSelectionModel.Select)

        self.updateFooter()

        self._selected_rows_id = value

    @property  # getter
    def selected_rows_number(self):
        return self._selected_rows_number

    @selected_rows_number.setter
    def selected_rows_number(self, value):
        """
        anzahl der ausgewählten zeilen; wird in der fußzeile angezeigt
        """
        if value > 0:
            text = "  (" + str(value) + " ausgewählt)"
        else:
            text = ""
        self.uiTableFooterTextSelectedLbl.setText(text)

        self._selected_rows_number = value

    @property  # getter
    def title(self):
        return self._title

    @title.setter
    def title(self, value):

        self.uiTitleLbl.setText(value)
        self._title = value

    def __init__(self, parent=None, mci_list=None, gis_layer=None, canvas=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent
        self._mci_list = mci_list
        self._gis_layer = gis_layer
        self._canvas = canvas

        """liste mit den widgets im fußbereich der tabelle (zum anzeigen 
        verschiedener spaltensummen"""
        self.footer_list = []
        """"""

        """optionales menü, das dem 'uiAddDataTbtn' übergeben werden kann wenn
        z.b. unterschiedliche typen in der gleichen tabelle dargestellt werden"""
        self.add_entity_menu = QMenu(self)
        """"""

        """anzahl der maximal möglichen detail-filter (noch nicht fertig!)"""
        self.maintable_filter_limit = 5
        """"""

        if self._gis_layer is not None:

            self.vector_layer_cache = QgsVectorLayerCache(gis_layer,
                                                     10000)
            self.model = self._gis_table_model_class(
                self.vector_layer_cache, self)
            self.model.loadLayer()

            self.filter_proxy = QgsAttributeTableFilterModel(
                canvas,
                self.model
            )

            # self.view = QgsAttributeTableView()
            self.view = GisTableView(self)
            self.view.setModel(self.filter_proxy)
            self.initUi()

            self.initDataView()

        else:

            self.model = self._model_class(self)
            self.filter_proxy = SortFilterProxyModel(self)
            # self.filter_proxy = QgsAttributeTableFilterModel(None, self.model, self)
            self.filter_proxy.setSourceModel(self.model)

            """definiere das verwendete view; funktioniert derzeit nur mit
            einem QTableView, soll aber auch mit einem QTreeView möglich sein"""
            self.view = self.data_view_class(self)
            self.view.setModel(self.filter_proxy)

            self.initUi()
            self.loadData()

            self.initDataView()
            """"""

        self.uiTableVlay.addWidget(self.view)

        self.view_gis = GisTableView(self)
        self.uiTableVlay.addWidget(self.view_gis)

        # """liste mit den widgets im fußbereich der tabelle (zum anzeigen
        # verschiedener spaltensummen"""
        # self.footer_list = []
        # """"""
        #
        # """optionales menü, das dem 'uiAddDataTbtn' übergeben werden kann wenn
        # z.b. unterschiedliche typen in der gleichen tabelle dargestellt werden"""
        # self.add_entity_menu = QMenu(self)
        # """"""
        #
        # """anzahl der maximal möglichen detail-filter (noch nicht fertig!)"""
        # self.maintable_filter_limit = 5
        # """"""

        # self.model = self._model_class(self)
        # self.filter_proxy = SortFilterProxyModel(self)
        # self.filter_proxy.setSourceModel(self.model)
        #
        # """definiere das verwendete view; funktioniert derzeit nur mit
        # einem QTableView, soll aber auch mit einem QTreeView möglich sein"""
        # self.view = self.data_view_class(self)
        # self.uiTableVlay.addWidget(self.view)
        # """"""
        #
        # self.view.setModel(self.filter_proxy)
        #
        # self.initUi()

    def test_sel(self):

        print(f':::::::::selection changed ::::::::::::')

    def signals(self):

        self.uiEditDataTbtn.clicked.connect(self.clickedEditRow)
        self.uiDeleteDataTbtn.clicked.connect(self.delRowMain)

        self.view.doubleClicked.connect(self.doubleClickedRow)

        self.view.selectionModel().selectionChanged \
            .connect(self.selectedRowsChanged)

        if self._gis_layer is not None:
            self._gis_layer.selectionChanged.connect(self.test_sel)
        self.uiClearSelectionPbtn.clicked.connect(self.clearSelectedRows)

        self.uiSelectAllTbtn.clicked.connect(self.selectAllRows)

        self.uiActionExportCsv.triggered.connect(self.export_csv)

    def getSelectedRows(self):
        """
        liste der QModelIndex der ausgewählten zeilen

        :return: list of QModelIndex
        """

        if self.view.selectionModel():
            indexes = self.view.selectionModel().selectedRows()

            return indexes

    def selectAllRows(self):

        self.view.selectAll()

    def clearSelectedRows(self):
        """
        hebe die auswahl der zeilen auf
        """
        self.view.selectionModel().clear()

    def selectedRowsChanged(self):
        """
        die auswahlt der zeilen hat sich geändert
        """
        print(f'--- selection changed -----------------------')
        self.updateFooter()

    def getProxyIndex(self, index):
        """
        erhalte den filter_proxy index des übergebenen maintable_model index
        :return: QModelIndex
        """
        return self.filter_proxy.mapToSource(index)

    def setSelectedRowsNumber(self):
        """
        trage die anzahl der ausgewählten zeilen im fuß-element ein

        :return:
        """

        indexes = self.getSelectedRows()

        number = len(indexes)
        if number > 0:
            text = "  (" + str(number) + " ausgewählt)"
        else:
            text = ""

        self.uiTableFooterTextSelectedLbl.setText(text)

    def export_csv(self):
        """
        exportiere die maintable als csv
        """

        try:
            """erstelle eine neue datei"""
            name, _ = QFileDialog.getSaveFileName(
                self, 'exportiere Tabelle', "", "All Files (*);;CSV Files (*.csv)")
            """"""

            """öffne die datei"""
            with open(name, 'w', newline='', encoding='utf8') as f:

                writer = csv.writer(f, delimiter=";")

                """hole die spaltenüberschriften"""
                header_list = []
                for column_name in self.model.header:
                    header_list.append(column_name)
                """"""

                """schreibe die spaltenüberschriften in die datei"""
                writer.writerow(list(header_list))
                """"""

                """hole die zellenwerte"""
                for row in range(self.view.model().rowCount()):
                    row_text = []
                    for col in range(self.view.model().columnCount()):
                        value = self.view.model().data(
                            self.view.model().index(
                                row, col),
                            Qt.DisplayRole)
                        row_text.append(str(value))
                    writer.writerow(row_text)  # schreibe zeile in datei
                """"""
        except:
            print(f"cannot create csv")

    def initUi(self):
        """
        definiere das layout des maintables hier;

        :return:
        """

        self.setSelectBehaviour()
        self.setEditBehaviour()
        self.setSorting()
        self.setDisplayVetricalHeader()
        self.setFilterUI()

        """setze detail-filter buttons unsichtbar"""
        self.uiEnableFilterDetailPbtn.setVisible(False)
        self.uiAddFilterDetailRowPbtn.setVisible(False)
        self.uiDelFilterDetailRowPbtn.setVisible(False)
        """"""

        self.uiActionExportCsv = QAction(self.uiToolsTbtn)
        self.uiActionExportCsv.setText('exportiere csv-Datei')
        self.uiToolsTbtn.addAction(self.uiActionExportCsv)

        """definiere für eine alternative zeilen farbe"""
        data_view_palette = self.view.palette()
        data_view_palette.setColor(QPalette.AlternateBase, QColor(205, 202, 28, 20))
        self.view.setPalette(data_view_palette)
        self.view.setAlternatingRowColors(True)
        """"""

    def setDisplayVetricalHeader(self):
        """
        setze die sichtbarkeit des vertical_headers
        """

        if not self.display_vertical_header:
            self.view.verticalHeader().hide()

    def setEditBehaviour(self):
        """
        setze den bearbeitungsmodus;
        derzeit ist nur 'dialog' umgesetzt
        """

        if self.edit_behaviour == 'dialog':
            self.view.setEditTriggers(
                QAbstractItemView.NoEditTriggers)
        if self.edit_behaviour == 'row':
            self.view.setEditTriggers(
                QAbstractItemView.CurrentChanged)

    def setFilterUI(self):
        """
        setze das layout für die filter
        :return:
        """
        if 'g' in self.available_filters:
            self.setFilterGeneralUI()

        if 's' in self.available_filters:
            self.setFilterScopeUI()

    def setFilterGeneralUI(self):
        """
        setze das layout für den generellen filter
        :return:
        """
        self.guiFiltGeneralLbl = QLabel("Suche:")
        self.guiFiltGeneralLedit = QLineEdit(self)
        self.guiFiltGeneralLedit.setClearButtonEnabled(True)

        self.uiTableFilterHLay.insertWidget(0, self.guiFiltGeneralLbl)
        self.uiTableFilterHLay.insertWidget(1, self.guiFiltGeneralLedit)

        self.guiFiltGeneralLedit.textChanged.connect(self.applyFilter)

    def setFilterScopeUI(self):
        """
        setze das layout für den scope-filter;
        subclass in child-widgets falls der scope-filter verwendet wird
        :return:
        """
        pass

    def setSelectBehaviour(self):
        """
        setze die auswahlmethode der tabelleneinträge;
        derzeit nur 'row' umgesetzt
        """

        if self.select_behaviour == 'row':
            self.view.setSelectionBehavior(
                QAbstractItemView.SelectRows)
        if self.select_behaviour == 'cell':
            self.view.setSelectionBehavior(
                QAbstractItemView.SelectItems)

    def setSorting(self):
        """
        lege das sortierverhalten fest
        """

        self.view.setSortingEnabled(True)
        """sort case insensitive"""
        self.filter_proxy.setSortCaseSensitivity(Qt.CaseInsensitive)
        """"""

    def setFilter(self):
        """
        aktiviere die vorgesehenen filter
        """

        if 's' in self.available_filters:
            self.setFilterScope()

        if self.filter_activated is False:
            self.filter_proxy.invalidateFilter()
            self.filter_activated = True

    def setFilterScope(self):
        """
        aktiviere den scope-filter;
        subclass in child-widget falls verwendet
        (z.b. core.scopes.gst.gst_zuordnung.GstTable)
        :return:
        """
        pass

    def applyFilter(self):
        """
        methode die aufgrrufen wird wenn der filter angewendet werden soll
        (z.b. wenn sich die daten im einem filter-widget ändern)
        :return:
        """
        self.filter_proxy.invalidateFilter()
        self.updateFooter()

    def useFilterScope(self, source_row, source_parent):
        """
        teil der methode 'filterAcceptsRow' um die werte des scope-filters
        und dem tableview zu vergleichen

        :param source_row:
        :param source_parent:
        :return: False wenn die werte nicht übereinstimmen
        """
        pass

    def updateFilterElements(self):
        """
        aktualisiere die filter-elemete
        :return:
        """

        if 's' in self.available_filters:
            self.updateFilterElementsScope()

    def updateFilterElementsScope(self):
        """
        aktualisiere die filter-elemete des scope-filter (z.b. das filter widget
        ist eine combobox und ein datensatz in der tabelle wurde gelöscht)
        :return:
        """
        pass

    def initDataView(self):
        """
        initialisiere maintable

        :param parent_id:
        :param
        :return:
        """
        self.setFilter()

        # self.setAddEntityMenu()
        self.setDataViewLayout()

        self.signals()

        self.updateFooter()
        self.finalInit()

    def setMciList(self, mci_list):

        self.view.model().sourceModel().layoutAboutToBeChanged.emit()

        for mci in mci_list:
            self.filter_proxy.sourceModel().mci_list.append(mci)

        self.view.model().sourceModel().layoutChanged.emit()

    def setCustomMci(self, custom_mci):

        self._customm_mci = custom_mci

    def getMciList(self, session):
        """
        frage die mci für dieses DataView ab und return es
        :param session:
        :return: mci
        """
        stmt = select(self._entity_mc)

        mci = session.scalars(stmt).unique().all()

        return mci

    def getCustomData(self, session):
        """
        lade alle Daten für dieses DataView
        :return:
        """

    def loadData(self):

        with db_session_cm() as session:

            mci_list = self.getMciList(session)
            self.getCustomData(session)

        self.view.model().sourceModel().layoutAboutToBeChanged.emit()

        self.view.model().sourceModel().mci_list.clear()

        for mci in mci_list:
            self.view.model().sourceModel().mci_list.append(mci)

        self.view.model().sourceModel().layoutChanged.emit()

    def finalInit(self):
        """
        dinge die direkt nach dem initialisieren durchgeführt werden sollen
        :return:
        """
        pass

    def updateMaintableNew(self):
        """
        aktualisiere das table_view
        :return:
        """
        if self._commit_entity:

            self.loadData()

        self.updateFooter()

        """data_view hat als parent ein MainWidget"""
        if issubclass(self.parent.__class__, MainWidget):
            self.parent.updateMainWidget()
        """"""

    def setDataViewLayout(self):
        """
        setze das data_view-layout
        :return:
        """
        pass

    def setStretchMethod(self, method):
        """
        setze die strech-methode der tabelle

        1: die spaltenbreite wird nur an den inhalt angepasst
        2: nur die letzte spalte wird bis zum tabellenende gedehnt
        3: alle spalen werden gleichmäßig verteilt
        """
        if method == 1:
            self.view.resizeColumnsToContents()
        elif method == 2:
            self.view.horizontalHeader().setStretchLastSection(True)
        elif method == 3:
            self.view.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)

    def insertFooterLine(self, label, unit, column_calc, amount_width, factor=1,
                         decimal=None, filter_col=None, filter_operator=None,
                         filter_criterion=None):
        """
        füge ein footer-elemet (=widget am fuß der tabelle) auf position 0
        in das layout 'uiFooterLinesVlay' ein
        """

        footer_line = self._footer_line(self, label, unit, column_calc, amount_width,
                                        factor, decimal, filter_col, filter_operator,
                                        filter_criterion)

        self.uiFooterLinesVlay.insertWidget(0, footer_line)
        self.footer_list.append(footer_line)

    def updateFooter(self):
        """
        aktualisiere alle footer elemente (zeilenanzahl, summenelemente, ...)
        """
        for line in self.footer_list:
            line.update_footer_line(self.getSelectedRows())

        self.displayed_rows = self.view.model().rowCount()
        if self.getSelectedRows():
            self.selected_rows_number = len(self.getSelectedRows())
        else:
            self.selected_rows_number = 0

    def get_selected_type_id(self, index):
        """
        erhalte den type_id von der ausgewählten zeile
        die type-spalte muss in der eigenschaft 'typ_column' eingetragen sein

        wird derzeit nicht verwendent!!!

        :return: type_id
        """
        typ_column = list(self.entity_typ_column.keys())[0]

        sel_type_id = self.model.data(
            self.model.index(index.row(),
                                       typ_column),
            Qt.DisplayRole)

        return sel_type_id

    def get_row_id(self, index):
        """
        erhalte den entity_id der ausgewählten zeile
        :param index: QModelIndex der zeile
        :return: entity_id
        """

        entity_id = self.model.data(
            self.model.index(index.row(),
                                       self.id_column),
            Qt.EditRole)

        return entity_id

    def doubleClickedRow(self, index):

        if self.edit_behaviour == 'dialog':

            self.indexBasedRowEdit(index)

    def indexBasedRowEdit(self, index):
        """
        define here zones of columns for different edit behaviours

        subclass this method to enable individual settings
        """

        if 0 <= index.column() <= 9999:  # all columns of the model

            entity_witdget_class = self.get_entity_widget_class(index)

            if self.edit_entity_by == 'id':
                self.editRow(entity_witdget_class(self),
                             entity_id=self.getEntityId(index))

            if self.edit_entity_by == 'mci':
                self.editRow(entity_witdget_class(self),
                             entity_mci=self.getEntityMci(index))

    def getEntityId(self, index):
        """
        liefere den id des Datensatzes mit dem übergebenen Index

        :param index: QModelIndex
        :return: int (z.B.: self._mci_list[self.getProxyIndex(index).row()].id)
        """
        return self.model.mci_list[self.getProxyIndex(index).row()].id

    def getEntityMci(self, index):
        """
        liefere die MCI (Mapped Class Instance) des Datensatzes mit dem
        übergebenen Index

        :param index: QModelIndex
        :return: MCI-Objekt (z.B.: self._mci_list[index.row()])
        """
        return self.model.mci_list[self.getProxyIndex(index).row()]

    def rowSelected(self):
        """
        kontrolliere ob eine Zeile ausgewählt ist
        :return: False wenn keine Zeile gewählt ist, den QModelIndex der ersten
        Zeile wenn eine ausgewählt ist
        """

        """hole den index der ausgewählten zeile"""
        sel_rows = self.getSelectedRows()
        """"""
        """breche ab wenn keine zeile ausgewählt ist"""
        if not sel_rows:
            self.no_row_selected_msg()
            return False
        """"""
        return sel_rows[0]

    def editEntity(self):

        pass

    def clickedEditRow(self):
        """
        die Schaltfläche zum einfügen/anlegen eines neuen Datensatzes wird
        geklickt
        :return:
        """

        """hole den index der ausgewählten zeilen"""
        sel_indexes = self.getSelectedRows()
        """"""
        """breche ab wenn keine zeile ausgewählt ist"""
        if not sel_indexes:
            self.no_row_selected_msg()
            return
        """"""
        """nehme den ersten index (falls mehrere ausgewählt sind) und
        wandle ihn in einen proxy-index um"""
        proxy_index = self.getProxyIndex(sel_indexes[0])
        """"""

        self.edit_row(proxy_index)

    def getCustomEntityData(self):
        """
        define or create here a list with custom data that is given in 'editRow'
        to edit the entity (e.g. data for comboboxes)
        """
        return []

    def editRow(self, entity_widget, entity_id=None, entity_mci=None):
        """
        edit one table row;
        you could use the table_index to get the column (e.g. to open different
        item-widgets on different columns for editing)

        :return:
        """
        if entity_id:
            entity_widget.editEntity(entity_id=entity_id,
                                     custom_entity_data=self.getCustomEntityData())

        if entity_mci:
            entity_widget.editEntity(entity_mci=entity_mci,
                                     custom_entity_data=self.getCustomEntityData())

        """open the entity_widget_class in a dialog"""
        self.openDialog(entity_widget)
        """"""

    def get_entity_widget(self, sel_index):
        """
        hole das entity-widget; brücksichtige, dass es typ-abhängig sein kann;
        in diesem fall wird die widget-klasse aus der entsprechenden tabelle mit
        den typ-date geholt und eine entity-widget instanz erzeugt"""

        if self.entity_typ_column:  #: if there are entity_type set
            """hole die modul und widget_class infos von der type_data_instance"""
            module, widget_class = self.get_entity_widget_class(
                self.get_selected_type_id(sel_index))
            """"""

            """hole die widget_class erzeuge eine instance"""
            entity_module = __import__(module, fromlist=[widget_class])
            wid = getattr(entity_module, widget_class)
            entity_widget = wid(self)
            """"""
        else:  # es gibt keine unterschiedlichen entity-typen
            entity_widget = self.entity_widget(self)

        return entity_widget

    def get_entity_widget_class(self, sel_index):
        """get the entity_widget_class; consider there are different types of the
        item"""

        if self.entity_widget_class is not None:

            wdg_class = self.entity_widget_class

        elif hasattr(self.mci_list[sel_index.row()], 'rel_type'):
            """get the module and the widget_class from the
            type_data_instance"""
            # module, widget_class = self.get_item_widget_class(
            #     self.get_selected_type_id(sel_index))
            module = self.mci_list[sel_index.row()].rel_type.module
            widget_class = self.mci_list[sel_index.row()].rel_type.type_class

            """import the widget_class and make a instance"""
            item_module = __import__(module, fromlist=[widget_class])
            wdg_class = getattr(item_module, widget_class)
            # item_widget = wid(self)
            """"""

        return wdg_class

    def get_type_class(self, type_instance):
        """
        wandle die sting-infos aus der type_instanz in eine klasse um
        :return:
        """
        entity_module = __import__(type_instance.module,
                                   fromlist=[type_instance.type_class])
        return getattr(entity_module, type_instance.type_class)

    def no_row_selected_msg(self):
        """
        mitteilung das keine zeile ausgewählt ist
        """
        msg_text = "Es ist kein Eintrag ausgewählt.\n\n"
        msg = QMessageBox(self)
        msg.setWindowTitle("Info")
        msg.setInformativeText(msg_text)
        msg.setStandardButtons(QMessageBox.Ok)
        # msg.centerInGivenWdg(self.view)
        msg.exec()

    def delRowMain(self):
        """
        einstiegs-metode zum löschen einer oder mehrerer zeilen dieser tabellen
        """

        indexes = self.getSelectedRows()

        if not indexes:  # no row selected
            self.no_row_selected_msg()
            return
        else:
            msgbox = self.delMsg(len(indexes))

            if msgbox.exec() == QMessageBox.Yes:
                self.delRow()
                # self.updateOnAccept()
                self.updateMaintableNew()

    def delRow(self):
        """eigentliche methode zum löschen von zeilen der tabelle"""

        indexes = self.getSelectedRows()

        for index in indexes:
            try:
                """lösche den datensatz mit SQLAlchemy-session"""
                with db_session_cm() as session:
                    inst = session.query(self.data_model_class).filter(
                        self.data_model_class.id == self.filter_proxy.data(
                            self.filter_proxy.index(
                                index.row(), self.id_column),
                            Qt.DisplayRole)).first()
                    session.delete(inst)
                """"""
            except IntegrityError:
                """falls der datensatz mit einer anderen tabelle verknüpft ist
                soll er nicht gelöscht werden"""
                if self.getDeleteInfo(index) is not False:
                    del_info = self.getDeleteInfo(index)
                else:
                    del_info = 'in Zeile '+str(index.row())
                self.can_not_delete_msg(del_info)
                """"""

    def getDeleteInfo(self, index=None):
        """
        definiere hier den info-text für die lösch-nachricht
        :return: delete_info (str)
        """
        return False

    def can_not_delete_msg(self, delete_info):
        """
        nachricht das der datensatz nicht gelöscht werden kann, da er mit einer
        anderen tabelle in beziehung steht
        :return:
        """
        msgbox = QMessageBox(self)
        msgbox.setWindowTitle(self._delete_window_title[0])
        msgbox.setInformativeText(self.delete_text[0] + '\n\n' + delete_info
                                  + '\n\n' + self.delete_text[1])
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.centerInGivenWdg(self.view)
        msgbox.exec()

    def delMsg(self, delete_number):
        """
        absicherungs-frage ob ein oder mehrere datensätze wirklich gelöscht
        werden sollen
        """

        msgbox = QMessageBox(self)

        if delete_number == 1:
            msgbox.setWindowTitle(self._delete_window_title[0])
            msgbox.setInformativeText(self._delete_window_text_single +
                                      "\n\n\n")
        if delete_number > 1:
            msgbox.setWindowTitle(self._delete_window_title[1])
            msgbox.setInformativeText(self._delete_window_text_plural[0] +
                                      " " +
                                      str(delete_number) +
                                      " " +
                                      self._delete_window_text_plural[1] +
                                      "\n\n\n")

        msgbox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msgbox.setDefaultButton(QMessageBox.No)

        return msgbox

    def getEntityWidget(self, type_instance):
        """
        hole die sting-infos für modul und widget_class von einer type_instance
        """

        module = type_instance.module
        widget_class = type_instance.type_class

        return module, widget_class

    def add_row(self, **kwargs):
        """
        füge einen datensatz in eine tabelle ohne gis-geometrien ein
        """

        type_instance = None

        if kwargs:
            type_instance = kwargs['typ']

        if self.entity_typ_column:
            """unterschiedliche entity-typen sind vorhanden; hole die 
            entity_widget_class aus der type_tabelle in der datenbank"""

            """erhalte modul und widget_class als string"""
            module, widget_class = self.getEntityWidget(type_instance)
            """"""

            """importiere die widget_class und erzeuge eine instance"""
            entity_module = __import__(module, fromlist=[widget_class])
            wid = getattr(entity_module, widget_class)
            entity_widget = wid(self)
            """"""

            entity_widget.newEntity(type_instance=type_instance)

        else:
            """nehme das hinterlegt entity_widget"""
            entity_widget = self.entity_widget(self)
            entity_widget.newEntity()
            """"""

        """öffne das entity-widget in einem dialog"""
        self.openDialog(entity_widget)
        """"""
        entity_widget.focusFirst()

    def openDialog(self, entity_widget):
        """
        öffne einen dialog mit dem entity_widget
        """

        self.entity_dialog = self.entity_dialog_class(parent=self)

        """setze den entity_dialog im entity_widget"""
        entity_widget.entity_dialog = self.entity_dialog
        """"""

        self.entity_dialog.insertWidget(entity_widget)
        self.entity_dialog.resize(self.minimumSizeHint())

        self.entity_dialog.show()

        self.entity_dialog.rejected.connect(self.rejectEditingInDialog)

    def acceptEditingInDialog(self):
        """
        definiere hier aktionen die nach dem 'accept' eines datensatzes
        durchgeführt werden sollen
        """
        self.updateMaintableNew()

    def rejectEditingInDialog(self):
        """
        definiere hier was gemacht werden soll wenn die datenbearbeitung
        abgebrochen wird
        :return:
        """
        pass

    def setEntityDialog(self):
        """
        setze hier das layout des entity-dialoges (z.b. buttons, title, ...)

        :return:
        """

    # def setAddEntityMenu(self):
    #     """
    #     erzeuge ein typ basiertes add-entity menü falls eine 'entity_typ_column'
    #     vorhanden ist
    #     :return:
    #     """
    #     if self.entity_typ_column:
    #         with db_session_cm() as session:
    #             session.expire_on_commit = False
    #             type_class = list(self.entity_typ_column.values())[0]
    #             type_list = session.query(type_class) \
    #                 .filter(type_class.blank_value != 1) \
    #                 .all()
    #
    #             for type_instance in type_list:
    #                 action = QAction(type_instance.name, self)
    #                 action.triggered.connect(
    #                     lambda a_id, key=type_instance: self.add_row(typ=key))
    #                 self.add_entity_menu.addAction(action)
    #
    #             self.uiAddDataTbtn.setMenu(self.add_entity_menu)
    #             self.uiAddDataTbtn.setPopupMode(QToolButton.InstantPopup)

    def updateMaintable(self):
        """
        aktualisiere den maintable;
        """
        self.updateFooter()


class SortFilterProxyModel(QSortFilterProxyModel):
    """
    baseclass für ein QSortFilterProxyModel in dieser tabelle
    """
    def __init__(self, parent):
        QSortFilterProxyModel.__init__(self, parent)

        self.parent = parent
        self.filter_rows_with_elements = {}

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = ...):
        """erhalte die nummerierng des vertical_headers in aufsteigender
        reihenfolge, wenn sortiert wird"""
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section + 1
        """"""
        return super(SortFilterProxyModel, self).headerData(section,
                                                            orientation,
                                                            role)

    def filterAcceptsRow(self, source_row, source_parent):
        """
        diese methode überwacht ob ein filtereintrag mit einem datensatzeintrag
        übereinstimmt

        return True to display the row
        return False to hide the row

        :param source_row:
        :param source_parent:
        :return:
        """
        """filter general"""
        if 'g' in self.parent.available_filters:
            if self.parent.guiFiltGeneralLedit.text() != '':
                found = False
                """vergleiche den Zelleninhalt mit dem Text aus dem Suchfeld"""
                for col in range(len(self.parent.model.header)):
                    col_value = self.sourceModel().data(
                                self.sourceModel().index(source_row,
                                                         col), Qt.DisplayRole)
                    if str(self.parent.guiFiltGeneralLedit.text().lower()) in str(
                            col_value).lower():
                        found = True
                """"""
                if found == False:  # kein treffer in der zeile
                    return False
        """"""

        """filter scope"""
        if 's' in self.parent.available_filters:
            if self.parent.useFilterScope(source_row, source_parent) == False:
                return False
        """"""

        return True
