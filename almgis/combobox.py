from qga.combobox import QgaComboModel, QgaComboView, \
    QgaExtendedCombo, QgaComboActionAdd

# from almgis.data_session import session_cm


class AlmComboModel(QgaComboModel): pass


class AlmComboView(QgaComboView): pass


class AlmExtendedCombo(QgaExtendedCombo): pass


class AlmComboActionAdd(QgaComboActionAdd):

    def __init__(self, parent, session):
        super(AlmComboActionAdd, self).__init__(parent, session)

        # self.session_cm = session_cm