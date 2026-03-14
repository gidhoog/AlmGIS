import sys
import os
from qgis.PyQt.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QWidget, QLabel, QLineEdit,
    QCheckBox, QSpinBox, QFormLayout, QFrame
)
from qgis.PyQt.QtCore import QSettings
from qgis.gui import QgsOptionsDialogBase, QgsOptionsPageWidget
from qgis.PyQt.QtGui import QIcon

from almgis.resources.ui_py import test_qgsoptionsdialog_template_UI


# from qgis.core import QgsApplication


# ── 1. Individual settings pages ────────────────────────────────────────────

class GeneralSettingsPage(QgsOptionsPageWidget):
    """General settings page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("MyOrg", "MyApp")

        layout = QFormLayout()
        self.setLayout(layout)

        # Username field
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your name")
        layout.addRow("Username:", self.username_edit)

        # Auto-save checkbox
        self.autosave_check = QCheckBox("Enable auto-save")
        layout.addRow("Auto-save:", self.autosave_check)

        # Load current values
        self.username_edit.setText(self.settings.value("general/username", ""))
        self.autosave_check.setChecked(
            self.settings.value("general/autosave", False, type=bool)
        )

    def apply(self):
        """Called when the user clicks OK or Apply."""
        self.settings.setValue("general/username", self.username_edit.text())
        self.settings.setValue("general/autosave", self.autosave_check.isChecked())
        print(f"[General] Settings saved: user={self.username_edit.text()}")


class DisplaySettingsPage(QgsOptionsPageWidget):
    """Display / appearance settings page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("MyOrg", "MyApp")

        layout = QFormLayout()
        self.setLayout(layout)

        # Font size spinner
        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setRange(6, 72)
        self.fontsize_spin.setSuffix(" pt")
        layout.addRow("Font size:", self.fontsize_spin)

        # Show tooltips checkbox
        self.tooltips_check = QCheckBox("Show tooltips")
        layout.addRow("Tooltips:", self.tooltips_check)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layout.addRow(line)

        # Dark mode checkbox
        self.darkmode_check = QCheckBox("Enable dark mode")
        layout.addRow("Theme:", self.darkmode_check)

        # Load current values
        self.fontsize_spin.setValue(
            self.settings.value("display/fontsize", 10, type=int)
        )
        self.tooltips_check.setChecked(
            self.settings.value("display/tooltips", True, type=bool)
        )
        self.darkmode_check.setChecked(
            self.settings.value("display/darkmode", False, type=bool)
        )

    def apply(self):
        self.settings.setValue("display/fontsize", self.fontsize_spin.value())
        self.settings.setValue("display/tooltips", self.tooltips_check.isChecked())
        self.settings.setValue("display/darkmode", self.darkmode_check.isChecked())
        print(f"[Display] Settings saved: fontsize={self.fontsize_spin.value()}")


# ── 2. The options dialog ────────────────────────────────────────────────────

class AppSettingsDialog(QgsOptionsDialogBase, test_qgsoptionsdialog_template_UI.Ui_QgsOptionDialogTemplate):
    """
    Main settings dialog.
    QgsOptionsDialogBase provides the two-panel layout (tree on the left,
    stacked pages on the right) plus OK / Cancel / Apply buttons for free.
    """

    def __init__(self, parent=None):
        # args: dialog object name, parent, Qt flags, QSettings object
        super().__init__("AppSettings", parent)
        self.setupUi(self)

        self.setWindowTitle("Application Settings")
        self.setMinimumSize(600, 400)

        # Initialise the base dialog internals
        self.initOptionsBase(False)   # False = don't restore geometry yet

        # ── register pages ──────────────────────────────────────────────────
        self.general_page = GeneralSettingsPage(self)
        self.addPage('general',
                     'ggggen',
                     QIcon.fromTheme("preferences-other"),
                     self.general_page)

        self.display_page = DisplaySettingsPage(self)
        self.addPage('display',
                     'ddd',
                     QIcon.fromTheme("preferences-desktop"),
                     self.display_page)

        # Restore geometry after pages are added
        self.restoreOptionsBaseUi()

    def accept(self):
        """OK clicked – apply every page, then close."""
        self.general_page.apply()
        self.display_page.apply()
        super().accept()


# ── 3. Main application window ───────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Standalone PyQGIS App")
        self.resize(400, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.status_label = QLabel("Press the button to open Settings.")
        layout.addWidget(self.status_label)

        btn = QPushButton("Open Settings…")
        btn.clicked.connect(self.open_settings)
        layout.addWidget(btn)

        btn_read = QPushButton("Read & show current settings")
        btn_read.clicked.connect(self.show_settings)
        layout.addWidget(btn_read)

    def open_settings(self):
        dlg = AppSettingsDialog(self)
        dlg.exec()

    def show_settings(self):
        s = QSettings("MyOrg", "MyApp")
        text = (
            f"username : {s.value('general/username', '(not set)')}\n"
            f"autosave : {s.value('general/autosave', False, type=bool)}\n"
            f"fontsize : {s.value('display/fontsize', 10, type=int)} pt\n"
            f"tooltips : {s.value('display/tooltips', True, type=bool)}\n"
            f"darkmode : {s.value('display/darkmode', False, type=bool)}"
        )
        self.status_label.setText(text)


# ── 4. Bootstrap ─────────────────────────────────────────────────────────────

def main():
    # Point to your QGIS installation if needed
    # os.environ["QGIS_PREFIX_PATH"] = "/usr"

    from qgis.core import QgsApplication
    qgs = QgsApplication([], True)   # True = GUI app
    qgs.initQgis()

    win = MainWindow()
    win.show()

    exit_code = qgs.exec()
    qgs.exitQgis()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()