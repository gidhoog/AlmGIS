
from PyQt5.QtCore import Qt, QSize, QAbstractItemModel, QModelIndex

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsField

from core.entity import Entity
from core.gis_layer import setLayerStyle
from core.main_gis import MainGis

from core.scopes.gst import gst_version_UI


class GstVersion(gst_version_UI.Ui_GstVersion, Entity):
    """
    baseclass für eine gst-version
    """

    _ez = 0
    _ezkg = 0
    _area_gb = 0
    _datenstand = ''
    _importzeit = ''

    @property  # getter
    def ez(self):

        return self._ez

    @ez.setter
    def ez(self, value):

        self.uiEZLbl.setText(str(value))
        self._ez = value

    @property  # getter
    def ezkg(self):

        return self._ezkg

    @ezkg.setter
    def ezkg(self, value):

        kgname = self.data_instance.rel_alm_gst_ez.rel_kat_gem.kgname

        self.uiEzKgLbl.setText(str(value) + ' - ' + kgname)
        self._ezkg = value

    @property  # getter
    def area_gb(self):

        return self._area_gb

    @area_gb.setter
    def area_gb(self, value):

        val = ('{:.4f}'.format(round(float(value) / 10000, 4))
               .replace(".", ","))
        self.uiAreaGbLbl.setText(str(val) + 'ha')

        self._area_gb = value

    @property  # getter
    def datenstand(self):

        return self._datenstand

    @datenstand.setter
    def datenstand(self, value):

        self.uiDatenstandLbl.setText(value)
        self._datenstand = value

    @property  # getter
    def importzeit(self):

        return self._importzeit

    @importzeit.setter
    def importzeit(self, value):

        self.uiImportZeitLbl.setText(value)
        self._importzeit = value


    def __init__(self, parent=None):
        super(__class__, self).__init__()
        self.setupUi(self)


        # """erzeuge ein main_gis widget und füge es in ein GisDock ein"""
        # self.uiGisDock = GisDock(self)
        # self.guiMainGis = MainGis(self.uiGisDock, self)
        # self.guiMainGis.komplex_jahr = 2018
        # self.addDockWidget(Qt.RightDockWidgetArea, self.uiGisDock)
        # self.uiGisDock.setWidget(self.guiMainGis)
        # """"""
        #
        # """setzte den 'scope_id'; damit die richtigen layer aus dem
        # daten_model 'BGisScopeLayer' für dieses main_gis widget geladen werden"""
        # self.guiMainGis.scope_id = 1
        # """"""
        #
        # """erzeuge einen Layer für die Koppeln und füge ihn ins canvas ein"""
        # self.koppel_layer = QgsVectorLayer("Polygon?crs=epsg:31259", "Koppeln", "memory")
        # self.koppel_dp = self.koppel_layer.dataProvider()
        #
        # # add fields
        # self.koppel_dp.addAttributes([QgsField("id", QVariant.Int),
        #                               QgsField("name", QVariant.String),
        #                               QgsField("bearbeiter", QVariant.String),
        #                               QgsField("aw_ha", QVariant.String),
        #                               QgsField("aw_proz", QVariant.String),
        #                               QgsField("area", QVariant.String)])
        #
        # self.koppel_layer.updateFields()  # tell the vector layer to fetch changes from the provider
        #
        # self.koppel_layer.back = False
        # self.koppel_layer.base = True
        # setLayerStyle(self.koppel_layer, 'koppel_gelb')
        # self.guiMainGis.addLayer(self.koppel_layer)
        # """"""
        #
        # """erzeuge einen Layer für die Komplexe und füge ihn ins canvas ein"""
        # self.komplex_layer = QgsVectorLayer("Polygon?crs=epsg:31259", "Komplexe", "memory")
        # self.komplex_dp = self.komplex_layer.dataProvider()
        # self.komplex_layer.back = False
        # self.komplex_layer.base = True
        # setLayerStyle(self.komplex_layer, 'komplex_rot')
        # self.guiMainGis.addLayer(self.komplex_layer)
        # """"""

    def mapData(self):
        super().mapData()

        self.ez = self.data_instance.rel_alm_gst_ez.ez
        self.ezkg = self.data_instance.rel_alm_gst_ez.kgnr
        self.datenstand = self.data_instance.rel_alm_gst_ez.datenstand
        self.importzeit = self.data_instance.rel_alm_gst_ez.import_time

