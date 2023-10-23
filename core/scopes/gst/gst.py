
from PyQt5.QtCore import Qt, QSize, QAbstractItemModel, QModelIndex

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QHBoxLayout, QWidget, QLabel
from qgis.core import QgsVectorLayer, QgsField

from core.entity import Entity
from core.gis_layer import setLayerStyle
from core.main_gis import MainGis

from core.scopes.gst import gst_UI, gst_version_banu_UI
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

        # gst_version = GstVersion(self)

        # akt_lay = QVBoxLayout(self)
        # akt_lay.addWidget(gst_version)

        # self.uiAktuellWdg.setLayout(akt_lay)

    def mapData(self):
        super().mapData()

        self.gst = self.data_instance.gst
        self.kgnr = self.data_instance.kgnr

    def loadSubWidgets(self):
        super().loadSubWidgets()

        for gst_version in self.data_instance.rel_alm_gst_version:

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

            """füge die Banu-Widgets in das vorgesehene Layout ein"""
            for banu in sorted_banu:
                banu_wdg = GstVersionBanu(self)
                banu_wdg.initData(banu)
                gst_version_wdg.uiBanuVlay.insertWidget(0, banu_wdg)
            """"""


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

