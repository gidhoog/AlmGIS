
from PyQt5.QtCore import Qt, QSize, QAbstractItemModel, QModelIndex

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsField

from core.gis_layer import setLayerStyle
from core.main_gis import MainGis

from core.scopes.gst import gst_version_UI


class GstVersion(gst_version_UI.Ui_GstVersion):
    """
    baseclass für eine gst-version
    """

    # _alm_bnr = 0
    #
    # @property  # getter
    # def alm_bnr(self):
    #
    #     if self.uiAlmBnrLedit.text() != '':
    #         self._alm_bnr = int(self.uiAlmBnrLedit.text())
    #     else:
    #         self._alm_bnr = ''
    #     return self._alm_bnr
    #
    # @alm_bnr.setter
    # def alm_bnr(self, value):
    #
    #     if value == 'None' or value == None:
    #         self._alm_bnr = ''
    #     else:
    #         self.uiAlmBnrLedit.setText(str(value))
    #         self._alm_bnr = value


    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
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