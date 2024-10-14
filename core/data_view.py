import csv

from qgis.PyQt.QtCore import QAbstractTableModel, Qt, QModelIndex, \
    QSortFilterProxyModel, QItemSelectionModel, QItemSelection, \
    QItemSelectionRange, QSize
from qgis.PyQt.QtGui import QPalette, QColor, QIcon
from qgis.PyQt.QtWidgets import QWidget, QHeaderView, QMenu, QAction, \
    QAbstractItemView, QFileDialog, QMessageBox, QTableView, \
    QDialog, QPushButton, QAbstractButton

from qgis.gui import (QgsAttributeTableModel, QgsAttributeTableView,
                      QgsAttributeTableFilterModel, QgsMapCanvas)
from qgis.core import QgsVectorLayerCache, edit

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from core import data_view_UI, db_session_cm, color, DbSession
from core.entity import EntityDialog
from core.footer_line import FooterLine
from core.gis_layer import Feature
from core.tools import getMciState


class GisTableView(QgsAttributeTableView):

    def __init__(self, parent):
        super(GisTableView, self).__init__(parent)

        self.parent = parent

        self.verticalHeader().setMinimumWidth(25)

        """declare the corner-button of the table-view"""
        self.uiCornerButton = self.findChild(QAbstractButton)
        self.uiCornerButton.setToolTip('wähle alle Zeilen aus')
        self.uiCornerButton.setStyleSheet(
            "QTableView QTableCornerButton::section{background: rgba(0,0,0,0); "
            "border: 0px solid rgba(0,0,0,0); border-width: 2px; "
            "image: url(:/svg/resources/icons/mActionSelectAllRows.svg);}")
        self.uiCornerButton.clicked.disconnect()
        self.uiCornerButton.clicked.connect(self.clickedCornerButton)
        """"""

    def clickedCornerButton(self):
        """
        the corner-button of the tableview is clicked
        """

        if self.parent._gis_layer.selectedFeatureIds() == []:

            self.parent._gis_layer.selectAll()
            self.setCornerButtonDeselectAll()
        else:
            self.parent._gis_layer.removeSelection()
            self.setCornerButtonSelectAll()

    def setCornerButtonSelectAll(self):
        """
        set the corner-button of the table-view to select all rows
        """

        self.uiCornerButton.setToolTip('wähle alle Zeilen aus')
        self.uiCornerButton.setStyleSheet(
            "QTableView QTableCornerButton::section{background: rgba(0,0,0,0); "
            "border: 0px solid rgba(0,0,0,0); border-width: 2px; "
            "image: url(:/svg/resources/icons/mActionSelectAllRows.svg);}")

    def setCornerButtonDeselectAll(self):
        """
        set the corner-button of the table-view to deselect all rows
        """

        self.uiCornerButton.setToolTip('hebe Auswahl auf')
        self.uiCornerButton.setStyleSheet(
            "QTableView QTableCornerButton::section{background: rgba(0,0,0,0); "
            "border: 0px solid rgba(0,0,0,0); border-width: 2px; "
            "image: url(:/svg/resources/icons/mActionDeselectAllRows.svg);}")


class GisTableModel(QgsAttributeTableModel):

    def __init__(self, layerCache, parent=None):
        super(GisTableModel, self).__init__(layerCache, parent)

        # self.parent = parent

    def headerData(self, column, orientation, role=None):
        super().headerData(column, orientation, role)

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:

            header_name = self.parent()._gis_layer.fields().field(column).name()
            header_alias = self.parent()._gis_layer.fields().field(column).alias()

            if header_alias == '':
                return header_name
            else:
                return header_alias


class TableView(QTableView):
    """
    baseclass für ein data_view
    """

    def __init__(self, parent):
        super(TableView, self).__init__(parent)
        # QTableView.__init__(self)

        self.parent = parent

        self.setEditTriggers(QAbstractItemView.AllEditTriggers)

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSortingEnabled(True)

        self.verticalHeader().setMinimumWidth(20)

        #todo: implement here 'selectRow' (see c++ code):
        self.verticalHeader().sectionPressed.connect(self.nothing)

        # highlight_focus_string = 'QTableView::item:focus {border: 2px solid #00FF7F}; '

        selection_color = color.data_view_selection
        color_string = (f'rgb({str(selection_color.red())}, '
                        f'{str(selection_color.green())}, '
                        f'{str(selection_color.blue())})')
        selection_style = f'selection-background-color: {color_string};'

        """zweiter string funktioniert leider nicht"""
        # self.setStyleSheet(selection_style + highlight_focus_string)
        """"""

        """declare the corner-button of the table-view"""
        self.uiCornerButton = self.findChild(QAbstractButton)
        self.uiCornerButton.setToolTip('wähle alle Zeilen aus')
        self.uiCornerButton.setStyleSheet(
            "QTableView QTableCornerButton::section{background: rgba(0,0,0,0); "
            "border: 0px solid rgba(0,0,0,0); border-width: 2px; "
            "image: url(:/svg/resources/icons/mActionSelectAllRows.svg);}")
        self.uiCornerButton.clicked.disconnect()
        self.uiCornerButton.clicked.connect(self.clickedCornerButton)
        """"""

        """create a custom cell-border for a clicked cell"""
        self.style = ('QTableView::item:focus {border: 3px solid #00FF7F;}')
        self.setStyleSheet(self.style)
        """"""

    def clickedCornerButton(self):
        """
        the corner-button of the tableview is clicked
        """

        if self.parent.getSelectedRows() == []:
            self.parent.selectAllRows()
            self.setCornerButtonDeselectAll()
        else:
            self.parent.clearSelectedRows()
            self.setCornerButtonSelectAll()

    def setCornerButtonSelectAll(self):
        """
        set the corner-button of the table-view to select all rows
        """

        self.uiCornerButton.setToolTip('wähle alle Zeilen aus')
        self.uiCornerButton.setStyleSheet(
            "QTableView QTableCornerButton::section{background: rgba(0,0,0,0); "
            "border: 0px solid rgba(0,0,0,0); border-width: 2px; "
            "image: url(:/svg/resources/icons/mActionSelectAllRows.svg);}")

    def setCornerButtonDeselectAll(self):
        """
        set the corner-button of the table-view to deselect all rows
        """

        self.uiCornerButton.setToolTip('hebe Auswahl auf')
        self.uiCornerButton.setStyleSheet(
            "QTableView QTableCornerButton::section{background: rgba(0,0,0,0); "
            "border: 0px solid rgba(0,0,0,0); border-width: 2px; "
            "image: url(:/svg/resources/icons/mActionDeselectAllRows.svg);}")

    def nothing(self, index):

        print(f'..nothing: {index}')

    def mousePressEvent(self, e):

        print(f'mouse pressed')

        self.setSelectionMode(QAbstractItemView.NoSelection)
        super().mousePressEvent(e)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def mouseReleaseEvent(self, e):

        pass

        self.setSelectionMode(QAbstractItemView.NoSelection)
        super().mouseReleaseEvent(e)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def mouseMoveEvent(self, e):

        pass

        self.setSelectionMode(QAbstractItemView.NoSelection)
        super().mouseMoveEvent(e)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def keyPressEvent(self, event):

        if event.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left,
                           Qt.Key_Right]:
            self.setSelectionMode(QAbstractItemView.NoSelection)
            super().keyPressEvent(event)
            self.setSelectionMode(QAbstractItemView.ExtendedSelection)
            return
        elif event.key() == Qt.Key_Delete:
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

    header = ['g',
              'f']

    def __init__(self, parent, mci_list):
        super(TableModel, self).__init__()

        self.parent = parent
        self.mci_list = mci_list

    def data(self, index: QModelIndex, role: int = ...):
        pass

    def insertRows(self, position, rows, QModelIndex, parent):
        self.beginInsertRows(QModelIndex, position, position+rows-1)
        default_row = ['']*len(self._data[0])  # or _headers if you have that defined.
        for i in range(rows):

            self.mci_list.insert(position, default_row)
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def removeRows(self, position, rows, QModelIndex):
        self.layoutAboutToBeChanged.emit()
        self.beginRemoveRows(QModelIndex, position, position+rows-1)
        for i in range(rows):

            with db_session_cm() as session:
                session.delete(self.mci_list[position])
            del(self.mci_list[position])
        self.endRemoveRows()

        self.layoutChanged.emit()

        return True

    def rowCount(self, parent: QModelIndex = ...):
        """
        definiere die zeilenanzahl
        """

        return len(self.mci_list)

    def columnCount(self, parent: QModelIndex = ...):
        """
        definiere die spaltenanzahl
        """
        return len(self.header)

    def headerData(self, column, orientation, role=None):
        """
        wenn individuelle überschriften gesetzt sind (in 'self.header')
        dann nehme diese
        """
        super().headerData(column, orientation, role)

        if self.header:
            if role == Qt.DisplayRole and orientation == Qt.Horizontal:

                return self.header[column]

    # def flags(self, index):  # to make the table(-cells) editable
    #     if not index.isValid():
    #         return Qt.ItemIsEnabled
    #
    #     return Qt.ItemFlags(
    #         QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)


class DataView(QWidget, data_view_UI.Ui_DataView):
    """
    baseclass für maintables
    """
    instance_list = []

    _main_table_model_class = None

    _data_view_mc = None

    _mci_list = []

    _gis_layer = None

    filter_proxy_gis_class = None
    vector_layer_cache_class = None

    _model_gis_class = GisTableModel
    _view_gis_class = GisTableView

    _view_class = TableView
    _model_class = None

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


    """einige einstellungen für diese klasse"""
    _select_behaviour = 'row'  # standardverhalten was ausgewählt werden soll
    # _edit_behaviour = 'dialog'  # standardverhalten um tabelleneinträge zu bearbeiten
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

    def __init__(self, parent=None, gis_mode=False):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent

        DataView.instance_list.append(self)

        self.gis_mode = gis_mode
        self.current_feature = None

        # if session:
        #     self.dataview_session = session
        # else:
        self.dataview_session = None

        self.sel_entity_mci = None

        """"""
        self.entity_dialog_class = DataViewEntityDialog
        self.entity_widget_class = None
        self._entity_mc = None
        self._type_mc = None
        self.edit_entity_by = 'id'  # or 'mci'

        self._edit_behaviour = 'dialog'  # standardverhalten um tabelleneinträge zu bearbeiten
        self._custom_dataview_data = {}

        self.custom_entity_data = {}
        """"""

        self._commit_entity = True
        self.feature_fields = []
        self._model_gis_class = GisTableModel
        self._model_class = TableModel

        """liste mit den widgets im fußbereich der tabelle (zum anzeigen 
        verschiedener spaltensummen"""
        self.footer_list = []
        """"""

        """optionales menü, das dem 'uiAddDataTbtn' übergeben werden kann wenn
        z.b. unterschiedliche typen in der gleichen tabelle dargestellt werden"""
        self.add_entity_menu = QMenu(self)
        """"""

        """"setzt die farbe der selection von zeilen"""
        selection_color = color.data_view_selection
        color_string = (f'rgb({str(selection_color.red())}, '
                        f'{str(selection_color.green())}, '
                        f'{str(selection_color.blue())})')
        selection_style = f'selection-background-color: {color_string};'
        self.setStyleSheet(selection_style)
        """"""

        self.uiTitleLbl.setVisible(False)

        if self.gis_mode:

            self.filter_proxy_gis_class = QgsAttributeTableFilterModel
            self.vector_layer_cache_class = QgsVectorLayerCache

            self.view = self._view_gis_class(self)

        else:
            self.view = self._view_class(self)
            self._model_class = TableModel

        self.uiTableVlay.addWidget(self.view)

    def setDataviewSession(self, session):

        self.dataview_session = session

    def initDataView(self):

        self.loadData(self.dataview_session)

        if self.gis_mode:

            self.setFeatureFields()

            self._gis_layer = self.setLayer()

            # self.addFeaturesFromMciList(self._mci_list)
            self.setFeaturesFromMci()

        self.setFilterUI()

        self.initView()

        self.initUi()

        self.finalInit()

        self.updateFooter()

        self.signals()

    def initView(self):

        if self.gis_mode:

            self.vector_layer_cache = self.vector_layer_cache_class(self._gis_layer,
                                                          10000)
            self.model = self._model_gis_class(
                self.vector_layer_cache, self)
            self.model.loadLayer()

            self.filter_proxy = self.filter_proxy_gis_class(
                QgsMapCanvas(),
                self.model
            )

        else:
            self.model = self._model_class(self, self._mci_list)
            self.filter_proxy = SortFilterProxyModel(self)
            self.filter_proxy.setSourceModel(self.model)

        self.view.setModel(self.filter_proxy)

    def setCanvas(self, canvas):

        self.canvas = canvas

    def test_sel(self, selected):

        print(f':::::::::selection changed :::::::::::: {selected}')

        print(f'selected feature-ids: {self._gis_layer.selectedFeatureIds()}')

    def signals(self):

        # self.uiEditDataTbtn.clicked.connect(self.clickedEditRow)
        self.uiDeleteDataTbtn.clicked.connect(self.delRowMain)
        self.uiAddDataTbtn.clicked.connect(self.add_row)

        self.view.doubleClicked.connect(self.doubleClickedRow)

        self.uiActionExportCsv.triggered.connect(self.export_csv)

        if self.gis_mode:
            self._gis_layer.selectionChanged.connect(self.selectedRowsChanged)
        else:
            self.view.selectionModel().selectionChanged.connect(
                self.selectedRowsChanged)

    def getSelectedRows(self):
        """
        liste der QModelIndex der ausgewählten zeilen

        :return: list of QModelIndex
        """
        if self.gis_mode:
            return self._gis_layer.selectedFeatureIds()
        else:
            return self.view.selectionModel().selectedRows()

    def selectAllRows(self):

        if self.gis_mode:
            self._gis_layer.selectAll()
        else:
            self.view.selectAll()

        self.view.setFocus()

    def clearSelectedRows(self):
        """
        hebe die auswahl der zeilen auf
        """
        if self.gis_mode:
            self._gis_layer.removeSelection()
        else:
            self.view.selectionModel().clear()

        self.view.setFocus()

    def selectedRowsChanged(self):
        """
        die auswahlt der zeilen hat sich geändert
        """
        print(f'--- selection changed -----------------------')
        self.updateFooter()

        if self.gis_mode:
            if self._gis_layer.selectedFeatureIds() == []:
                self.view.setCornerButtonSelectAll()
            else:
                self.view.setCornerButtonDeselectAll()
        else:
            if self.getSelectedRows() == []:
                self.view.setCornerButtonSelectAll()
            else:
                self.view.setCornerButtonDeselectAll()

    def getProxyIndex(self, index):
        """
        erhalte den filter_proxy index des übergebenen maintable_model index
        :return: QModelIndex
        """
        return self.filter_proxy.mapToSource(index)

    def getDisplayedRowsNumber(self):

        number = 0

        if self.gis_mode:
            number = self._gis_layer.featureCount()
        else:
            number = self.filter_proxy.rowCount()

        return number

    def getSelectedRowsNumber(self):

        number = 0

        if self.gis_mode:
            number = len(self._gis_layer.selectedFeatureIds())
        else:
            if self.view.selectionModel():
                indexes = self.view.selectionModel().selectedRows()
                number = len(indexes)

        return number

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
                self, 'exportiere Tabelle', "",
                "All Files (*);;CSV Files (*.csv)")
            """"""

            """öffne die datei"""
            with open(name, 'w', newline='', encoding='utf8') as f:

                writer = csv.writer(f, delimiter=";")

                if self.gis_mode:
                    # todo: gis-tabellen werden noch nicht korrekt exportiert
                    """hole die spaltenüberschriften"""
                    header_list = []
                    for field in self._gis_layer.fields():
                        if field.alias() == '':
                            header_list.append(field.name())
                        else:
                            header_list.append(field.alias())
                    """"""

                    """schreibe die spaltenüberschriften in die datei"""
                    writer.writerow(list(header_list))
                    """"""

                    for feature in self._gis_layer.getFeatures():
                        writer.writerow(feature.attributes())  # schreibe zeile in datei

                else:
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
        pass

    def removeFilter(self):
        """
        remove here the inputs of the filter widgets to remove the filter
        """
        pass

    def setFilterRemoveBtn(self):
        """
        insert the button to remove the filter into the data_view
        """
        self.uiFilterRemovePbtn = QPushButton()
        self.uiFilterRemovePbtn.setMaximumWidth(30)
        self.uiFilterRemovePbtn.setIcon(
            QIcon(':/svg/resources/icons/filter_remove.svg'))
        self.uiFilterRemovePbtn.setIconSize(QSize(20, 20))
        self.uiFilterRemovePbtn.setFlat(True)
        self.uiFilterRemovePbtn.setVisible(False)

        self.uiFilterRemovePbtn.clicked.connect(self.removeFilter)

        self.uiFilterHlay.addWidget(self.uiFilterRemovePbtn)

    def useFilter(self):
        """
        use the filter
        """
        pass

    def useSubsetString(self):
        """
        wende die definierten filter_strings an
        :return:
        """
        pass

    def testGeneralFilter(self):

        expression = '"status_id"=2'
        self._gis_layer.setSubsetString(expression)

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

    def updateFilterElementsScope(self):
        """
        aktualisiere die filter-elemete des scope-filter (z.b. das filter widget
        ist eine combobox und ein datensatz in der tabelle wurde gelöscht)
        :return:
        """
        pass

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
        :return: dict with custom data
        """
        pass

    def setLayer(self):
        """
        erstelle hier den gis_layer
        :return: QgsVectorlayer
        """
        pass

    def addFeaturesFromMciList(self, mci_list):
        """
        erstelle hier die feature für den layer basierend auf der mci_list
        und füge sie in den data_provider mit 'addFeatures' ein
        :return:
        """
        features_to_add = []

        for mci in mci_list:
            feat = Feature(self._gis_layer.fields(), self)

            self.setFeatureAttributes(feat, mci)
            features_to_add.append(feat)

        # self._gis_layer.data_provider.addFeatures([feat])
        self._gis_layer.data_provider.addFeatures(features_to_add)

    def setFeaturesFromMci(self):
        """
        erstelle hier die feature für den layer basierend auf der mci_list
        und füge sie in den data_provider mit 'addFeatures' ein
        :return:
        """

        pass

    def setColumnVisibility(self, layer, columnName, visible):
        config = layer.attributeTableConfig()
        columns = config.columns()
        for column in columns:
            if column.name == columnName:
                column.hidden = not visible
                break
        config.setColumns(columns)
        layer.setAttributeTableConfig(config)

    def loadData(self, session=None):

        self._mci_list = self.getMciList(session)

    def finalInit(self):
        """
        dinge die direkt nach dem initialisieren durchgeführt werden sollen
        :return:
        """
        pass

    def setFeatureFields(self):
        """
        definiere die QgsField's eines Features inklusive aller zusätzlichen
        Attribute (z.B. alias) und füge sie in die Liste 'feature_fields' ein
        :return: List (feature_fields)
        """
        pass

    def setFeatureAttributes(self, feature, mci):
        """
        setze die attribute eines features
        :param args:
        :return:
        """

        pass

    def updateFeatureAttributes(self, *args):
        """
        aktualisiere die attribute des current_feature
        :param args:
        :return:
        """

    def updateMaintableNew(self, widget_purpose, *args):
        """
        aktualisiere das table_view
        :return:
        """
        # todo: find a better way to check args:
        try:
            accepted_mci = args[0]
            edited_mci = args[1]
        except:
            pass

        if self.gis_mode:
            if widget_purpose == 'add':

                self.updateInstanceNew()

            elif widget_purpose == 'edit':

                if self.current_feature is not None:

                    self.updateFeatureAttributes(args)

                    self._gis_layer.startEditing()

                    self.changeAttributes(self.current_feature,
                                          args[0])

                    self._gis_layer.commitChanges()

                    self.loadData()

            self.view.model().sourceModel().modelChanged.emit()

        else:  # no gis-mode

            if widget_purpose == 'add':

                if self.edit_entity_by == 'mci':
                    self.view.model().sourceModel().layoutAboutToBeChanged.emit()
                    self._mci_list.append(accepted_mci)
                    self.view.model().sourceModel().layoutChanged.emit()

                elif self.edit_entity_by == 'id':

                    for inst in DataView.instance_list:
                        inst.view.model().sourceModel().layoutAboutToBeChanged.emit()
                        inst.loadData()
                        inst.view.model().sourceModel().mci_list = inst._mci_list
                        inst.view.model().sourceModel().layoutChanged.emit()

            elif widget_purpose == 'edit':

                self.view.model().sourceModel().layoutAboutToBeChanged.emit()

                if self.edit_entity_by == 'id':
                    self.dataview_session.refresh(edited_mci)

                self.view.model().sourceModel().layoutChanged.emit()

                for inst in DataView.instance_list:
                    self.updateDataviewInstances(inst)

        #     self.view.model().sourceModel().layoutAboutToBeChanged.emit()
        #     if self.edit_entity_by == 'id':
        #         self.dataview_session.refresh(self.edit_entity)
        #     self.view.model().sourceModel().layoutChanged.emit()
        #
        # self.updateFooter()

    def updateDataviewInstances(self, instance):

        instance.view.model().sourceModel().layoutAboutToBeChanged.emit()

        instance.view.model().sourceModel().layoutChanged.emit()

    # def updateInstanceNew(self):
    #     """
    #     update the given data_view instance
    #     :param instance:
    #     :return:
    #     """
    #
    #     self._gis_layer.startEditing()
    #
    #     self._gis_layer.data_provider.truncate()
    #
    #     with db_session_cm(name='update data_view') as session:
    #         self.loadData(session)
    #
    #         # instance.addFeaturesFromMciList(instance._mci_list)
    #         self.setFeaturesFromMci()
    #     self._gis_layer.commitChanges()
    #
    #     # instance._gis_layer.data_provider.dataChanged.emit()
    #     self._gis_layer.data_provider.reloadData()
    #     self._gis_layer.triggerRepaint()
    #
    #     self.updateFooter()
    #
    # def updateInstance(self, instance):
    #     """
    #     update the given data_view instance
    #     :param instance:
    #     :return:
    #     """
    #
    #     instance._gis_layer.startEditing()
    #
    #     instance._gis_layer.data_provider.truncate()
    #
    #     instance.loadData()
    #     # instance.addFeaturesFromMciList(instance._mci_list)
    #     instance.setFeaturesFromMci()
    #     instance._gis_layer.commitChanges()
    #
    #     # instance._gis_layer.data_provider.dataChanged.emit()
    #     instance._gis_layer.data_provider.reloadData()
    #     instance._gis_layer.triggerRepaint()
    #
    #     instance.updateFooter()

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

    def insertFooterLine(self, label, unit=None, attribute=None, column_id=None, value_width=120, factor=1,
                         decimal=None, filter_col=None, filter_operator=None,
                         filter_criterion=None, column_type=int):
        """
        füge ein footer-elemet (=widget am fuß der tabelle) auf position 0
        in das layout 'uiFooterLinesVlay' ein
        """

        footer_line = self._footer_line(self, label, unit, attribute, column_id, value_width,
                                             factor, decimal, filter_col, filter_operator,
                                             filter_criterion, column_type)

        self.uiFooterLinesVlay.insertWidget(0, footer_line)
        self.footer_list.append(footer_line)

    def updateFooter(self):
        """
        aktualisiere alle footer elemente (zeilenanzahl, summenelemente, ...)
        """
        for line in self.footer_list:
            line.update_footer_line()

        self.displayed_rows = self.getDisplayedRowsNumber()
        self.selected_rows_number = self.getSelectedRowsNumber()

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

            proxy_index = self.getProxyIndex(index)

            self.indexBasedRowEdit(proxy_index)

    def indexBasedRowEdit(self, index):
        """
        define here zones of columns for different edit behaviours

        subclass this method to enable individual settings
        """

        if 0 <= index.column() <= 9999:  # all columns of the model

            if self.gis_mode:
                self.current_feature = self.model.feature(index)
                entity_mci = self.getFeatureMci(self.current_feature)
            else:
                entity_mci = self.getEntityMci(index)

            # self.edit_entity = entity_mci

            entity_wdg_cls = self.get_entity_widget_class(entity_mci)
            entity_wdg = entity_wdg_cls(self)

            if self.edit_entity_by == 'id':

                # entity_wdg.setEntitySession(DbSession())
                # entity_wdg.initEntityWidget()

                self.editRow(entity_wdg,
                             entity_id=self.getEntityId(index),
                             entity_mci=entity_mci,
                             feature=self.current_feature)

            if self.edit_entity_by == 'mci':

                # entity_wdg.setEntitySession(self.dataview_session)
                # entity_wdg.initEntityWidget()

                self.editRow(entity_wdg,
                             entity_mci=entity_mci,
                             feature=self.current_feature)

    def getEntityId(self, index):
        """
        liefere den id des Datensatzes mit dem übergebenen Index

        :param index: QModelIndex
        :return: int (z.B.: self._mci_list[self.getProxyIndex(index).row()].id)
        """

        if self.gis_mode:
            id = self.model.data(self.model.index(index.row(), 0), Qt.EditRole)
        else:
            id = self._mci_list[index.row()].id

        return id

    def getEntityMci(self, index):
        """
        liefere die MCI (Mapped Class Instance) des Datensatzes mit dem
        übergebenen Index

        :param index: QModelIndex
        :return: MCI-Objekt (z.B.: self._mci_list[index.row()])
        """
        # return self.model.mci_list[self.getProxyIndex(index).row()]
        return self._mci_list[index.row()]

    def getFeatureMci(self, feature):
        """
        liefere das mci eines features; subclass wenn notwendig

        :param feature:
        :return:
        """
        return feature.attribute('mci')[0]


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
        return self._custom_dataview_data

    def editRow(self, entity_widget, entity_id=None, entity_mci=None, feature=None):
        """
        edit one table row;
        you could use the table_index to get the column (e.g. to open different
        item-widgets on different columns for editing)

        :return:
        """
        if entity_id:
            entity_widget.setEntitySession(DbSession())
            entity_widget.editEntity(entity_id=entity_id,
                                     feature=feature,
                                     edited_mci=entity_mci)

        # if entity_mci:
        else:
            entity_widget.setEntitySession(self.dataview_session)
            entity_widget.editEntity(entity_mci=entity_mci)

        """open the entity_widget_class in a dialog"""
        self.openDialog(entity_widget)
        """"""

    def get_entity_widget_class(self, entity_mci=None):
        """
        gebe die klasse des entity_widgets zurück;
        falls unterschiedliche typen im daten-model definiert sind kann auch
        der rückgabewert von 'getEntityTypeWdgCls' verwendet werden;
        oder es kann hier eine komplett eigenständige methode definiert werden
        (z.B. siehe 'kontakt_main')
        :param entity_mci:
        :return:
        """

        return self.entity_widget_class

    def getEntityTypeWdgCls(self, entity_mci):
        """
        falls es für das entity_mci verschiedene typen gibt, dann gebe hier die
        widget-klasse für dieses entity_mci zurück
        :param entity_mci:
        :return:
        """

        if hasattr(entity_mci, 'rel_type'):
            """get the module and the widget_class from the
            type_data_instance"""

            module = entity_mci.rel_type.module
            widget_class = entity_mci.rel_type.type_class

            """import the widget_class and make a instance"""
            item_module = __import__(module, fromlist=[widget_class])
            wdg_class = getattr(item_module, widget_class)
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

    def deleteCheck(self, mci):
        """
        return True if the given mci can be deleted; e.g. check if the mci is
        used in some relations
        :param mci:
        :return:
        """
        return True

    def delRowMain(self):
        """
        einstiegs-metode zum löschen einer oder mehrerer zeilen dieser tabellen
        """
        if self.gis_mode:
            sel_features = self._gis_layer.selectedFeatures()

            if sel_features:

                with edit(self._gis_layer):
                    for feat in sel_features:
                        for mci in self._mci_list:
                            if feat.attribute('id') == mci.id:

                                if self.deleteCheck(mci):
                                    try:
                                        self.dataview_session.delete(mci)
                                    except IntegrityError:  # mci is used
                                        self.can_not_delete_msg(
                                            self.getFeatureDeleteInfo(feat))
                                    else:
                                        self._mci_list.remove(mci)
                                        self._gis_layer.data_provider.deleteFeatures(
                                            [feat.id()])

                                else:
                                    self.can_not_delete_msg(
                                        self.getFeatureDeleteInfo(feat))

                self._gis_layer.data_provider.dataChanged.emit()

            else:
                self.no_row_selected_msg()

        else:  # no gis-mode

            sel_rows_idx = self.getSelectedRows()

            del_mci = [self._mci_list[self.getProxyIndex(r).row()]
                       for r in sel_rows_idx]

            self.view.model().sourceModel().layoutAboutToBeChanged.emit()

            for mci in del_mci:
                self.delMci(mci)

            self.view.model().sourceModel().layoutChanged.emit()

        self.clearSelectedRows()
        self.updateFooter()

    def delMci(self, mci):

        try:
            with db_session_cm(name='delete mci from data_view') as session:
                session.delete(mci)
        except IntegrityError:  # mci is used
            print('...........................................cannot delete')
            raise
        else:
            self._mci_list.remove(mci)

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
        msgbox.setInformativeText(self._delete_text[0] + '\n\n' + delete_info
                                  + '\n\n' + self._delete_text[1])
        msgbox.setStandardButtons(QMessageBox.Ok)
        # msgbox.centerInGivenWdg(self.view)
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

        if self._type_mc:
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
            """nehme das hinterlegte entity_widget"""
            entity_widget = self.entity_widget_class(self)
            mci = self._entity_mc()
            """"""

        entity_widget.purpose = 'add'

        self.editRow(entity_widget=entity_widget,
                     entity_mci=mci)

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

    def updateMaintable(self):
        """
        aktualisiere den maintable;
        """
        self.updateFooter()


class GisSortFilterProxyModel(QgsAttributeTableFilterModel):

    def __init__(self, canvas, sourceModel, parent=None):
        super().__init__(canvas, sourceModel, parent)

        self.parent = parent


class SortFilterProxyModel(QSortFilterProxyModel):
    """
    baseclass für ein QSortFilterProxyModel in dieser tabelle
    """
    def __init__(self, parent):
        QSortFilterProxyModel.__init__(self, parent)

        self.parent = parent
        self.filter_rows_with_elements = {}

        self.layoutChanged.connect(self.selectionChanged)

    def selectionChanged(self):

        self.parent.updateFooter()
        print(f'layout changed!')

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
        if self.parent.useFilterScope(source_row, source_parent) == False:
            return False

        return True
