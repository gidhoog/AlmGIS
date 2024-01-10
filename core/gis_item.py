
from qgis.PyQt.QtGui import QStandardItem
from PyQt5.QtCore import Qt


class GisItem(QStandardItem):
    """
    Subclass eines QStandardItems erweitert mit zusätzlichen Gis-Informationen
    """

    Instance_Role = Qt.UserRole + 10
    Feature_Role = Qt.UserRole + 11
    Current_Role = Qt.UserRole + 12  # 0 für aktuelle und 1 für alte versionen

    Color_Role = Qt.UserRole + 20

    Nr_Role = Qt.UserRole + 100
    Name_Role = Qt.UserRole + 101

    Layer_Role = Qt.UserRole + 199
    Geometry_Role = Qt.UserRole + 200

    def __init__(self, data_instance=None):
        super().__init__()

        if data_instance != None:

            self.setData(data_instance, GisItem.Instance_Role)

            # self.setData(data_instance.nr, GisItem.Nr_Role)
            # self.setData(data_instance.name, GisItem.Name_Role)


    # @staticmethod
    # def clone(self) -> 'QStandardItem':
    #     return GisItem()

    def type(self) -> int:
        return self.data(Qt.UserRole + 1000)
