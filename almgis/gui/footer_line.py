from qga.footer_line import QgaFooterLine

from almgis.zzz_config import Config

class AlmFooterLine(QgaFooterLine):

    def __init__(self, parent, label_text, unit, attribute, column_id=None,
                 value_width=120, factor=1, decimal=None, filter_col=None,
                 filter_operator=None, filter_criterion=None, column_type=int):
        super().__init__(parent, label_text. label_text, unit, attribute,
                         column_id, value_width, factor, decimal, filter_col,
                         filter_operator, filter_criterion, column_type)

        self.colors = Config.Colors