from PyQt5.QtCore import Qt
from qga.column import QgaTextColumn

from almgis.data_model import DmKontakt


class KontaktNameCol(QgaTextColumn):

    def __init__(self, name):
        super().__init__(name)

        self.base_mc = DmKontakt

    def col_value(self, mci):
        return mci.name

class KontaktAdresseCol(QgaTextColumn):

    def __init__(self, name):
        super().__init__(name)

        self.base_mc = DmKontakt

    def col_value(self, mci):
        return mci.adresse

class KontaktTypeCol(QgaTextColumn):

    def __init__(self, name):
        super().__init__(name)

        self.base_mc = DmKontakt

    def col_value(self, mci):
        return mci.rel_type.name

class KontaktGemTypeCol(QgaTextColumn):

    def __init__(self, name, visible):
        super().__init__(name, visible=visible)

        self.base_mc = DmKontakt

    def col_value(self, mci):
        return mci.rel_gem_type.name