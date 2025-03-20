import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QMenu
from PyQt5.QtCore import Qt, QAbstractTableModel

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self.column_names = ["ID", "First Name", "Last Name", "Email"]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.column_names[section]
        return super().headerData(section, orientation, role)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableView Column Manager")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        data = [
            [1, "John", "Doe", "john@example.com"],
            [2, "Jane", "Smith", "jane@example.com"],
            [3, "Bob", "Johnson", "bob@example.com"],
        ]

        self.model = TableModel(data)
        self.table_view.setModel(self.model)

        # Define default column visibility
        self.column_visibility = [True, True, False, True]  # Hide "Last Name" by default

        # Apply default visibility
        self.apply_column_visibility()

        self.column_manager_button = QPushButton("Manage Columns")
        self.column_manager_button.clicked.connect(self.show_column_manager)
        layout.addWidget(self.column_manager_button)

    def apply_column_visibility(self):
        for column, is_visible in enumerate(self.column_visibility):
            self.table_view.setColumnHidden(column, not is_visible)

    def show_column_manager(self):
        menu = QMenu(self)

        for column, name in enumerate(self.model.column_names):
            action = menu.addAction(name)
            action.setCheckable(True)
            action.setChecked(self.column_visibility[column])
            action.toggled.connect(lambda checked, col=column: self.toggle_column(col, checked))

        menu.exec_(self.column_manager_button.mapToGlobal(self.column_manager_button.rect().bottomLeft()))

    def toggle_column(self, column, checked):
        self.column_visibility[column] = checked
        self.table_view.setColumnHidden(column, not checked)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
