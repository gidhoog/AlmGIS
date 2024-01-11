from qgis.PyQt.QtWidgets import QWidget
from core import entity_titel_UI

class EntityTitel(QWidget, entity_titel_UI.Ui_EntityTitel):
    """
    Widget für die Titelzeile in einem Entity
    """

    def __init__(self, parent=None) -> None:
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent

