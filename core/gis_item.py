
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

    Id_Role = Qt.UserRole + 99
    Nr_Role = Qt.UserRole + 100
    Name_Role = Qt.UserRole + 101
    Jahr_Role = Qt.UserRole + 102
    Bearbeiter_Role = Qt.UserRole + 103
    ErfassungsArtId_Role = Qt.UserRole + 104
    StatusId_Role = 105
    Anmerkung_Role = Qt.UserRole + 106
    Inactive_Role = Qt.UserRole + 107

    KomplexNameId_Role = Qt.UserRole + 108

    NichtWeide_Role = Qt.UserRole + 109

    Layer_Role = Qt.UserRole + 199
    Geometry_Role = Qt.UserRole + 200

    def __init__(self, data_instance=None):
        super().__init__()

        if data_instance != None:

            self.setData(data_instance, GisItem.Instance_Role)

            self.setData(data_instance.id, GisItem.Id_Role)

            # self.setData(data_instance.nr, GisItem.Nr_Role)
            # self.setData(data_instance.name, GisItem.Name_Role)

    def getItemData(self, data_instance):

        data_instance.id = self.data(GisItem.Id_Role)


    # @staticmethod
    # def clone(self) -> 'QStandardItem':
    #     return GisItem()

    def type(self) -> int:
        return self.data(Qt.UserRole + 1000)
