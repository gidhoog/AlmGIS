import sys
from qgis.PyQt.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QLabel, QLineEdit, QCheckBox, QSpinBox,
    QFormLayout, QFrame, QComboBox
)
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtGui import QIcon
from qgis.gui import QgsOptionsDialogBase, QgsOptionsPageWidget

from almgis.resources.ui_py import test_qgsoptionsdialog_template_UI


# ── 1. Settings pages (unchanged) ────────────────────────────────────────────

class GeneralSettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("MyOrg", "MyApp")
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your name")
        layout.addRow("Username:", self.username_edit)

        self.autosave_check = QCheckBox("Enable auto-save on project close")
        layout.addRow("Auto-save:", self.autosave_check)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "German", "French", "Italian"])
        layout.addRow("Language:", self.language_combo)

        self.username_edit.setText(self.settings.value("general/username", ""))
        self.autosave_check.setChecked(self.settings.value("general/autosave", False, type=bool))
        self.language_combo.setCurrentText(self.settings.value("general/language", "English"))

    def apply(self):
        self.settings.setValue("general/username", self.username_edit.text())
        self.settings.setValue("general/autosave", self.autosave_check.isChecked())
        self.settings.setValue("general/language", self.language_combo.currentText())


class PathsSettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("MyOrg", "MyApp")
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.projects_edit = QLineEdit()
        self.projects_edit.setPlaceholderText("/home/user/projects")
        layout.addRow("Projects folder:", self.projects_edit)

        self.plugins_edit = QLineEdit()
        self.plugins_edit.setPlaceholderText("/home/user/.qgis3/python/plugins")
        layout.addRow("Plugins folder:", self.plugins_edit)

        self.projects_edit.setText(self.settings.value("paths/projects", ""))
        self.plugins_edit.setText(self.settings.value("paths/plugins", ""))

    def apply(self):
        self.settings.setValue("paths/projects", self.projects_edit.text())
        self.settings.setValue("paths/plugins", self.plugins_edit.text())


class DisplaySettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("MyOrg", "MyApp")
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setRange(6, 72)
        self.fontsize_spin.setSuffix(" pt")
        layout.addRow("Font size:", self.fontsize_spin)

        self.tooltips_check = QCheckBox("Show tooltips")
        layout.addRow("Tooltips:", self.tooltips_check)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.addRow(sep)

        self.darkmode_check = QCheckBox("Enable dark mode")
        layout.addRow("Theme:", self.darkmode_check)

        self.fontsize_spin.setValue(self.settings.value("display/fontsize", 10, type=int))
        self.tooltips_check.setChecked(self.settings.value("display/tooltips", True, type=bool))
        self.darkmode_check.setChecked(self.settings.value("display/darkmode", False, type=bool))

    def apply(self):
        self.settings.setValue("display/fontsize", self.fontsize_spin.value())
        self.settings.setValue("display/tooltips", self.tooltips_check.isChecked())
        self.settings.setValue("display/darkmode", self.darkmode_check.isChecked())


class ColorsSettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.canvas_color = QLineEdit("#ffffff")
        layout.addRow("Canvas background:", self.canvas_color)

        self.selection_color = QLineEdit("#ffff00")
        layout.addRow("Selection color:", self.selection_color)

    def apply(self):
        s = QSettings("MyOrg", "MyApp")
        s.setValue("colors/canvas", self.canvas_color.text())
        s.setValue("colors/selection", self.selection_color.text())


class NetworkSettingsPage(QgsOptionsPageWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("MyOrg", "MyApp")
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.proxy_check = QCheckBox("Use proxy server")
        layout.addRow("Proxy:", self.proxy_check)

        self.proxy_host = QLineEdit()
        self.proxy_host.setPlaceholderText("proxy.example.com")
        layout.addRow("Host:", self.proxy_host)

        self.proxy_port = QSpinBox()
        self.proxy_port.setRange(1, 65535)
        self.proxy_port.setValue(8080)
        layout.addRow("Port:", self.proxy_port)

        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(5, 300)
        self.timeout_spin.setSuffix(" s")
        self.timeout_spin.setValue(30)
        layout.addRow("Timeout:", self.timeout_spin)

        self.proxy_check.setChecked(self.settings.value("network/use_proxy", False, type=bool))
        self.proxy_host.setText(self.settings.value("network/host", ""))
        self.proxy_port.setValue(self.settings.value("network/port", 8080, type=int))

    def apply(self):
        self.settings.setValue("network/use_proxy", self.proxy_check.isChecked())
        self.settings.setValue("network/host", self.proxy_host.text())
        self.settings.setValue("network/port", self.proxy_port.value())


# ── 2. The options dialog ────────────────────────────────────────────────────

class AppSettingsDialog(QgsOptionsDialogBase, test_qgsoptionsdialog_template_UI.Ui_QgsOptionDialogTemplate):
    """
    Settings dialog built on QgsOptionsDialogBase.

    The `path` argument of addPage() is a QStringList that tells the base
    class where to place the page in the tree:

        path=[]            →  top-level item  (like "Network")
        path=["General"]   →  child of a "General" group
        path=["Display"]   →  child of a "Display" group

    The base class creates the group node automatically the first time a
    path component is seen.  This is the same mechanism QGIS 3.22+ uses
    internally for its own settings pages.
    """

    def __init__(self, parent=None):
        # QgsOptionsDialogBase(objectName, parent, flags, settings)
        super().__init__("AppSettings", parent)
        self.setupUi(self)

        self.setWindowTitle("Application Settings")
        self.setMinimumSize(640, 480)

        # Wire up the base-class UI (tree + stacked widget + button box).
        # Pass False to skip restoring geometry before pages are registered.
        self.initOptionsBase(False)

        # Keep references so we can call apply() ourselves in accept()
        self._pages = []

        self._register_pages()

        # Restore last window geometry *after* all pages are added
        self.restoreOptionsBaseUi()

    # ── Page registration ────────────────────────────────────────────────────

    def _register_pages(self):
        # ── General group ────────────────────────────────────────────────────
        p = GeneralSettingsPage(self)
        self._pages.append(p)
        self.addPage(
            "General",  # 1. title
            "General application settings",  # 2. tooltip
            QIcon.fromTheme("preferences-other"),  # 3. icon
            p,  # 4. widget  ← was wrongly first
            ["General"],  # 5. path
        )

        p = PathsSettingsPage(self)
        self._pages.append(p)
        self.addPage(
            "Paths",
            "Project and plugin folder paths",
            QIcon.fromTheme("folder"),
            p,
            ["General"],
        )

        # ── Display group ────────────────────────────────────────────────────
        p = DisplaySettingsPage(self)
        self._pages.append(p)
        self.addPage(
            "Display",
            "Font size, tooltips, and theme",
            QIcon.fromTheme("video-display"),
            p,
            ["Display"],
        )

        p = ColorsSettingsPage(self)
        self._pages.append(p)
        self.addPage(
            "Colors",
            "Canvas and selection colors",
            QIcon.fromTheme("preferences-desktop-color"),
            p,
            ["Display"],
        )

        # ── Network — top-level ──────────────────────────────────────────────
        p = NetworkSettingsPage(self)
        self._pages.append(p)
        self.addPage(
            "Network",
            "Proxy and connection settings",
            QIcon.fromTheme("network-workgroup"),
            p,
            [],
        )

    # ── Apply / OK ───────────────────────────────────────────────────────────

    def _apply_all(self):
        for page in self._pages:
            page.apply()

    def accept(self):
        """OK button — save every page then close."""
        self._apply_all()
        super().accept()


# ── 3. Main window ───────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Standalone PyQGIS App")
        self.resize(420, 220)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.status_label = QLabel("Press the button to open Settings.")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        btn_open = QPushButton("⚙  Open Settings…")
        btn_open.clicked.connect(self.open_settings)
        layout.addWidget(btn_open)

        btn_read = QPushButton("Read & show current settings")
        btn_read.clicked.connect(self.show_settings)
        layout.addWidget(btn_read)

    def open_settings(self):
        dlg = AppSettingsDialog(self)
        dlg.exec()

    def show_settings(self):
        s = QSettings("MyOrg", "MyApp")
        lines = [
            f"username : {s.value('general/username', '(not set)')}",
            f"language : {s.value('general/language', 'English')}",
            f"autosave : {s.value('general/autosave', False, type=bool)}",
            f"fontsize : {s.value('display/fontsize', 10, type=int)} pt",
            f"darkmode : {s.value('display/darkmode', False, type=bool)}",
            f"proxy    : {s.value('network/use_proxy', False, type=bool)}",
        ]
        self.status_label.setText("\n".join(lines))


# ── 4. Bootstrap ─────────────────────────────────────────────────────────────

def main():
    from qgis.core import QgsApplication
    qgs = QgsApplication([], True)
    qgs.initQgis()

    win = MainWindow()
    win.show()

    exit_code = qgs.exec()
    qgs.exitQgis()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()