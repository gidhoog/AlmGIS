# from PyQt5.QtCore import QModelIndex, Qt
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload

from qgis.PyQt.QtCore import QModelIndex, Qt

from app_core import db_session_cm
from app_core.combogroup import ExtendedCombo, ComboModel
from app_core.data_model import BKontakt, BKontaktTyp


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

    def loadComboData(self, session=None, gruppe='a'):
        """

        :param session:
        :param gruppe: a=alle; e=einzelpersonen; g=gemeinschaften
        :return:
        """

        if session is not None:
            self.combo_session = session

        # with db_session_cm(name='load contact-type in contact',
        #                    expire_on_commit=False) as session:

        match gruppe:

            case 'a':
                stmt = select(BKontakt)
            case 'e':
                stmt = select(BKontakt).join(BKontakt.rel_type).where(
                    BKontaktTyp.gemeinschaft == 0)
            case 'g':
                stmt = select(BKontakt).join(BKontakt.rel_type).where(
                    or_((BKontaktTyp.gemeinschaft == 1), (BKontakt.blank_value == 1))
                )

        self._mci_list = self.combo_session.scalars(stmt).unique().all()


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
