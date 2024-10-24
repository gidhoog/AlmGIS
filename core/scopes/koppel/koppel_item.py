from core.gis_item import GisItem
from qgis.PyQt.QtGui import QColor


class KoppelItem(GisItem):
    """
    ein Koppel-Item (=QStandardItem + Gis) zur Verwendung in Models
    """

    def __init__(self, data_instance=None):
        super().__init__(data_instance)

        self.setData(data_instance.nr, GisItem.Nr_Role)
        self.setData(data_instance.name, GisItem.Name_Role)
        self.setData(data_instance.nicht_weide, GisItem.NichtWeide_Role)
        self.setData(data_instance.bearbeiter, GisItem.Bearbeiter_Role)
        self.setData(data_instance.anmerkung, GisItem.Anmerkung_Role)
        self.setData(data_instance.geometry, GisItem.Geometry_Role)

        self.setData(QColor(240, 160, 20), GisItem.Color_Role)

    def getItemData(self, data_instance):
        super().getItemData(data_instance)

        data_instance.nr = self.data(GisItem.Nr_Role)
        data_instance.name = self.data(GisItem.Name_Role)
        data_instance.nicht_weide = self.data(GisItem.NichtWeide_Role)
        data_instance.bearbeiter = self.data(GisItem.Bearbeiter_Role)
        data_instance.anmerkung = self.data(GisItem.Anmerkung_Role)
        data_instance.geometry = self.data(GisItem.Geometry_Role)

    # @staticmethod
    # def clone(self) -> 'QStandardItem':
    #     return KoppelItem()