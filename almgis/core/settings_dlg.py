from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox, QSpinBox, QFormLayout, QComboBox, QLineEdit, QPushButton
from qga.core.settings_dlg import QgaSettingsDlg, QgaSettingsPrjDlg
from qga.core.settings_register import SettingsPageDescriptor, SettingsRegistry
from qga.core.settings_wdg import SettingsPageStartDlg
from qgis._gui import QgsOptionsPageWidget
from qga import Qga
from qga.core.tools import selectFile
from almgis.resources.ui_py import settings_general_wdg_UI

# from almgis.core.settings import AlmSettingsApp, AlmSettingsUser


class GeneralSettingsPage(QgsOptionsPageWidget, settings_general_wdg_UI.Ui_GeneralSettingsPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


        """set a group for the info-buttons"""
        self.uiInfoTest.group = 'QgaSettingsDlg'
        """"""
    #     # s = QSettings("NoeAbb", "AlmGIS")
    #     s = AlmSettingsUser()
    #     s.sync()
    #     s = Qga.Settings.User
    #     print(f'Qga.Settings.User - ini: {s.fileName()}')
    #
        # a = Qga.Settings.App
        # a.sync()
        # print(f'Qga.Settings.App - ini: {a.fileName()}')
        #
        # AlmSettingsApp.sync()
        # print(f'AlmSettingsApp - ini: {AlmSettingsApp.fileName()}')
    #     layout = QFormLayout(self)
    #     layout.setContentsMargins(20, 20, 20, 20)
    #     layout.setSpacing(12)
    #
    #     self.uiSetCommonDbPbtn = QPushButton(self)
    #     self.uiSetCommonDbPbtn.setText('aaa')
    #
    #     self.username_edit = QLineEdit()
    #     layout.addRow("Username:", self.username_edit)
    #
    #     layout.addRow("wähle DB:", self.uiSetCommonDbPbtn)
    #
    #     self.autosave_check = QCheckBox("Enable auto-save on project close")
    #     layout.addRow("Auto-save:", self.autosave_check)
    #
    #     self.language_combo = QComboBox()
    #     self.language_combo.addItems(["English", "German", "French", "Italian"])
    #     layout.addRow("Language:", self.language_combo)
    #
    #     # self.username_edit.setText(s.value("general/username", ""))
    #     self.username_edit.setText(s.value("paths/common_db_file", "sss"))
    #     self.autosave_check.setChecked(s.value("general/autosave", False, type=bool))
    #     self.language_combo.setCurrentText(s.value("general/language", "English"))
    #
    #     self.uiSetCommonDbPbtn.clicked.connect(self.selectCommonDb)
    #
    # def selectCommonDb(self):
    #     selectFile(self,
    #                self.username_edit,
    #                'wähle die Zentraldatenbank',
    #                filter='db-Dateien (*.db)')
    #
    # def apply(self):
    #     s = QSettings("MyOrg", "MyApp")
    #     s.setValue("general/username", self.username_edit.text())
    #     s.setValue("general/autosave", self.autosave_check.isChecked())
    #     s.setValue("general/language", self.language_combo.currentText())


class DisplaySettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        s = QSettings("MyOrg", "MyApp")
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setRange(6, 72)
        self.fontsize_spin.setSuffix(" pt")
        layout.addRow("Font size:", self.fontsize_spin)

        self.darkmode_check = QCheckBox("Enable dark mode")
        layout.addRow("Theme:", self.darkmode_check)

        self.fontsize_spin.setValue(s.value("display/fontsize", 10, type=int))
        self.darkmode_check.setChecked(s.value("display/darkmode", False, type=bool))

    def apply(self):
        s = QSettings("MyOrg", "MyApp")
        s.setValue("display/fontsize", self.fontsize_spin.value())
        s.setValue("display/darkmode", self.darkmode_check.isChecked())


SettingsRegistry.register(SettingsPageDescriptor(
    title   = "Startdialog",
    factory = SettingsPageStartDlg,
    group   = "Allgemein",
    icon    = QIcon.fromTheme("network-workgroup"),
    tooltip = "Startdialog",
    order   = 10,
))
# SettingsRegistry.register(SettingsPageDescriptor(
#     title   = "Datenbanken",
#     factory = DatabaseSettingsPage,
#     group   = "Allgemein",
#     icon    = QIcon.fromTheme("server-database"),
#     tooltip = "Angaben zu den verwendeten Datenbanken",
#     order   = 20,
# ))
#
# SettingsRegistry.register(SettingsPageDescriptor(
#     title   = "General",
#     factory = GeneralSettingsPage,
#     group   = "AlmGIS",
#     icon    = QIcon.fromTheme("preferences-other"),
#     tooltip = "General application settings",
#     order   = 10,
# ))
# SettingsRegistry.register(SettingsPageDescriptor(
#     title   = "Display",
#     factory = DisplaySettingsPage,
#     group   = "AlmGIS",
#     icon    = QIcon.fromTheme("video-display"),
#     tooltip = "Font size and theme",
#     order   = 20,
# ))


class AlmSettingsDialog(QgaSettingsDlg):


    def __init__(self, parent=None):
        super().__init__(parent, title="AlmGIS – Einstellungen")

        print('2')
        # self.setting_reg = SettingsRegistry


class AlmSettingsProjectDlg(QgaSettingsPrjDlg):


    def __init__(self, parent=None):
        super().__init__(parent, title="AlmGIS – Projekteigenschaften")

        print('77')
        # self.setting_reg = SettingsRegistry
