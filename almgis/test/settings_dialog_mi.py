from qgis.core import QgsApplication, QgsSettings
from qgis.gui import QgsOptionsDialogBase, QgsOptionsPageWidget
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QWidget, QAction
)
from PyQt5.QtCore import Qt

class MyCustomOptionsPage(QgsOptionsPageWidget):
    """Custom options page for the settings dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Example: Add a line edit for a custom setting
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter your custom setting here")
        layout.addWidget(QLabel("Custom Setting:"))
        layout.addWidget(self.line_edit)

        # Load the current setting
        settings = QgsSettings()
        self.line_edit.setText(settings.value("my_plugin/custom_setting", "", str))

    def apply(self):
        # Save the setting when the user clicks "OK"
        settings = QgsSettings()
        settings.setValue("my_plugin/custom_setting", self.line_edit.text())
        return True  # Return True to indicate success

class MyOptionsDialog(QgsOptionsDialogBase):
    """Custom options dialog with a single page."""
    def __init__(self, parent=None):
        super().__init__(parent, "My Custom App Settings")

        # Add your custom options page
        self.add_page(MyCustomOptionsPage(self), "My Custom Page", "Custom Settings")

    def apply(self):
        # This is called when the user clicks "OK"
        QMessageBox.information(self, "Settings Saved", "Your settings have been saved!")
        return True

class MainWindow(QMainWindow):
    """Main application window with a menu to open the settings dialog."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Standalone PyQGIS App")
        self.setGeometry(100, 100, 400, 300)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Example: Display the current setting
        self.label = QLabel("Current setting: ")
        layout.addWidget(self.label)

        # Menu bar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")

        # Action to open the settings dialog
        settings_action = QAction("Open Settings", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

        # Load and display the current setting
        self.load_setting()

    def open_settings(self):
        """Open the settings dialog."""
        dialog = MyOptionsDialog(self)
        dialog.exec_()
        self.load_setting()  # Refresh the displayed setting

    def load_setting(self):
        """Load and display the current setting."""
        settings = QgsSettings()
        current_setting = settings.value("my_plugin/custom_setting", "", str)
        self.label.setText(f"Current setting: {current_setting}")

def main():
    # Initialize QGIS Application
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # Create and show the main window
    app = QApplication([])
    window = MainWindow()
    window.show()

    # Run the application
    app.exec_()

    # Cleanup
    qgs.exitQgis()

if __name__ == "__main__":
    main()
