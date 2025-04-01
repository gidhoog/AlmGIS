import sys

from qgis._gui import QgsAttributeTableView
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsPointXY,
    QgsProject
)
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from qgis.gui import QgsMapCanvas

# # Initialize QGIS application
# QgsApplication.setPrefixPath("/path/to/qgis/installation", True)
# qgs = QgsApplication([], False)
# qgs.initQgis()


# Base class for features with filtering capability
class CustomFeature(QgsFeature):
    def __init__(self, fields):
        super().__init__(fields)
        self.fields = fields

    def set_attributes(self, attributes):
        self.setAttributes(attributes)

    def filter_by_attribute(self, attribute_name, value):
        """Filter the feature based on an attribute value."""
        return self.attribute(attribute_name) == value


# Base class for fields
class CustomField(QgsField):
    def __init__(self, name, field_type):
        super().__init__(name, field_type)


# Factory to create vector layers
class VectorLayerFactory:
    @staticmethod
    def create_layer(layer_name, crs="EPSG:4326"):
        layer = QgsVectorLayer(f"Point?crs={crs}", layer_name, "memory")
        provider = layer.dataProvider()

        # Add fields to the layer
        fields = [
            CustomField("name", QVariant.String),
            CustomField("age", QVariant.Int),
            CustomField("height", QVariant.Double)
        ]
        provider.addAttributes(fields)
        layer.updateFields()

        return layer


# Create a standalone PyQt5 application with Map Canvas
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create vector layer using the factory
        self.layer = VectorLayerFactory.create_layer("Custom Layer")

        # Add features to the layer
        provider = self.layer.dataProvider()
        features_data = [
            {"geometry": QgsGeometry.fromPointXY(QgsPointXY(10, 10)),
             "attributes": ["Alice", 30, 1.65]},
            {"geometry": QgsGeometry.fromPointXY(QgsPointXY(20, 20)),
             "attributes": ["Bob", 25, 1.80]},
            {"geometry": QgsGeometry.fromPointXY(QgsPointXY(30, 30)),
             "attributes": ["Charlie", 35, 1.75]}
        ]

        features = []
        for data in features_data:
            feature = CustomFeature(self.layer.fields())
            feature.setGeometry(data["geometry"])
            feature.set_attributes(data["attributes"])
            features.append(feature)

        provider.addFeatures(features)
        self.layer.updateExtents()

        # Add the layer to the project
        QgsProject.instance().addMapLayer(self.layer)

        # Initialize Map Canvas and set up layers
        self.init_map_canvas()

    def init_map_canvas(self):
        self.canvas = QgsMapCanvas()

        # Set canvas extent and layers
        self.canvas.setExtent(self.layer.extent())
        self.canvas.setLayers([self.layer])

        # table_view = QgsAttributeTableView()
        # table_view.setLayer(self.layer)

        # Embed canvas into GUI layout
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(self.canvas)
        # layout.addWidget(table_view)

        self.setCentralWidget(widget)
        self.setWindowTitle("PyQGIS Standalone Application with Map Canvas")
        self.resize(800, 600)


# Run the application
if __name__ == "__main__":
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

    # app = QApplication([])
    # window = MainWindow()
    # window.show()
    #
    # app.exec_()
    #
    # # Clean up QGIS resources
    # qgs.exitQgis()
