from PyQt5.QtCore import Qt

class Column:
    def __init__(self, name, data_type):
        self.name = name
        self.data_type = data_type

    def format_data(self, value):
        return str(value)

class IntegerColumn(Column):
    def __init__(self, name):
        super().__init__(name, int)

    def format_data(self, value):
        return f"{value:,d}"

class FloatColumn(Column):
    def __init__(self, name, decimal_places=2):
        super().__init__(name, float)
        self.decimal_places = decimal_places

    def format_data(self, value):
        return f"{value:.{self.decimal_places}f}"

class CustomTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, columns):
        super().__init__()
        self._data = data
        self._columns = columns

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            return self._columns[index.column()].format_data(value)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._columns[section].name

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._columns)
