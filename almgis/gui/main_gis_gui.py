from PyQt5.QtCore import QModelIndex, Qt, QVariant
from qga.gui.main_gis import QgaMainGisGui
from qgis._core import QgsLayerTreeModel, QgsLayerTreeModelLegendNode



# class AlmLayerTreeModel(QgsLayerTreeModel):
#
#     def __init__(self, root):
#         super().__init__(root)
#
#     def columnCount(self, parent=QModelIndex()):
#         return 3  # Default + 2 custom columns [web:3]
#
#     def headerData(self, section, orientation, role=Qt.DisplayRole):
#         if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#             return {
#                 0: "Layers",
#                 1: "Status",
#                 2: "Count"
#             }.get(section, super().headerData(section, orientation, role))
#         return super().headerData(section, orientation, role)
#
#     def data(self, index, role=Qt.DisplayRole):
#         if not index.isValid():
#             return QVariant()
#
#         if index.column() == 0:
#             return super().data(index, role)  # Default layer tree column
#
#         node = self.index2node(index)
#         if not isinstance(node, QgsLayerTreeModelLegendNode) and \
#                 index.column() == 1 and role == Qt.DisplayRole:
#             # Status column example
#             layer = node.layer() if hasattr(node, 'layer') else None
#             return "✓" if layer and layer.featureCount() > 0 else "Empty"
#
#         elif index.column() == 2 and role == Qt.DisplayRole:
#             # Feature count column
#             layer = node.layer() if hasattr(node, 'layer') else None
#             return layer.featureCount() if layer else 0
#
#         return QVariant()
