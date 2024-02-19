from datetime import datetime

from qgis.PyQt.QtWidgets import QWidget

from core import entity
from core.scopes.komplex import komplex_dataform_UI


class KomplexDataForm(komplex_dataform_UI.Ui_KomplexDataForm, entity.Entity):
    """
    class for a komplex-entity
    """

    # _entity_mc = BKomplexe

    _nr = 0
    _name = ''
    _jahr = 0
    _bearbeiter = ''
    _anm = ''

    @property  # getter
    def nr(self):

        self._nr = self.uiNr.value()
        return self._nr

    @nr.setter
    def nr(self, value):
        try:
            self.uiNr.setValue(value)
            self._nr = value
        except:
            print(f'cannot set nr')

    @property  # getter
    def name(self):

        self._name = self.uiName.text()
        return self._name

    @name.setter
    def name(self, value):

        self.uiName.setText(value)
        self._name = value

    @property  # getter
    def jahr(self):

        self._jahr = self.uiJahr.value()
        return self._jahr

    @jahr.setter
    def jahr(self, value):

        try:
            self.uiJahr.setValue(value)
            self._jahr = value
        except:
            print(f'cannot set year')
    @property  # getter
    def bearbeiter(self):

        self._bearbeiter = self.uiBearbeiter.text()
        return self._bearbeiter

    @bearbeiter.setter
    def bearbeiter(self, value):

        self.uiBearbeiter.setText(value)
        self._bearbeiter = value

    @property  # getter
    def anm(self):

        self._anm = self.uiAnmerkung.toPlainText()
        return self._anm

    @anm.setter
    def anm(self, value):

        self.uiAnmerkung.setPlainText(value)
        self._anm = value

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        # self.parent = parent

        self.jahr = int(datetime.now().strftime('%Y'))

    def mapData(self):
        super().mapData()

        self.nr = self._entity_mci.nr
        self.name = self._entity_mci.name
        self.jahr = self._entity_mci.jahr
        self.bearbeiter = self._entity_mci.bearbeiter
        self.anm = self._entity_mci.anmerkung

    def submitEntity(self):
        super().submitEntity()

        self._entity_mci.nr = self.nr
        self._entity_mci.name = self.name
        self._entity_mci.jahr = self.jahr
        self._entity_mci.bearbeiter = self.bearbeiter
        self._entity_mci.anmerkung = self.anm

    def feature_attribute_list(self):

        return [self.nr, self.name, self.jahr, self.bearbeiter, self.anm]
