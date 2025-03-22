from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QModelIndex
from qgis.core import QgsVectorLayer, QgsVectorLayerCache, QgsFeature
from qgis.gui import QgsAttributeTableModel, QgsAttributeTableView
from qgis.utils import iface


# Custom Attribute Table Model
class CustomAttributeTableModel(QgsAttributeTableModel):
    def __init__(self, layer_cache, parent=None):
        super().__init__(layer_cache, parent)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            # Get the original data
            original_data = super().data(index, role)
            column = index.column()

            # Customize data display for column 1 (second column)
            if column == 1:  # Example: Add a prefix to the second column's values
                return f"Custom: {original_data}"

        # For all other roles or columns, return the original data
        return super().data(index, role)

    def flags(self, index: QModelIndex):
        # Make all items editable (optional)
        return super().flags(index) | Qt.ItemIsEditable


# Dialog for displaying the custom attribute table
class AttributeTableDialog(QDialog):
    def __init__(self, layer, parent=None):
        super().__init__(parent)
        self.layer = layer
        self.setWindowTitle("Custom Attribute Table")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create the attribute table view
        self.table_view = QgsAttributeTableView(self)
        layout.addWidget(self.table_view)

        # Set up the custom model with a layer cache
        layer_cache = QgsVectorLayerCache(self.layer,
                                          1000)  # Cache up to 1000 features
        self.custom_model = CustomAttributeTableModel(layer_cache)
        self.table_view.setModel(self.custom_model)

        # Add a close button at the bottom of the dialog
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)


# Main function to run the script in QGIS
def run_custom_attribute_table():
    # Get the active layer from QGIS
    layer = iface.activeLayer()

    if not layer or not isinstance(layer, QgsVectorLayer):
        iface.messageBar().pushMessage("Error", "Please select a vector layer",
                                       level=3)  # Level 3 = Critical
        return

    # Open the custom attribute table dialog for the selected layer
    dialog = AttributeTableDialog(layer)
    dialog.exec_()


# Run the script (this will execute when you paste it into the QGIS Python Console)
run_custom_attribute_table()
