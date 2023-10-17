
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QFileDialog

from sqlalchemy import select

from core.data_model import BSettings
from core.main_dialog import MainDialog
from core import settings_UI, DbSession, db_session_cm


def getSettingValue(code):
    """
    lese die Einstellung mit dem übergebenen Code aus der Datenbank
    und liefere den Wert zurück

    :param code: str
    :return: value
    """
    with db_session_cm() as session:
        stmt = select(BSettings).filter(BSettings.code == code)
        query = session.scalars(stmt).first()

    return query.value


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

        self.list_option_pathes = QListWidgetItem()
        self.list_option_pathes.setText('Verzeichnisse')

        self.list_option_other = QListWidgetItem()
        self.list_option_other.setText('Sonstiges')


        self.uiOptionLwdg.insertItem(0, self.list_option_pathes)
        self.uiOptionLwdg.insertItem(1, self.list_option_other)

        self.uiOptionLwdg.currentRowChanged.connect(self.indexChanged)

        self.uiGstImportPbtn.clicked.connect(self.setImportPath)

        # print(f'bev_path: {self.getSettingValue("bev_imp_path")}')
        self.loadData()

    def acceptEntity(self):

        aaa = self.setSettingValue("bev_imp_path", self.uiGstImportLedit.text())

        print(f'speichern')

        return True

    def loadData(self):

        # self.uiGstImportLedit.setText(self.getSettingValue("bev_imp_path"))
        self.uiGstImportLedit.setText(getSettingValue("bev_imp_path"))


    # @staticmethod
    # def getSettingValue(code):
    #     """
    #     lese die Einstellung mit dem übergebenen Code aus der Datenbank
    #     und liefere den Wert zurück
    #
    #     :param code: str
    #     :return: value
    #     """
    #     with db_session_cm() as session:
    #
    #         stmt = select(BSettings).filter(BSettings.code == code)
    #         query = session.scalars(stmt).first()
    #
    #     return query.value

    def setSettingValue(self, code, value: str):
        """
        schreibe den Wert einer Einstelung in die Datenbank

        :param code: str
        :param value: str
        :return: bool
        """
        try:
            with db_session_cm() as session:

                stmt = select(BSettings).filter(BSettings.code == code)
                query = session.scalars(stmt).first()

                query.value = value
            return True
        except:
            print(f"failed to write the value '{value}' to the setting-code: '{code}'")
            return False


    def indexChanged(self, index):

        self.uiSettingStackW.setCurrentIndex(index)

    def setImportPath(self):

        imp_path_dlg = QFileDialog()
        imp_path_dlg.setFileMode(QFileDialog.Directory)
        imp_path_dlg.setOption(QFileDialog.ShowDirsOnly, True)

        # project_file = imp_path_dlg.getOpenFileName(self, "wähle das Import-Verzeichnis", "")
        # print(f'project_file: {project_file}')

        directory = imp_path_dlg.getExistingDirectory()  # Select directory

        print(f'{directory}')

        if directory:
            self.uiGstImportLedit.setText(directory)

