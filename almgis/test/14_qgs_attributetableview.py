import sys

from PyQt5.QtCore import Qt
from qgis._core import QgsVectorLayerCache
from qgis._gui import QgsAttributeTableModel, QgsAttributeTableFilterModel, \
    QgsMapCanvas
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsPointXY
)
from qgis.PyQt.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from qgis.gui import QgsAttributeTableView
from qgis.PyQt.QtCore import QVariant

# # Initialize QGIS application
# QgsApplication.setPrefixPath("/path/to/qgis/installation", True)
# qgs = QgsApplication([], True)
# qgs.initQgis()

# # Create the PyQt application
# app = QApplication([])

# Create a memory vector layer
layer = QgsVectorLayer("Point?crs=epsg:4326", "Memory Layer", "memory")
provider = layer.dataProvider()

# Add fields (attributes) to the layer
provider.addAttributes([
    QgsField("Name", QVariant.String),
    QgsField("Age", QVariant.Int),
    QgsField("Height", QVariant.Double)
])
layer.updateFields()

# Add features (data) to the layer
feature = QgsFeature()
feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(10, 10)))
feature.setAttributes(["Alice", 30, 5.5])
provider.addFeatures([feature])

feature2 = QgsFeature()
feature2.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(20, 20)))
feature2.setAttributes(["Bob", 25, 6.0])
provider.addFeatures([feature2])

layer.updateExtents()

class TestModel(QgsAttributeTableModel):
    def __init__(self, layer_cache, parent=None):
        super().__init__(layer_cache, parent)

    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            # Set alignment for the "Age" column (column index 1)
            if index.column() == 1:
                return Qt.AlignHCenter | Qt.AlignVCenter

        if role == Qt.DisplayRole:
            # Append a string to the "Name" column (column index 0)
            if index.column() == 0:
                current_value = super().data(index, role)
                return f"{current_value} - Edited"

        # Default behavior for other roles
        return super().data(index, role)

# Create a main window to display the attribute table
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGIS Attribute Table Example")
        self.resize(800, 600)

        # Create a widget and layout for the table view
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        # Create and configure the attribute table view
        self.vc = QgsVectorLayerCache(layer, 10000)
        # self.model = QgsAttributeTableModel(self.vc)
        self.model = TestModel(self.vc)
        self.model.loadLayer()
        self.fpm = QgsAttributeTableFilterModel(QgsMapCanvas(), self.model)
        self.attribute_table_view = QgsAttributeTableView(self)
        self.attribute_table_view.setModel(self.fpm)
        self.layout.addWidget(self.attribute_table_view)

        self.setCentralWidget(self.widget)


# Initialize QGIS Application
qgs = QgsApplication([], True)
qgs.setPrefixPath("/var/lib/flatpak/app/org.qgis.qgis",
                  True)  # Adjust path based on your QGIS installation

qgs.initQgis()
# app = QApplication(sys.argv)

# Create and show the main window
window = MainWindow()
window.show()

# Execute the application loop
# app.exec_()

# Exit QGIS application
# qgs.exitQgis()
sys.exit(qgs.exec_())
