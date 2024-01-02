from core.gis_item import GisItem
from PyQt5.QtGui import QColor


class AbgrenzungItem(GisItem):
    """
    ein Koppel-Item (=QStandardItem + Gis) zur Verwendung in Models
    """

    def __init__(self, data_instance=None):
        super().__init__(data_instance)

        self.setData(data_instance.jahr, GisItem.Name_Role)

        self.setData(QColor(70, 160, 240), GisItem.Color_Role)


class KomplexItem(GisItem):
    """
    ein Koppel-Item (=QStandardItem + Gis) zur Verwendung in Models
    """

    def __init__(self, data_instance=None):
        super().__init__(data_instance)

        self.setData(data_instance.rel_komplex_name.name, GisItem.Name_Role)

        self.setData(QColor(70, 160, 240), GisItem.Color_Role)

    # @staticmethod
    # def clone(self) -> 'QStandardItem':
    #     return KomplexItem()