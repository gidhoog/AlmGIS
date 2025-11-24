from qga.core.tools import getDmiState
from sqlalchemy import select, or_

from qgis.PyQt.QtCore import QModelIndex, Qt

from almgis.core.combobox import AlmComboModel, AlmExtendedCombo, AlmComboActionAdd
from almgis.database.models import DmKontakt, DmKontaktGemTyp


class ContactCombo(AlmExtendedCombo):

    def __init__(self, parent):
        super(ContactCombo, self).__init__(parent)

        self.combo_model_class = ContactComboModel
        # self.combo_widget_form = Kontakt
        self.combo_mc = DmKontakt

        self.setEditable(True)
        self.validator_mc_attr = 'name'

        # self.combo_view.setColumnWidth(0, 180)
        # self.combo_view.setColumnWidth(1, 180)
        #
        # self.combobox_line_edit.view.setColumnWidth(0, 180)
        # self.combobox_line_edit.view.setColumnWidth(1, 180)

        # self.action_add = AlmComboActionAdd(self, self.session)

        # """make a default setting of the combo_actions"""
        # self.action_list = [self.action_clear,
        #                     self.action_edit,
        #                     self.action_add]
        # """"""

        """set the default sort order"""
        self.combo_proxy_model.sort(0, Qt.AscendingOrder)
        """"""

    def setActionList(self):
        super().setActionList()

        self.action_add = AlmComboActionAdd(self, self.session)

        """make a default setting of the combo_actions"""
        self.action_list = [self.action_clear,
                            self.action_edit,
                            self.action_add]
        """"""

    def loadComboData(self, session=None, gruppe='a'):
        """

        :param session:
        :param gruppe: a=alle; e=einzelpersonen; g=gemeinschaften
        :return:
        """

        self._dmi_list = []

        if session is not None:
            self.session = session

        match gruppe:

            case 'a':
                stmt = select(DmKontakt)
            case 'e':
                stmt = select(DmKontakt).where(DmKontakt.type_id == 0)
            case 'g':
                stmt = select(DmKontakt).join(DmKontakt.rel_type).where(
                    or_((DmKontaktGemTyp.gemeinschaft == 1), (DmKontakt.blank_value == 1))
                )

        self._dmi_list = self.session.scalars(stmt).unique().all()


class ContactComboModel(AlmComboModel):

    header = ['Name',
              'Anschrift']

    def __init__(self, parent, dmi_list=None):
        super(ContactComboModel, self).__init__(parent, dmi_list)

    def data(self, index: QModelIndex, role: int = ...):
        # super().data(index, role)

        # if index.column() == 0:
        #
        #     if role == Qt.DisplayRole:
        #
        #         return self.parent._dmi_list[index.row()].id

        if index.column() == 0:

            if role == AlmComboModel.IdRole:

                return self._dmi_list[index.row()].id

            if role == AlmComboModel.DmiRole:

                return self._dmi_list[index.row()]

            if role == Qt.DisplayRole:

                return self._dmi_list[index.row()].name

            if role == Qt.EditRole:

                return self._dmi_list[index.row()].name

        if index.column() == 1:

            if role == Qt.DisplayRole:
                return self._dmi_list[index.row()].strasse
