from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from core import footer_line_UI


class FooterLine(QWidget, footer_line_UI.Ui_FooterLine):
    """
    ein element für den fuß einer maintable in dem tabelleneigenschaften
    angezeigt werden können;
    es könne mehrer fuß_zeilen definiert werden die in der maintable mit
    'self.insertFooter('TestFoo', 'Baa', 3, 100)' aufgerufen und in einer
    subclass von maintable in 'initUI' geladen werden
    """

    _column_calc = 0
    _decimal = None
    _factor = 1
    _label = ''
    _unit = ''
    _value = ''
    _value_width = ''

    @property  # getter
    def column_calc(self):
        return self._column_calc

    @column_calc.setter
    def column_calc(self, value):
        self._column_calc = value

    @property  # getter
    def decimal(self):
        return self._decimal

    @decimal.setter
    def decimal(self, value):
        self._decimal = value

    @property  # getter
    def factor(self):
        return self._factor

    @factor.setter
    def factor(self, value):
        self._factor = value

    @property  # getter
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self.uiLabelLbl.setText(value)
        self._label = value

    @property  # getter
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self.uiUnitLbl.setText(value)
        self._unit = value

    @property  # getter
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self.uiValueLbl.setText(val)
        self._value = val

    @property  # getter
    def value_width(self):
        return self._value_width

    @value_width.setter
    def value_width(self, val):
        self.uiValueLbl.setMaximumWidth(val)
        self._value_width = val

    def __init__(self, parent, label_text, unit, column_calc, value_width,
                 factor=1, decimal=None, filter_col=None, filter_operator=None,
                 filter_criterion=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

        self.column_calc = column_calc
        self.decimal = decimal
        self.factor = factor
        self.label = label_text
        self.unit = unit
        self.value_width = value_width

        self.filter_col = filter_col
        self.filter_operator = filter_operator
        self.filter_criterion = filter_criterion

        self.uiValueLbl.setFocusPolicy(Qt.NoFocus)

    def update_footer_line(self):
        """
        aktualisiere die footer_line
        :return:
        """
        value_text = ''
        if self.parent.filter_proxy:
            footer_model = self.parent.filter_proxy
            amount = self.calc_column(footer_model, self.column_calc)
            value_text = str(amount)

        self.value = value_text

    def calc_column(self, model, col):
        """
        summiere die werte der angegebenen spalte (col)
        :return: col_sum
        """
        try:
            col_sum = 0
            for i in range(model.rowCount()):
                value = model.data(model.index(i, col), Qt.EditRole)
                if value:
                    if self.filter_col:
                        filter_compare = model.data(
                            model.index(i, self.filter_col), Qt.EditRole)
                        if filter_compare == self.filter_criterion:
                            col_sum = col_sum + value
                    else:
                        if type(value) == str:
                            try:
                                col_sum = col_sum + int(value)
                            except:
                                pass
                        else:
                            col_sum = col_sum + value

            if self.decimal:
                decimal_string = '{:.' + str(self.decimal) + 'f}'
                return decimal_string.format(
                    round(float(col_sum * self.factor),
                          self.decimal)).replace(".", ",")
            else:
                return col_sum * self.factor

        except:
            print(f'Cannot calculate footer value!')
