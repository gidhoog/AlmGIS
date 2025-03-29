import sys

from PyQt5.QtCore import QVariant
from qgis._core import QgsVectorLayerCache
from qgis._gui import QgsAttributeTableFilterModel, QgsMapCanvas
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsField,
    QgsProject,
)
from qgis.gui import QgsAttributeTableView, QgsAttributeTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# Sample data
places_data = [
    {"id": 1, "name": "City A", "population": 1000000},
    {"id": 2, "name": "City B", "population": 500000},
]

lakes_data = [
    {"id": 1, "name": "Lake A", "geom": "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"},
    {"id": 2, "name": "Lake B", "geom": "POLYGON((2 2, 3 2, 3 3, 2 3, 2 2))"},
]


# Function to create a QgsVectorLayer for places (no geometry)
def create_places_layer(data):
    layer = QgsVectorLayer("Point?crs=EPSG:4326", "Places Layer", "memory")
    provider = layer.dataProvider()
    provider.addAttributes([
        QgsField("id", QVariant.Int),
        QgsField("name", QVariant.String),
        QgsField("population", QVariant.Int),
    ])
    layer.updateFields()

    for place in data:
        feature = QgsFeature()
        feature.setAttributes([place["id"], place["name"], place["population"]])
        provider.addFeature(feature)

    return layer


# Function to create a QgsVectorLayer for lakes (with geometry)
def create_lakes_layer(data):
    layer = QgsVectorLayer("Polygon?crs=EPSG:4326", "Lakes Layer", "memory")
    provider = layer.dataProvider()
    provider.addAttributes([
        QgsField("id", QVariant.Int),
        QgsField("name", QVariant.String),
    ])
    layer.updateFields()

    for lake in data:
        feature = QgsFeature()
        feature.setAttributes([lake["id"], lake["name"]])
        feature.setGeometry(QgsGeometry.fromWkt(lake["geom"]))
        provider.addFeature(feature)

    return layer


# Main Application Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGIS Standalone Application")

        # Create the QGIS layers
        self.places_layer = create_places_layer(places_data)
        self.lakes_layer = create_lakes_layer(lakes_data)

        # Add layers to the QGIS project
        QgsProject.instance().addMapLayer(self.places_layer)
        QgsProject.instance().addMapLayer(self.lakes_layer)

        # Create the GUI layout
        layout = QVBoxLayout()

        # Create and populate the attribute table view for places
        places_table_view = self.create_attribute_table_view(self.places_layer)
        layout.addWidget(places_table_view)

        # Create and populate the attribute table view for lakes
        lakes_table_view = self.create_attribute_table_view(self.lakes_layer)
        layout.addWidget(lakes_table_view)

        # Set up the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_attribute_table_view(self, layer):
        """Creates a QgsAttributeTableView for a given layer."""
        vc = QgsVectorLayerCache(layer, 10000)
        model = QgsAttributeTableModel(vc)
        model.loadLayer()  # Load data into the model

        fpm = QgsAttributeTableFilterModel(QgsMapCanvas(), model)

        table_view = QgsAttributeTableView()
        table_view.setModel(fpm)  # Set the model for the table view

        return table_view

# Run the application
if __name__ == "__main__":

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
