from PyQt5.QtGui import QIcon
from qga.core.settings_dlg import QgaSettingsDlg, QgaSettingsPrjDlg
from qga.core.settings_page_register import SettingsPageDescriptor, SettingsPageRegistry, PropertiesPageRegistry
from qga.core.settings_wdg import SettingsPageStartDlg, PropPageGeneralDlg

from almgis.core.settings_wdg import SettingsAlmgisDlg


SettingsPageRegistry.register(
    SettingsPageDescriptor(
    title   = "Startdialog",
    factory = SettingsPageStartDlg,
    group   = "Allgemein",
    icon    = QIcon.fromTheme("network-workgroup"),
    tooltip = "Startdialog",
    order   = 10,
))

SettingsPageRegistry.register(
    SettingsPageDescriptor(
    title   = "Stile",
    factory = SettingsAlmgisDlg,
    group   = "AlmGIS",
    icon    = QIcon.fromTheme("network-workgroup"),
    tooltip = "Stile",
    order   = 20,
))

PropertiesPageRegistry.register(
    SettingsPageDescriptor(
    title   = "Projektname",
    factory = PropPageGeneralDlg,
    group   = "Allgemein",
    icon    = QIcon.fromTheme("network-workgroup"),
    tooltip = "Projektname",
    order   = 10,
))


class AlmSettingsDialog(QgaSettingsDlg):


    def __init__(self, parent=None):
        super().__init__(parent, title="AlmGIS – Einstellungen")

        print('2')
        # self.setting_reg = SettingsPageRegistry


class AlmSettingsProjectDlg(QgaSettingsPrjDlg):


    def __init__(self, parent=None):
        super().__init__(parent, title="AlmGIS – Projekteigenschaften")

        print('77')
        # self.setting_reg = SettingsPageRegistry
