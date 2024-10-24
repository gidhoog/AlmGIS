# from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel, \
#     QSortFilterProxyModel
from qgis.PyQt.QtCore import Qt, QModelIndex, QAbstractTableModel, \
    QSortFilterProxyModel
from qgis.PyQt.QtGui import QIcon, QValidator, QKeyEvent
from qgis.PyQt.QtWidgets import QAction, QComboBox, QCompleter, QTableView, \
    QLineEdit, QMenu, QMessageBox

from core import db_session_cm
from core.entity import EntityDialog


class ComboModel(QAbstractTableModel):

    IdRole = Qt.UserRole + 1
    MciRole = Qt.UserRole + 2

    header = []

    def __init__(self, parent, mci_list=None):
        super(ComboModel, self).__init__(parent)

        self.parent = parent
        self._mci_list = mci_list

    def data(self, index: QModelIndex, role: int = ...):
        # super().data(index, role)

        return super().data(index, role)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        # return super().rowCount(parent)

        return len(self._mci_list)

    def columnCount(self, parent: QModelIndex = ...) -> int:

        return len(self.header)

    def headerData(self, column, orientation, role=None):
        """
        wenn individuelle überschriften gesetzt sind (in 'self.header')
        dann nehme diese
        """
        super().headerData(column, orientation, role)

        if self.header:
            if role == Qt.DisplayRole and orientation == Qt.Horizontal:

                return self.header[column]


class ComboView(QTableView):

    def __init__(self, parent):
        super(ComboView, self).__init__(parent)

        self.parent = parent

        self.setSortingEnabled(True)

        self.horizontalHeader().setStretchLastSection(True)


class LineEdit(QLineEdit):
    """the line-edit inside a Combobox"""

    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)

        self.parent = parent

        self.view = ComboView(self)

        self.completer = QCompleter(self)
        self.setCompleter(self.completer)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setPopup(self.view)

        self.completer.popup().setMinimumHeight(self.parent.view_height)
        self.completer.popup().setMinimumWidth(self.parent.view_width)

        self.editingFinished.connect(self.selectCompleterItem)
        self.completer.popup().clicked.connect(self.selectCompleterItem)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super(LineEdit, self).keyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            self.parent.setCurrentIndex(self.parent.fallback_index)

    def selectCompleterItem(self):

        if self.text() not in self.parent.validator_list:

            print(f':::::: {self.text()} not in list!!!!!!!!!!!!')

            msg = QMessageBox(self)
            msg.setWindowTitle("Info")
            msg.setInformativeText("Der Eintrag nicht in der Liste.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

            self.setFocus()

        else:

            index = self.completer.popup().currentIndex()

            current_id = self.completer.popup().model().data(
                self.completer.popup().model().index(index.row(), 0),
                ComboModel.IdRole
            )

            if current_id != None:
                set_index = self.parent.findData(current_id, ComboModel.IdRole)
                self.parent.setCurrentIndex(set_index)


class ComboValidator(QValidator):

    def __init__(self, itemlist,  parent=None):
        super(ComboValidator, self).__init__(parent)

        self.items = itemlist

    def validate(self, _text, _pos):

        for name in self.items:

            if _text.lower() in name.lower():
                return (QValidator.Acceptable, _text, _pos)

        return (QValidator.Invalid, _text, _pos)


class ExtendedCombo(QComboBox):
    """
    combobox with a valitator to enable only inputs that matches with values
    of a given list (validator_list) and popup-view (!!) to select filtered
    items of the popup-list
    """

    combo_widget_title = {'default': 'Kontakt',
                          'add': 'neuer Kontakt',
                          'edit': 'Kontakt bearbeiten'}

    def __init__(self, parent):
        super(ExtendedCombo, self).__init__(parent)

        self.parent = parent

        self.combo_model_class = ComboModel
        self.combo_widget_form = None
        self.combo_mc = None

        self.blank_value_id = 0

        self.fallback_index = None

        self.combo_proxy_model = QSortFilterProxyModel(self)

        self.view_width = 400
        self.view_height = 200

        self.action_clear = ActionClear(self)
        self.action_edit = ActionEdit(self)
        self.action_add = ActionAdd(self)

    def initCombo(self):

        self.combo_model = self.combo_model_class(self, self._mci_list)
        self.combo_proxy_model.setSourceModel(self.combo_model)
        self.combo_proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)

        self.setModel(self.combo_proxy_model)

        if self.isEditable():
            self.completer().setModel(self.combo_proxy_model)

            self.validator_list = [m.name for m in self._mci_list]
            combo_validator = ComboValidator(self.validator_list,
                                             self.combobox_line_edit)
            self.setValidator(combo_validator)

            self.setActions()

    def setComboValue(self, id_value):

        self.fallback_index = self.findData(id_value, ComboModel.IdRole)
        self.setCurrentIndex(self.fallback_index)

    def setEditable(self, editable):

        if editable:
            self.combobox_line_edit = LineEdit(self)
            self.setLineEdit(self.combobox_line_edit)

            self.combo_view = ComboView(self)
            self.setView(self.combo_view)
            self.combo_view.setMinimumHeight(self.view_height)
            self.combo_view.setMinimumWidth(self.view_width)

    def setActions(self):
        """
        set the lineedit-actions depending on the text
        """

        for action in self.action_list:

            # if action.displayRule() is True:
            self.lineEdit().addAction(action, self.lineEdit().TrailingPosition)
            # else:
            #     self.guiCombo.lineEdit().removeAction(action)


class ComboAction(QAction):
    """
    define an action inside an combobox
    """

    item_types = {}
    combo_types = None

    def __init__(self, parent):
        super(ComboAction, self).__init__(parent)

        self.parent = parent

        self.initAction()

        self.triggered.connect(self.doAction)

    def initAction(self):
        """
        init here an individual behavior of this action
        :return:
        """
        pass

    def doAction(self):
        """
        set here the code if the action is triggered
        :return:
        """

    def displayRule(self):
        """
        define the rule to display and enable the action in the editor

        return False to disable the action

        :return: True or False
        """
        return True


class ActionClear(ComboAction):

    def __init__(self, parent):
        super(ActionClear, self).__init__(parent)

        self.setIcon(QIcon(':/svg/resources/icons/reset_blue.svg'))

    def doAction(self, *args, **kwargs):
        super().doAction()

        # index = self.parent.findText('--- --')

        match_index = self.parent.model().match(
            self.parent.model().index(0, 0),
            ComboModel.IdRole,
            self.parent.blank_value_id,
            -1,
            Qt.MatchExactly)

        if match_index:

            self.parent.setCurrentIndex(match_index[0].row())

    def displayRule(self):
        super().displayRule()
        """
        disable this action for the item with id = 0:
        """

        # if self.parent.model().data(self.parent.model().index(
        #         self.parent.currentIndex(), 0), Qt.EditRole) in [0]:
        #     return False
        # else:
        #     return True

        return True


class ActionEdit(ComboAction):

    def __init__(self, parent):
        super(ActionEdit, self).__init__(parent)

        self.setIcon(QIcon(':/svg/resources/icons/edit_yellow.svg'))

    def doAction(self, *args, **kwargs):

        current_mci = self.parent.currentData(ComboModel.MciRole)

        contact_wdg = self.parent.combo_widget_form()
        contact_wdg._commit_on_apply = False
        contact_wdg.setEntitySession(self.parent.combo_session)
        contact_wdg.editEntity(entity_mci=current_mci)

        self.entity_dialog = EntityDialog(parent=self.parent)

        """setze den entity_dialog im entity_widget"""
        contact_wdg.entity_dialog = self.entity_dialog
        """"""

        self.entity_dialog.insertWidget(contact_wdg)
        # self.entity_dialog.resize(self.minimumSizeHint())

        dialog_answer = self.entity_dialog.exec()

        if dialog_answer == 1:
            self.parent.setCurrentIndex(self.parent.currentIndex())

    def displayRule(self):
        super().displayRule()

        if self.parent.model().data(
                self.parent.model().index(
                    self.parent.currentIndex(), 0), Qt.EditRole) in [0]:
            return False
        else:
            return True


class ActionAdd(ComboAction):

    def __init__(self, parent):
        super(ActionAdd, self).__init__(parent)

        self.parent = parent

        self.setIcon(QIcon(':/svg/resources/icons/plus_green.svg'))

    def initAction(self):
        """
        if there are multiple item-types, then set the menu to add multiple
        types; if not, do nothing
        :return:
        """

        super().initAction()

        if hasattr(self.parent, 'combo_data_model'):
            if hasattr(self.parent.combo_data_model, 'rel_type'):
                self.setActionMenu()

    def setActionMenu(self):
        """
        set the action-menu if the are multiple item-types
        :return:
        """

        """query the types from the database"""
        with db_session_cm() as session:
            """expire_on_commit to enable editing child-instances"""
            session.expire_on_commit = False

            type_class = self.parent.combo_data_model.rel_type.property.mapper.class_

            type_instances = session.query(type_class) \
                .filter(type_class.blank_value == 0) \
                .all()
        """"""

        """create the menu with the queried types"""
        self.action_menu = QMenu(self.parent)
        for type in type_instances:
            action = QAction(type.name, self.action_menu)
            action.triggered.connect(lambda a_id, type_inst=type:
                                     self.doAction(mulitple_types=True,
                                                   type_inst=type_inst))
            self.action_menu.addAction(action)
        self.setMenu(self.action_menu)
        """"""

    def doAction(self, mulitple_types=False, type_inst=None):

        # new_mci = BContact()
        new_mci = self.parent.combo_mc()

        contact_wdg = self.parent.combo_widget_form()
        contact_wdg.editEntity(entity_mci=new_mci)

        self.entity_dialog = EntityDialog(parent=self.parent)

        """setze den entity_dialog im entity_widget"""
        contact_wdg.entity_dialog = self.entity_dialog
        """"""

        self.entity_dialog.insertWidget(contact_wdg)
        # self.entity_dialog.resize(self.minimumSizeHint())

        dialog_answer = self.entity_dialog.exec()

        if dialog_answer == 1:

            new_index = len(self.parent._mci_list)

            self.parent.model().sourceModel().layoutAboutToBeChanged.emit()

            self.parent._mci_list.append(new_mci)

            self.parent.model().sourceModel().layoutChanged.emit()

            self.parent.setCurrentIndex(new_index)
