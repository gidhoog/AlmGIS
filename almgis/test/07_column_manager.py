import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QVBoxLayout,
                             QPushButton,
                             QWidget, QHBoxLayout, QLineEdit, QCheckBox,
                             QSpinBox, QLabel)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt


class ColumnManager:
    def __init__(self, table_view):
        self.table_view = table_view
        self.columns = []

    def add_column(self, name, visible=True, width=100):
        column = {"name": name, "visible": visible, "width": width}
        self.columns.append(column)
        self.update_view()

    def set_column_visibility(self, index, visible):
        if 0 <= index < len(self.columns):
            self.columns[index]["visible"] = visible
            self.update_view()

    def set_column_width(self, index, width):
        if 0 <= index < len(self.columns):
            self.columns[index]["width"] = width
            self.update_view()

    def update_view(self):
        model = self.table_view.model()
        if not model:
            model = QStandardItemModel()
            self.table_view.setModel(model)

        model.setColumnCount(len(self.columns))
        for i, column in enumerate(self.columns):
            model.setHeaderData(i, Qt.Horizontal, column["name"])
            self.table_view.setColumnHidden(i, not column["visible"])
            if column["visible"]:
                self.table_view.setColumnWidth(i, column["width"])


class ColumnManagerUI(QWidget):
    def __init__(self, column_manager):
        super().__init__()
        self.column_manager = column_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Add new column section
        add_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.visible_checkbox = QCheckBox("Visible")
        self.visible_checkbox.setChecked(True)
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(10, 500)
        self.width_spinbox.setValue(100)
        add_button = QPushButton("Add Column")
        add_button.clicked.connect(self.add_column)

        add_layout.addWidget(QLabel("Name:"))
        add_layout.addWidget(self.name_input)
        add_layout.addWidget(self.visible_checkbox)
        add_layout.addWidget(QLabel("Width:"))
        add_layout.addWidget(self.width_spinbox)
        add_layout.addWidget(add_button)

        layout.addLayout(add_layout)

        # Existing columns section
        for i, column in enumerate(self.column_manager.columns):
            column_layout = QHBoxLayout()
            name_label = QLabel(column["name"])
            visible_checkbox = QCheckBox("Visible")
            visible_checkbox.setChecked(column["visible"])
            visible_checkbox.stateChanged.connect(
                lambda state, idx=i: self.toggle_visibility(idx, state))
            width_spinbox = QSpinBox()
            width_spinbox.setRange(10, 500)
            width_spinbox.setValue(column["width"])
            width_spinbox.valueChanged.connect(
                lambda value, idx=i: self.change_width(idx, value))

            column_layout.addWidget(name_label)
            column_layout.addWidget(visible_checkbox)
            column_layout.addWidget(QLabel("Width:"))
            column_layout.addWidget(width_spinbox)

            layout.addLayout(column_layout)

        self.setLayout(layout)

    def add_column(self):
        name = self.name_input.text()
        visible = self.visible_checkbox.isChecked()
        width = self.width_spinbox.value()
        self.column_manager.add_column(name, visible, width)
        self.init_ui()  # Refresh the UI

    def toggle_visibility(self, index, state):
        self.column_manager.set_column_visibility(index, state == Qt.Checked)

    def change_width(self, index, value):
        self.column_manager.set_column_width(index, value)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableView Column Manager Example")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout()

        table_layout = QVBoxLayout()
        self.table_view = QTableView()
        table_layout.addWidget(self.table_view)

        self.column_manager = ColumnManager(self.table_view)
        self.column_manager.add_column("ID")
        self.column_manager.add_column("Name")
        self.column_manager.add_column("Age")
        self.column_manager.add_column("City", visible=False)

        self.column_manager_ui = ColumnManagerUI(self.column_manager)

        main_layout.addLayout(table_layout)
        main_layout.addWidget(self.column_manager_ui)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.populate_table()

    def populate_table(self):
        model = QStandardItemModel(3, 4)
        model.setHorizontalHeaderLabels(["ID", "Name", "Age", "City"])

        data = [
            ["1", "Alice", "30", "New York"],
            ["2", "Bob", "25", "London"],
            ["3", "Charlie", "35", "Paris"]
        ]

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QStandardItem(value)
                model.setItem(row_idx, col_idx, item)

        self.table_view.setModel(model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
