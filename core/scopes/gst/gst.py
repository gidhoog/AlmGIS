

from qgis.PyQt.QtWidgets import QHBoxLayout, QWidget, QLabel, QDockWidget
from qgis.PyQt.QtCore import Qt

from core.entity import Entity
from core.main_gis import MainGis

from core.scopes.gst import gst_UI, gst_version_banu_UI, gst_version_eigentuemer_UI
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

        self.uiGstLbl.setText(value)
        self._gst = value

    @property  # getter
    def kgnr(self):

        return self._kgnr

    @kgnr.setter
    def kgnr(self, value):

        kgname = self.data_instance.rel_kat_gem.kgname

        self.uiKgLbl.setText(str(value) + ' - ' + kgname)
        self._kgnr = value


    def __init__(self, parent=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

        """erzeuge ein main_gis widget und füge es in ein GisDock ein"""
        self.uiGisDock = GisDock(self)
        self.guiMainGis = MainGis(self.uiGisDock, self)
        # self.guiMainGis.komplex_jahr = 2018
        self.addDockWidget(Qt.RightDockWidgetArea, self.uiGisDock)
        self.uiGisDock.setWidget(self.guiMainGis)
        """"""

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

        self.gst = self.data_instance.gst
        self.kgnr = self.data_instance.kgnr

    def loadSubWidgets(self):
        super().loadSubWidgets()

        gst_versions_sorted = sorted(self.data_instance.rel_alm_gst_version,
                                 key=lambda x:x.rel_alm_gst_ez.datenstand,
                                 reverse=True)

        for gst_version in gst_versions_sorted:

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
