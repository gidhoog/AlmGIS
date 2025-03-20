# https://www.perplexity.ai/search/81fc3e06-c35d-4bc1-a483-9677a341cfce

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
    QHBoxLayout, QLineEdit, QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel
from qgis._core import QgsVectorLayerCache
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, \
    QgsProject
from qgis.gui import QgsAttributeTableModel, QgsMapCanvas


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None


class UnifiedFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, layer=None, parent=None):
        super().__init__(parent)
        self.filter_text = ""
        self.layer = layer

    def setFilterText(self, text):
        self.filter_text = text.lower()
        # self.invalidateFilter()

        # If filtering a QgsVectorLayer (via QgsAttributeTableModel)
        if self.layer:
            if text:
                expression = f"\"name\" ILIKE '%{text}%'"
            else:
                expression = ""
            self.layer.setSubsetString(expression)

    def filterAcceptsRow(self, source_row, source_parent):
        if not self.filter_text:
            return True
        for column in range(self.sourceModel().columnCount()):
            index = self.sourceModel().index(source_row, column, source_parent)
            data = self.sourceModel().data(index, Qt.DisplayRole)
            if self.filter_text in str(data).lower():
                return True
        return False


class FilteredTableView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.filter_input = QLineEdit(self)
        self.table_view = QTableView(self)
        self.proxy_model = None

        self.layout.addWidget(self.filter_input)
        self.layout.addWidget(self.table_view)

    def setModel(self, model, layer=None):
        # Create a unified filter proxy model
        self.proxy_model = UnifiedFilterProxyModel(layer=layer)
        self.proxy_model.setSourceModel(model)
        self.table_view.setModel(self.proxy_model)

        # Connect the filter input to update the proxy model
        self.filter_input.textChanged.connect(self.proxy_model.setFilterText)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unified Filtered Tables Example")
        self.setGeometry(100, 100, 1200, 600)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Set up map canvas
        self.map_canvas = QgsMapCanvas()
        main_layout.addWidget(self.map_canvas, 2)

        # First table: QgsAttributeTableModel with filtering
        self.filtered_table1 = FilteredTableView()
        main_layout.addWidget(self.filtered_table1, 1)

        # Create a sample vector layer
        self.layer = QgsVectorLayer(
            "Point?crs=EPSG:4326&field=id:integer&field=name:string",
            "test_layer", "memory")

        features = [
            (1, "New York City", QgsPointXY(-74.006, 40.7128)),
            (2, "Los Angeles", QgsPointXY(-118.2437, 34.0522)),
            (3, "Chicago", QgsPointXY(-87.6298, 41.8781)),
            (4, "Houston", QgsPointXY(-95.3698, 29.7604)),
            (5, "Phoenix", QgsPointXY(-112.0740, 33.4484))
        ]

        for id_, name_, point_ in features:
            feat = QgsFeature()
            feat.setAttributes([id_, name_])
            feat.setGeometry(QgsGeometry.fromPointXY(point_))
            self.layer.dataProvider().addFeature(feat)

        # Add layer to project and map canvas
        QgsProject.instance().addMapLayer(self.layer)

        # Set up map canvas with the layer
        self.map_canvas.setLayers([self.layer])
        self.map_canvas.setExtent(self.layer.extent())

        # Set up attribute table model and connect it to the filtered table
        self.layer_cache = QgsVectorLayerCache(self.layer,
                                               self.layer.featureCount())
        attribute_table_model = QgsAttributeTableModel(self.layer_cache)
        attribute_table_model.loadLayer()

        # Pass the model and vector layer to the filtered table view
        self.filtered_table1.setModel(attribute_table_model, layer=self.layer)

        # Second table: Custom QAbstractTableModel with filtering
        custom_data = [
            ["Alice", "25", "Engineer"],
            ["Bob", "30", "Designer"],
            ["Charlie", "35", "Manager"],
            ["David", "28", "Developer"],
            ["Eve", "32", "Analyst"]
        ]

        custom_model = CustomTableModel(custom_data)

        # Create second filtered table view and add it to layout
        self.filtered_table2 = FilteredTableView()

        main_layout.addWidget(self.filtered_table2)

        # Pass the custom model to the second filtered table view
        self.filtered_table2.setModel(custom_model)


if __name__ == "__main__":
    # Initialize QGIS application
    from qgis.core import QgsApplication

    qgs = QgsApplication([], True)
    qgs.setPrefixPath("C:/work/_anwendungen/OSGeo4W/apps/qgis-ltr",
                          True)
    qgs.initQgis()

    # Create and show the main window
    # app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # # Run the application
    # exit_code = app.exec_()
    #
    # # Exit QGIS
    # qgs.exitQgis()
    #
    # sys.exit(exit_code)
    sys.exit(qgs.exec_())
