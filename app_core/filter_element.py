from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtGui import QColor

from app_core import filter_element_UI


class FilterElement(QWidget, filter_element_UI.Ui_FilterElement):

    def __init__(self, parent):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent