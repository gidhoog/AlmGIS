
from random import randrange

from qgis.PyQt.QtWidgets import QHBoxLayout, QWidget, QLabel, QDockWidget
from qgis.PyQt.QtCore import Qt, QVariant
from qgis.PyQt.QtGui import QColor

from qgis.core import (QgsVectorLayer, QgsField, QgsFeature, QgsGeometry,
                       QgsLayerTreeGroup, QgsSymbol, QgsSimpleFillSymbolLayer,
                       QgsRendererCategory, QgsCategorizedSymbolRenderer)

from geoalchemy2.shape import to_shape

from core.entity import Entity
from core.gis_layer import setLayerStyle
from core.main_gis import MainGis

from core.scopes.gst import (gst_UI, gst_version_banu_UI,
                             gst_version_eigentuemer_UI)
from core.scopes.gst.gst_version import GstVersion


class Gst(gst_UI.Ui_Gst, Entity):
    """
    baseclass für ein grundstück
    """

    _gst = ''
    _kgnr = ''
    _kggst = 0

    @property  # getter
    def gst(self):

        return self._gst

    @gst.setter
    def gst(self, value):

        self._gst = value
        self.uiGstLbl.setText(value)

    @property  # getter
    def kgnr(self):

        return self._kgnr

    @kgnr.setter
    def kgnr(self, value):

        kgname = self._entity_mci.rel_kat_gem.kgname

        self.uiKgLbl.setText(str(value) + ' - ' + kgname)
        self._kgnr = value


    def __init__(self, parent=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

    def mapData(self):
        super().mapData()

        self.gst = self._entity_mci.gst
        self.kgnr = self._entity_mci.kgnr

    def addGstLayerCurrent(self):
        """
        füge das letzt-aktuelle Gst in die Kartenansicht ein
        :return:
        """

        gst_version_current = self.gst_versions_sorted[0]
        self.gst_layer_current = QgsVectorLayer(
            "Polygon?crs=epsg:31259",
            "Grundstück " + self.gst + ' (Letztstand: ' +
            gst_version_current.rel_alm_gst_ez.datenstand[0:10] + ')',
            "memory")
        gst_dp = self.gst_layer_current.dataProvider()
        """"""

        """definiere die Attribute für den Layer"""
        gst_dp.addAttributes([QgsField("id", QVariant.Int),
                              QgsField("gst", QVariant.String),
                              QgsField("stand", QVariant.String),
                              QgsField("area", QVariant.String)])

        # tell the vector layer to fetch changes from the provider
        self.gst_layer_current.updateFields()
        """"""

        gst_feat = QgsFeature(self.gst_layer_current.fields())
        gst_feat.setAttributes([gst_version_current.id,
                                gst_version_current.rel_alm_gst.gst,
                                gst_version_current.rel_alm_gst_ez.datenstand,
                                to_shape(gst_version_current.geometry).area])
        gst_feat.setGeometry(
            QgsGeometry.fromWkt(to_shape(gst_version_current.geometry).wkt))

        gst_dp.addFeatures([gst_feat])

        self.gst_layer_current.back = False
        self.gst_layer_current.base = True
        setLayerStyle(self.gst_layer_current, 'gst_current_blue')

        self.guiMainGis.addLayer(self.gst_layer_current)
        """"""

    def addGstLayerVersions(self):
        """
        füge eine Layer mit allen Versionen dieses Gst ein
        :return:
        """

        # todo: die Darstellun der Layer im Kartenfenster und im Layer-Tree
        #  stimmt nicht überein!!!

        """erzeuge einen Layer für das Grundstück"""
        gst_layer = QgsVectorLayer("Polygon?crs=epsg:31259",
                                   'Grundstücksversionen ' + self.gst,
                                   "memory")
        gst_dp = gst_layer.dataProvider()
        """"""

        """definiere die Attribute für den Layer"""
        gst_dp.addAttributes([QgsField("id", QVariant.Int),
                              QgsField("gst", QVariant.String),
                              QgsField("stand", QVariant.String),
                              QgsField("area", QVariant.String)])
        gst_layer.updateFields()  # tell the vector layer to fetch changes from the provider
        """"""

        gst_features = []

        for gst_version in self.gst_versions_sorted:

            gst_feat = QgsFeature(gst_layer.fields())
            gst_feat.setAttributes([gst_version.id,
                                    gst_version.rel_alm_gst.gst,
                                    gst_version.rel_alm_gst_ez.datenstand,
                                    to_shape(gst_version.geometry).area])
            gst_feat.setGeometry(QgsGeometry.fromWkt(
                to_shape(gst_version.geometry).wkt))

            gst_features.append(gst_feat)

        gst_dp.addFeatures(gst_features)

        gst_layer.back = False
        gst_layer.base = False
        self.guiMainGis.addLayer(gst_layer)

        self.setGstVersionStyle(gst_layer, 'stand')

        """setze den Layer mit den Gst-Versionen auf unsichtbar"""
        layer_tree_layer = (self.guiMainGis.layer_tree_model.rootGroup()
                            .findLayer(gst_layer.id()))
        layer_tree_layer.setItemVisibilityCheckedRecursive(False)
        """"""

    def setGstVersionStyle(self, layer, fieldName):
        """
        erzeuge basierend auf die Spalte 'fieldName' einen Style mit zufälligen
        Farben und eindeutigen Spaltenwerten

        :param layer: QgsVectorLayer
        :param fieldName: str
        :return:
        """
        # provide file name index and field's unique values
        fni = layer.dataProvider().fields().indexFromName(fieldName)
        unique_values = layer.uniqueValues(fni)

        # fill categories
        categories = []
        for unique_value in unique_values:
            # initialize the default symbol for this geometry type
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())

            # configure a symbol layer
            layer_style = {}
            layer_style['color'] = '%d, %d, %d, %d' % (0,0,0,0)
            # layer_style['strokecolor'] = '%d, %d, %d' % (
            #     randrange(0, 256),
            #     randrange(0, 256),
            #     randrange(0, 256))
            # layer_style['outline'] = '#555555'
            symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)

            # replace default symbol layer with the configured one

            r = randrange(0, 256)
            g = randrange(0, 256)
            b = randrange(0, 256)

            if symbol_layer is not None:
                symbol.changeSymbolLayer(0, symbol_layer)
                symbol_layer.setStrokeColor(QColor(r, g, b))
                symbol_layer.setStrokeWidth(1)

            # create renderer object
            category = QgsRendererCategory(unique_value, symbol,
                                           str(unique_value))
            # entry for the list of category items
            categories.append(category)

        # create renderer object
        renderer = QgsCategorizedSymbolRenderer(fieldName, categories)

        # assign the created renderer to the layer
        if renderer is not None:
            layer.setRenderer(renderer)

        layer.triggerRepaint()

    def loadSubWidgets(self):
        super().loadSubWidgets()

        self.gst_versions_sorted = sorted(self._entity_mci.rel_alm_gst_version,
                                          key=lambda x:x.rel_alm_gst_ez.datenstand,
                                          reverse=True)

        """erzeuge ein main_gis widget und füge es in ein GisDock ein"""
        self.uiGisDock = GisDock(self)
        self.guiMainGis = MainGis(self.uiGisDock, self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.uiGisDock)
        self.uiGisDock.setWidget(self.guiMainGis)
        """"""

        self.addGstLayerVersions()
        self.addGstLayerCurrent()

        for gst_version in self.gst_versions_sorted:

            gst_version_wdg = GstVersion(self)
            gst_version_wdg.editEntity(gst_version, None)

            """erzeuge ein Tabulator-Blatt für diese Version und füge
            das Widget für die Gst-Version ein"""
            self.uiGstVersionTab.addTab(gst_version_wdg,
                    f'Stand: {gst_version.rel_alm_gst_ez.datenstand[0:10]}')
            """"""

            """sortiere die Liste der Banu nach 'nu_name'"""
            sorted_banu = sorted(gst_version.rel_alm_gst_nutzung,
                                 key=lambda x:x.rel_banu.nu_name,
                                 reverse=True)
            """"""

            """füge die Banu-Widgets in das vorgesehene Layout ein und
            errechne die Gst-Fläche"""
            gst_gb_area = 0
            for banu in sorted_banu:
                banu_wdg = GstVersionBanu(self)
                banu_wdg.initData(banu)
                gst_version_wdg.uiBanuVlay.insertWidget(0, banu_wdg)
                gst_gb_area = gst_gb_area + banu.area
            """"""

            gst_version_wdg.area_gb = gst_gb_area

            for eig in gst_version.rel_alm_gst_ez.rel_alm_gst_eigentuemer:

                eig_wdg = GstEigentuemer(self)
                eig_wdg.initData(eig)
                gst_version_wdg.uiEigentuemerVlay.insertWidget(0, eig_wdg)

class GstVersionBanu(QWidget, gst_version_banu_UI.Ui_GstVersionBanu):

    _name = ''
    _area = ''

    @property  # getter
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        self.uiNameLbl.setText(value)
        self._name = value

    @property  # getter
    def area(self):

        return self._area

    @area.setter
    def area(self, value):

        val = ('{:.4f}'.format(round(float(value) / 10000, 4))
               .replace(".", ","))

        self.uiAreaLbl.setText(str(val) + ' ha')
        self._area = value

    def __init__(self, parent=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

    def initData(self, data_instance):

        self.name = data_instance.rel_banu.nu_name
        self.area = data_instance.area


class GstEigentuemer(QWidget, gst_version_eigentuemer_UI.Ui_GstEigentuemer):

    _anteil = ''
    _name = ''
    _adresse = ''

    @property  # getter
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        self.uiNameLbl.setText(value)
        self._name = value

    @property  # getter
    def anteil(self):

        return self._anteil

    @anteil.setter
    def anteil(self, value):

        anteil_str = str(value) + '/' + str(self.data_instance.anteil_von)

        self.uiAnteilLbl.setText(anteil_str)
        self._anteil = value

    @property  # getter
    def adresse(self):

        return self._adresse

    @adresse.setter
    def adresse(self, value):

        self.uiAdresseLbl.setText(value)
        self._adresse = value

    def __init__(self, parent=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

        self.data_instance = None

    def initData(self, data_instance):

        self.data_instance = data_instance

        self.name = data_instance.name
        self.anteil = data_instance.anteil
        self.adresse = data_instance.adresse


class GisDock(QDockWidget):
    """
    baseclass für das GisDock in der klasse 'Akt'
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.setWindowTitle('Kartenansicht')
