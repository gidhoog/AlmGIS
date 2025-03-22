from PyQt5.QtCore import Qt, QVariant, QAbstractTableModel


class Column:
    def __init__(self, name, data_type):
        self.name = name
        self.data_type = data_type
        self.role_handlers = {}

    def format_data(self, value):
        return str(value)

    def set_role_handler(self, role, handler):
        """Assign a custom handler for a specific role."""
        self.role_handlers[role] = handler

    def handle_role(self, role, value):
        """Handle the given role using the assigned handler or default behavior."""
        if role in self.role_handlers:
            return self.role_handlers[role](value)
        elif role == Qt.DisplayRole:
            return self.format_data(value)
        elif role == Qt.EditRole:
            return value  # Default behavior for editing
        else:
            return QVariant()  # Return an empty QVariant for unsupported roles


class IntegerColumn(Column):
    def __init__(self, name):
        super().__init__(name, int)

    def format_data(self, value):
        return f"{value:,d}"


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, columns):
        super().__init__()
        self._data = data
        self._columns = columns

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        column = self._columns[index.column()]
        value = self._data[index.row()][index.column()]

        # Delegate role handling to the column class
        return column.handle_role(role, value)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._columns[section].name
        return QVariant()


# Example usage
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QTableView

    app = QApplication([])

    # Define columns with custom role handlers
    int_col = IntegerColumn("Integer")
    int_col.set_role_handler(Qt.DisplayRole, lambda x: f"User Role: {x}")

    float_col = Column("Float", float)
    float_col.set_role_handler(Qt.DisplayRole,
                               lambda x: f"Float User Role: {x:.2f}")

    columns = [int_col, float_col]

    # Sample data
    data = [
        [1234, 56.78],
        [9876, 12.34]
    ]

    model = CustomTableModel(data, columns)

    view = QTableView()
    view.setModel(model)
    view.show()

    app.exec_()
