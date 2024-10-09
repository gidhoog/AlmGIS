
from qgis.PyQt.QtCore import Qt, QSize, QAbstractItemModel, QModelIndex

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsField

from core import db_session_cm
from core.data_model import BGstVersion
from core.entity import Entity
from core.gis_layer import setLayerStyle
from core.main_gis import MainGis

from core.scopes.gst import gst_version_UI
from sqlalchemy import func, select
from geoalchemy2.shape import to_shape


class GstVersion(gst_version_UI.Ui_GstVersion, Entity):
    """
    baseclass für eine gst-version
    """

    _ez = 0
    _ezkg = 0
    _area_gb = 0
    _area_kat = 0.00
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

        kgname = self._entity_mci.rel_alm_gst_ez.rel_kat_gem.kgname

        self.uiEzKgLbl.setText(str(value) + ' - ' + kgname)
        self._ezkg = value

    @property  # getter
    def area_gb(self):

        return self._area_gb

    @area_gb.setter
    def area_gb(self, value):

        val = ('{:.6f}'.format(round(float(value) / 10000, 6))
               .replace(".", ","))
        self.uiAreaGbLbl.setText(str(val) + ' ha')

        self._area_gb = value

    @property  # getter
    def area_kat(self):

        return self._area_gb

    @area_kat.setter
    def area_kat(self, value):

        val = ('{:.6f}'.format(round(value / 10000, 6)).replace(".", ","))
        self.uiAreaKatLbl.setText(str(val) + ' ha')

        self._area_kat = value

    @property  # getter
    def datenstand(self):

        return self._datenstand

    @datenstand.setter
    def datenstand(self, value):

        self.uiDatenstandDatumLbl.setText(value[0:10])
        self.uiDatenstandZeitLbl.setText('(' + value[11:19] + ')')
        self._datenstand = value

    @property  # getter
    def importzeit(self):

        return self._importzeit

    @importzeit.setter
    def importzeit(self, value):

        self.uiImportZeitDatumLbl.setText(value[0:10])
        self.uiImportZeitZeitLbl.setText('(' + value[11:19] + ')')
        self._importzeit = value


    def __init__(self, parent=None):
        super(__class__, self).__init__()
        self.setupUi(self)


    def mapEntityData(self):
        super().mapEntityData()

        self.ez = self._entity_mci.rel_alm_gst_ez.ez
        self.ezkg = self._entity_mci.rel_alm_gst_ez.kgnr
        self.datenstand = self._entity_mci.rel_alm_gst_ez.datenstand
        self.importzeit = self._entity_mci.rel_alm_gst_ez.import_time

        self.area_kat = to_shape(self._entity_mci.geometry).area  # float

