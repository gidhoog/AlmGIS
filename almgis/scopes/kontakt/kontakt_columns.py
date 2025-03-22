from PyQt5.QtCore import Qt
from qga.column import QgaTextColumn

from almgis.data_model import BKontakt


class KontaktNameCol(QgaTextColumn):

    def __init__(self, name):
        super().__init__(name)

        self.base_mc = BKontakt

    def col_value(self, mci):
        return mci.name