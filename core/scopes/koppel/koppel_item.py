from core.gis_item import GisItem
from PyQt5.QtGui import QColor


class KoppelItem(GisItem):
    """
    ein Koppel-Item (=QStandardItem + Gis) zur Verwendung in Models
    """

    def __init__(self, data_instance=None):
        super().__init__()

        if data_instance != None:

            self.setData(data_instance, GisItem.Instance_Role)

        self.setData(QColor(240, 160, 20), GisItem.Color_Role)

    # @staticmethod
    # def clone(self) -> 'QStandardItem':
    #     return KoppelItem()