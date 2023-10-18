
from PyQt5.QtCore import Qt, QSize, QAbstractItemModel, QModelIndex

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsField

from core.gis_layer import setLayerStyle
from core.main_gis import MainGis

from core.scopes.gst import gst_UI


class Gst(gst_UI.Ui_Gst):
    """
    baseclass für ein grundstück
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