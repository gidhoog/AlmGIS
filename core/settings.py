
from PyQt5.QtWidgets import QWidget


from core.main_dialog import MainDialog
from core import settings_UI


class SettingsDlg(MainDialog):
    """
    dialog für die anzeige einer grundstückszuordnung
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.enableApply = True

        self.dialog_window_title = 'Alm- und Weidebuch - Einstellungen'
        self.set_apply_button_text('Änderungen übernehmen und Schließen')

    def accept(self):
        if self.dialogWidget.acceptEntity():
            super().accept()

class SettingsWdg(settings_UI.Ui_Settings, QWidget):
    """
    mit diesem Formular können ein oder mehrere Gst zugeordnet werden
    """

    dialog_widget = None

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent