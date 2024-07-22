from PyQt5.QtCore import QModelIndex, Qt
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core import db_session_cm
from core.combogroup import ExtendedCombo, ComboModel
from core.data_model import BKontakt, BKontaktTyp


# from core.scopes.kontakt.kontakt import Kontakt


class ContactCombo(ExtendedCombo):

    def __init__(self, parent):
        super(ContactCombo, self).__init__(parent)

        self.combo_model_class = ContactComboModel
        # self.combo_widget_form = Kontakt
        self.combo_mc = BKontakt

        self.setEditable(True)

        self.combo_view.setColumnWidth(0, 180)
        self.combo_view.setColumnWidth(1, 180)

        self.combobox_line_edit.view.setColumnWidth(0, 180)
        self.combobox_line_edit.view.setColumnWidth(1, 180)

        """make a default setting of the combo_actions"""
        self.action_list = [self.action_clear,
                            self.action_edit,
                            self.action_add]
        """"""

        """set the default sort order"""
        self.combo_proxy_model.sort(0, Qt.AscendingOrder)
        """"""

    def loadData(self):

        with db_session_cm() as session:

            stmt = select(BKontakt).join(BKontakt.rel_type).where(
                BKontaktTyp.gemeinschaft == False)

            self._mci_list = session.scalars(stmt).unique().all()


class ContactComboModel(ComboModel):

    header = ['Name',
              'Anschrift']

    def __init__(self, parent, mci_list=None):
        super(ContactComboModel, self).__init__(parent, mci_list)

    def data(self, index: QModelIndex, role: int = ...):
        # super().data(index, role)

        # if index.column() == 0:
        #
        #     if role == Qt.DisplayRole:
        #
        #         return self.parent._mci_list[index.row()].id

        if index.column() == 0:

            if role == ComboModel.IdRole:

                return self._mci_list[index.row()].id

            if role == ComboModel.MciRole:

                return self._mci_list[index.row()]

            if role == Qt.DisplayRole:

                return self._mci_list[index.row()].name

            if role == Qt.EditRole:

                return self._mci_list[index.row()].name

        if index.column() == 1:

            if role == Qt.DisplayRole:
                return self._mci_list[index.row()].strasse
