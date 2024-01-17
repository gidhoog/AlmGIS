from core.gis_item import GisItem
from core.main_dialog import MainDialog
from core.scopes.akte import abgrenzung_UI
from qgis.PyQt.QtWidgets import QWidget


class Abgrenzung(QWidget, abgrenzung_UI.Ui_Abgrenzung):

    def __init__(self, parent=None, item=None):
        super(__class__, self).__init__()
        self.setupUi(self)
        
        self.item = item

        self.mapData()

    def mapData(self):

        self.uiJahrSbox.setValue(self.item.data(GisItem.Jahr_Role))
        
    def submitData(self):
        
        self.item.setData(self.uiJahrSbox.value(), GisItem.Jahr_Role)


class AbgrenzungDialog(MainDialog):
    """
    dialog für ein entity-widget (Entity)
    """

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.parent = parent
        self.enableApply = True
        self.set_apply_button_text('&Speichern und Schließen')

        self.setMaximumWidth(500)

    def accept(self):
        """
        wenn 'acceptEntity' des entity-widget True zurückgibt (die daten sind
        gültig) dann rufe QDialog.accept() auf
        """
        # if self.dialogWidget.acceptEntity():
        #     super().accept()
        
        self.dialogWidget.submitData()
        super().accept()