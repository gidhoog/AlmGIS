
from qgis.PyQt.QtGui import QStandardItem
from PyQt5.QtCore import Qt


class GisItem(QStandardItem):
    """
    Subclass eines QStandardItems erweitert mit zusätzlichen Gis-Informationen
    """

    Instance_Role = Qt.UserRole + 10
    Feature_Role = Qt.UserRole + 11

    Color_Role = Qt.UserRole + 20

    # @staticmethod
    # def clone(self) -> 'QStandardItem':
    #     return GisItem()

    def type(self) -> int:
        return self.data(Qt.UserRole + 1000)