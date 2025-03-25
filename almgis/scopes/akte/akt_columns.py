from qga.column import QgaTextColumn

from almgis.data_model import BAkt


class KontaktNameCol(QgaTextColumn):

    def __init__(self, name):
        super().__init__(name)

        self.base_mc = BAkt

    def col_value(self, mci):
        return mci.name