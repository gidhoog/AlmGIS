from core.gis_item import GisItem
from PyQt5.QtGui import QColor


class AbgrenzungItem(GisItem):
    """
    ein Koppel-Item (=QStandardItem + Gis) zur Verwendung in Models
    """



    def __init__(self, data_instance=None):
        super().__init__(data_instance)

        self.setData(data_instance.jahr, GisItem.Jahr_Role)
        self.setData(data_instance.bearbeiter, GisItem.Bearbeiter_Role)

        self.setData(data_instance.erfassungsart_id, GisItem.ErfassungsArtId_Role)
        self.setData(data_instance.rel_erfassungsart.name, GisItem.ErfassungsArtName_Role)
        self.setData(data_instance.status_id, GisItem.StatusId_Role)
        self.setData(data_instance.rel_status.name_short, GisItem.StatusName_Role)

        self.setData(data_instance.anmerkung, GisItem.Anmerkung_Role)
        self.setData(data_instance.inaktiv, GisItem.Inactive_Role)

        self.setData(QColor(70, 160, 240), GisItem.Color_Role)

    def getItemData(self, data_instance):
        super().getItemData(data_instance)

        data_instance.jahr = self.data(GisItem.Jahr_Role)
        data_instance.bearbeiter = self.data(GisItem.Bearbeiter_Role)
        data_instance.erfassungsart_id = self.data(GisItem.ErfassungsArtId_Role)
        data_instance.status_id = self.data(GisItem.StatusId_Role)
        data_instance.anmerkung = self.data(GisItem.Anmerkung_Role)
        data_instance.inaktiv = self.data(GisItem.Inactive_Role)

class KomplexItem(GisItem):
    """
    ein Koppel-Item (=QStandardItem + Gis) zur Verwendung in Models
    """

    def __init__(self, data_instance=None):
        super().__init__(data_instance)

        self.setData(data_instance.rel_komplex_name.name, GisItem.Name_Role)
        self.setData(data_instance.komplex_name_id, GisItem.KomplexNameId_Role)

        self.setData(QColor(70, 160, 240), GisItem.Color_Role)

    def getItemData(self, data_instance):
        super().getItemData(data_instance)

        data_instance.komplex_name_id = self.data(GisItem.KomplexNameId_Role)

    # @staticmethod
    # def clone(self) -> 'QStandardItem':
    #     return KomplexItem()