
from PyQt5.QtCore import Qt, QSize, QAbstractItemModel, QModelIndex

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.core import QgsVectorLayer, QgsField

from core.entity import Entity
from core.gis_layer import setLayerStyle
from core.main_gis import MainGis

from core.scopes.gst import gst_UI
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

        akt_lay = QVBoxLayout(self)
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

            self.uiGstVersionTab.addTab(gst_version_wdg, f'Stand: {gst_version.rel_alm_gst_ez.datenstand[0:10]}')





