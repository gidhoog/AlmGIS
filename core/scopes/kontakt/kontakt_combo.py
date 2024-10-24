#!/usr/bin/env python

from sqlalchemy import asc, func

# from PyQt5.QtCore import Qt
from qgis.PyQt.QtCore import Qt

# from core.combo import Combobox, ComboGroup, ComboColumn, ComboModel

from core.combobox import Combobox, ComboModel, ComboProxyModel
from core.data_model import BContact
from core.scopes.contact.contact import Contact

# import resources_rc


class ContactComboModel(ComboModel):

    header = ['Name',
              'Anschrift']

    def __init__(self, parent=None, mci_list=None) -> None:
        super(ContactComboModel, self).__init__(parent)

    def data(self, index, role = ...):
        super().data(index, role)

        row = index.row()

        # if role == Qt.TextAlignmentRole:
        #
        #     if index.column() in [5, 6]:
        #
        #         return Qt.AlignRight | Qt.AlignVCenter
        #
        #     if index.column() in [1, 2, 4]:
        #
        #         return Qt.AlignHCenter | Qt.AlignVCenter

        if index.column() == 0:
            if role == Qt.DisplayRole:
                return self.mci_list[row].shown_name
                # return self.mci_list[row][0]

        if index.column() == 1:
            if role == Qt.DisplayRole:
                return self.mci_list[row].street


class ContactCombo(Combobox):

    # _model_class = ContactComboModel
    #
    # combo_data_model = BContact
    # combo_item_widget_class = Kontakt
    #
    # combo_widget_title = {'default': 'Kontakt',
    #                       'add': 'neuer Kontakt',
    #                       'edit': 'Kontakt bearbeiten'}
    #
    # column_display = 2
    # editable = True
    # show_view = True
    # use_completer = True

    def __init__(self, parent):
        super(ContactCombo, self).__init__(parent)

        self.parent = parent

        # self.action_list = [self.action_clear,
        #                     self.action_edit,
        #                     self.action_add]
