from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtGui import QColor

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
    _attribute = ''
    _decimal = None
    _factor = 1
    _label = ''
    _unit = ''
    _value = ''
    _value_sel = ''
    _value_width = ''

    @property  # getter
    def attribute(self):
        return self._attribute

    @attribute.setter
    def attribute(self, value):
        self._attribute = value

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
        self.uiValueLedit.setText(val)
        self._value = val

    @property  # getter
    def value_sel(self):
        return self._value_sel

    @value_sel.setter
    def value_sel(self, val):
        self.uiValueSelLedit.setText(val)
        self._value_sel = val

    @property  # getter
    def value_width(self):
        return self._value_width

    @value_width.setter
    def value_width(self, val):
        self.uiValueLedit.setMaximumWidth(val)
        self.uiValueSelLedit.setMaximumWidth(val)
        self._value_width = val

    def __init__(self, parent, label_text, unit, attribute, value_width,
                 factor=1, decimal=None, filter_attribute='', filter_operator=None,
                 filter_criterion=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

        self.attribute = attribute
        self.decimal = decimal
        self.factor = factor
        self.label = label_text
        self.unit = unit
        self.value_width = value_width

        self.filter_attribute = filter_attribute
        self.filter_operator = filter_operator
        self.filter_criterion = filter_criterion

        self.uiValueLedit.setFocusPolicy(Qt.NoFocus)

        """setze die Hintergrundfarbe für das LineEdit mit der Summe der
        ausgewählten Zeilen"""
        pal_sel = self.uiValueSelLedit.palette()
        pal_sel.setColor(self.uiValueSelLedit.backgroundRole(), QColor(130, 185, 230))
        self.uiValueSelLedit.setPalette(pal_sel)
        """"""

        self.uiValueSelLedit.setVisible(False)

    def update_footer_line(self):
        """
        aktualisiere die Spaltensummen in den Fußzeilen
        :return:
        """
        value_text = ''
        value_sel_text = ''

        field_names = [field for field in self.parent._gis_layer.fields()]
        field_type = [f for f in field_names if self.attribute == f.name()][0].typeName()

        sel_feature_ids = self.parent._gis_layer.selectedFeatureIds()

        if field_type == 'integer':
            amount = 0
            amount_sel = 0
        if field_type == 'double':
            amount = 0.00
            amount_sel = 0.00

        calc_amount = self.calc_all_values(amount)
        calc_amount_sel = self.calc_sel_values(amount_sel, sel_feature_ids)

        value_text = str(self.round_value(calc_amount, self.decimal, self.factor))
        value_sel_text = str(self.round_value(calc_amount_sel, self.decimal, self.factor))

        self.value = value_text
        self.value_sel = value_sel_text

        """steuere die Sichtbarkeit der des Wertes für ausgewählte Zeilen"""
        if len(sel_feature_ids) > 0:
            self.uiValueSelLedit.setVisible(True)
        else:
            self.uiValueSelLedit.setVisible(False)
        """"""

    def calc_all_values(self, amount):

        for feat in self.parent._gis_layer.getFeatures():

            if self.filter_attribute == '':
                amount = amount + feat.attribute(self.attribute)
            else:
                if feat.attribute(self.filter_attribute) == self.filter_criterion:
                    amount = amount + feat.attribute(self.attribute)

        return amount

    def calc_sel_values(self, amount_sel, sel_feature_ids):

        for feat_id in sel_feature_ids:

            feat = self.parent._gis_layer.getFeature(feat_id)

            if self.filter_attribute == '':
                amount_sel = amount_sel + feat.attribute(self.attribute)
            else:
                if feat.attribute(self.filter_attribute) == self.filter_criterion:
                    amount_sel = amount_sel + feat.attribute(self.attribute)

        return amount_sel

    def round_value(self, value, decimal, factor):

        if decimal:

            decimal_string = '{:.' + str(decimal) + 'f}'
            result = decimal_string.format(
                round(float(value * factor),
                      decimal)).replace(".", ",")

            return result

        return value

    # def calc_column(self, model, col, sel_indexes=None):
    #     """
    #     summiere die werte der angegebenen spalte (col)
    #
    #     :param model: table_model
    #     :param col: int
    #     :param sel_indexes: list
    #     :return: result, result_sel
    #     """
    #     try:
    #         col_sel_sum = 0
    #         col_sum = 0
    #         for i in range(model.rowCount()):
    #             value = model.data(model.index(i, col), Qt.EditRole)
    #             if value:
    #                 if self.filter_col:
    #                     filter_compare = model.data(
    #                         model.index(i, self.filter_col), Qt.EditRole)
    #                     if filter_compare == self.filter_criterion:
    #                         col_sum = col_sum + value
    #                         if sel_indexes:
    #                             if i in [x.row() for x in sel_indexes]:
    #                                 col_sel_sum = col_sel_sum + value
    #                 else:
    #                     if type(value) == str:
    #                         try:
    #                             col_sum = col_sum + int(value)
    #                             if sel_indexes:
    #                                 if i in [x.row() for x in sel_indexes]:
    #                                     col_sel_sum = col_sel_sum + int(value)
    #                         except:
    #                             print(f'Cannot sum footer values!')
    #                     else:
    #                         col_sum = col_sum + value
    #                         if sel_indexes:
    #                             if i in [x.row() for x in sel_indexes]:
    #                                 col_sel_sum = col_sel_sum + value
    #
    #         if self.decimal:
    #             decimal_string = '{:.' + str(self.decimal) + 'f}'
    #             result = decimal_string.format(
    #                 round(float(col_sum * self.factor),
    #                       self.decimal)).replace(".", ",")
    #             result_sel = decimal_string.format(
    #                 round(float(col_sel_sum * self.factor),
    #                       self.decimal)).replace(".", ",")
    #         else:
    #             result = col_sum * self.factor
    #             result_sel = col_sel_sum * self.factor
    #         return result, result_sel
    #
    #     except:
    #         print(f'Cannot calculate footer value!')
