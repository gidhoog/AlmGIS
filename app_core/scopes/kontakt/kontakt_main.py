# from PyQt5.QtCore import Qt
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (QLabel, QComboBox,
                                 QSpacerItem, QSizePolicy, QHBoxLayout,
                                 QMenu, QAction, QToolButton)
from qgis.PyQt.QtGui import QIcon
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app_core import db_session_cm, config, DbSession
from app_core.data_view import DataView, TableModel
from app_core.entity import EntityDialog
from app_core.main_widget import MainWidget

from app_core.data_model import BKontakt, BKontaktTyp
from app_core.scopes.kontakt.kontakt import Kontakt, KontaktEinzel


class KontaktEntityDialog(EntityDialog):

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.dialog_window_title = 'Kontakt'


class KontaktMainWidget(MainWidget):

    def __init__(self, parent=None, session=None):
        super().__init__(parent, session)

        self.uiTitleLbl.setText('alle Kontakte')

        self.kontakt_table = KontaktMain(self)

        # with db_session_cm(name='main-widget - kontakt',
        #                    expire_on_commit=False) as session:

        self.kontakt_table.setDataviewSession(session)
        self.kontakt_table.initDataView()

    def initMainWidget(self):
        super().initMainWidget()

        self.uiMainVLay.addWidget(self.kontakt_table)
        # self.kontakt_table.loadData()
        # self.kontakt_table.initDataView()


class KontaktModel(TableModel):

    header = [
        'Typ',
        'Name',
        'Vertreter',
        'Adresse',
        'Telefon',
        'e-Mail'
    ]

    def data(self, index, role=None):

        row = index.row()
        # col = index.column()

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
                return self.mci_list[row].rel_type.name
                # return self.mci_list[row][0]

            if role == Qt.EditRole:
                return self.mci_list[row].rel_type.id


        if index.column() == 1:
            if role == Qt.DisplayRole:
                return self.mci_list[row].name

        if index.column() == 2:
            if role == Qt.DisplayRole:

                if self.mci_list[row].rel_type.id == 0:
                    return ''
                else:
                    return self.mci_list[row].rel_vertreter.name

        if index.column() == 3:
            if role == Qt.DisplayRole:
                return self.mci_list[row].adresse
                # return self.mci_list[row][1]

        if index.column() == 4:
            if role == Qt.DisplayRole:
                return self.mci_list[row].telefon_all

        if index.column() == 5:
            if role == Qt.DisplayRole:
                return self.mci_list[row].mail_all


class KontaktMain(DataView):

    # data_view_mc = BContact

    entitiy_amount_text = ["Kontakt", "Kontakte", "kein Kontakt"]
    _delete_window_title = ["Kontakt löschen", "Kontakte löschen"]
    _delete_window_text_single = "Soll der ausgewählte Kontakt " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Kontakte wirklich gelöscht werden?"]
    _delete_text = ["Der Kontakt", "kann nicht gelöscht werden, da er "
                    "verwendet wird!"]

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.entity_dialog_class = KontaktEntityDialog
        self.entity_widget_class = KontaktEinzel
        self._entity_mc = BKontakt
        self._model_class = KontaktModel
        """"""

    def deleteCheck(self, mci):

        with db_session_cm() as session:
            all_vertreter_ids_stmt = select(BKontakt.vertreter_id)
            all_vertreter_ids = session.scalars(all_vertreter_ids_stmt).all()

            # bewirtschafter_ids_stmt = select(BAkt.bewirtschafter_id)

        if mci.id in all_vertreter_ids:
            return False
        else:
            return True

    def initUi(self):
        super().initUi()

        self.setStretchMethod(2)

        self.add_menu = QMenu(self)

        action_einzel = QAction(QIcon(":/svg/resources/icons/person.svg"),
                                'Einzelperson', self)
        action_gemeinschaft = QAction(QIcon(":/svg/resources/icons/group.svg"),
                                      'Gemeinschaft', self)

        action_einzel.triggered.connect(lambda: self.addKontakt("einzel"))
        action_gemeinschaft.triggered.connect(lambda: self.addKontakt("gem"))


        self.add_menu.addAction(action_einzel)
        self.add_menu.addAction(action_gemeinschaft)

        self.uiAddDataTbtn.setMenu(self.add_menu)
        self.uiAddDataTbtn.setPopupMode(QToolButton.InstantPopup)

    def addKontakt(self, type):

        if type == 'einzel':
            entity_widget = KontaktEinzel(self)
        elif type == 'gem':
            entity_widget = Kontakt(self)

        entity_widget.initEntityWidget()

        mci = BKontakt()

        entity_widget.purpose = 'add'

        self.edit_entity = mci

        self.editRow(entity_widget=entity_widget,
                     entity_mci=mci)

    def finalInit(self):
        super().finalInit()

        # self.view.setColumnHidden(0, True)
        # self.view.setColumnHidden(1, True)
        # self.view.setColumnHidden(3, True)

        self.view.sortByColumn(1, Qt.AscendingOrder)

        self.view.resizeColumnsToContents()

    def setFilterUI(self):
        """
        setze das layout für die filter
        :return:
        """

        filter_lay = QHBoxLayout(self)

        """filter typen"""

        self.filter_type_lbl = QLabel(self)
        self.filter_type_lbl.setText('Typ:')
        kontakt_type_lbl_font = self.filter_type_lbl.font()
        kontakt_type_lbl_font.setFamily(config.font_family)
        self.filter_type_lbl.setFont(kontakt_type_lbl_font)
        self.filter_type_lbl.setVisible(False)

        self.filter_type_input_wdg = QComboBox(self)

        self.filter_type_input_wdg.addItem('--- alle Typen ---', -1)

        with db_session_cm(name='contact type filter') as session:

            contact_type_stmt = select(BKontaktTyp)
            contact_type_list = session.scalars(contact_type_stmt).all()

            for kontact_type in contact_type_list:
                self.filter_type_input_wdg.addItem(kontact_type.name,
                                                   kontact_type.id)

        kontakt_type_input_wdg_font = self.filter_type_input_wdg.font()
        kontakt_type_input_wdg_font.setPointSize(11)
        kontakt_type_input_wdg_font.setFamily(config.font_family)
        self.filter_type_input_wdg.setFont(kontakt_type_input_wdg_font)

        # self.filter_type_input_wdg.currentIndexChanged.connect(self.useFilter)
        self.filter_type_input_wdg.currentTextChanged.connect(
            self.applyFilter)
        """"""

        # """filter name"""
        # # filter_name = FilterElement(self)
        # # filter_name.uiLabelLbl.setText('Name:')
        # self.filter_name_lbl = QLabel(self)
        #
        # name_lbl_font = self.filter_name_lbl.font()
        # name_lbl_font.setFamily(config.font_family)
        # self.filter_name_lbl.setFont(name_lbl_font)
        #
        # self.filter_name_lbl.setText('Name:')
        # self.filter_name_lbl.setVisible(False)
        #
        # self.filter_name_input_wdg = QLineEdit(self)
        #
        # name_input_wdg_font = self.filter_name_input_wdg.font()
        # name_input_wdg_font.setPointSize(11)
        # name_input_wdg_font.setFamily(config.font_family)
        # self.filter_name_input_wdg.setFont(name_input_wdg_font)
        #
        # self.filter_name_input_wdg.setPlaceholderText('Name')
        # self.filter_name_input_wdg.setClearButtonEnabled(True)
        # self.filter_name_input_wdg.setMaximumWidth(200)
        # # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)
        #
        # self.filter_name_input_wdg.textChanged.connect(self.useFilter)
        #
        # # filter_lay.addWidget(filter_name)
        # """"""
        #
        # """filter adresse"""
        # # filter_az = FilterElement(self)
        # # filter_az.uiLabelLbl.setText('AZ:')
        #
        # self.filter_adr_lbl = QLabel(self)
        #
        # adr_lbl_font = self.filter_adr_lbl.font()
        # adr_lbl_font.setFamily(config.font_family)
        # self.filter_adr_lbl.setFont(adr_lbl_font)
        #
        # self.filter_adr_lbl.setText('Adresse:')
        # self.filter_adr_lbl.setVisible(False)
        #
        # self.filter_adr_input_wdg = QLineEdit(self)
        # self.filter_adr_input_wdg.setPlaceholderText('Adresse')
        # adr_input_wdg_font = self.filter_adr_input_wdg.font()
        # adr_input_wdg_font.setPointSize(11)
        # adr_input_wdg_font.setFamily(config.font_family)
        # self.filter_adr_input_wdg.setFont(adr_input_wdg_font)
        # self.filter_adr_input_wdg.setClearButtonEnabled(True)
        # self.filter_adr_input_wdg.setMaximumWidth(80)
        # # filter_az.uiFilterElementLay.insertWidget(1, self.filter_adr_input_wdg)
        #
        # self.filter_adr_input_wdg.textChanged.connect(self.useFilter)

        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Minimum,
                                 QSizePolicy.Minimum)
        filter_lay.addItem(spacerItem1)

        filter_lay.addWidget(self.filter_type_lbl)
        filter_lay.addWidget(self.filter_type_input_wdg)
        # filter_lay.addWidget(self.filter_name_lbl)
        # filter_lay.addWidget(self.filter_name_input_wdg)
        # filter_lay.addWidget(self.filter_adr_lbl)
        # filter_lay.addWidget(self.filter_adr_input_wdg)

        """"""

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        filter_lay.addItem(spacerItem)

        self.uiHeaderHley.insertLayout(1, filter_lay)

    def applyFilter(self):

        if self.filter_type_input_wdg.currentData(Qt.UserRole) == -1:
            self.filter_type_lbl.setVisible(False)
        else:
            self.filter_type_lbl.setVisible(True)

        super().applyFilter()

    def useFilter(self):

        name_text = self.filter_name_input_wdg.text()
        adr_text = self.filter_adr_input_wdg.text()
        kontakt_type_id = self.filter_type_input_wdg.currentData(Qt.UserRole)

        name_expr = f"lower(\"name\") LIKE '%{name_text}%'"
        adr_expr = f"lower(\"adresse\") LIKE '%{adr_text}%'"
        kontakt_type_expr = f"(\"typ_id\") = {kontakt_type_id}"

        expr_list = []

        if name_text != '':
            self.filter_name_lbl.setVisible(True)
            expr_list.append(name_expr)
        else:
            self.filter_name_lbl.setVisible(False)

        if adr_text != '':
            self.filter_adr_lbl.setVisible(True)
            expr_list.append(adr_expr)
        else:
            self.filter_adr_lbl.setVisible(False)

        if kontakt_type_id != -1:
            self.filter_type_lbl.setVisible(True)
            expr_list.append(kontakt_type_expr)
        else:
            self.filter_type_lbl.setVisible(False)

        if expr_list == []:
            self._gis_layer.setSubsetString('')
        else:

            expr_string = " and ".join(expr for expr in expr_list)
            self._gis_layer.setSubsetString(expr_string)

            print(f'expression string: {expr_string}')

        print(f'expr_list: {expr_list}')

        self.updateFooter()

    def useFilterScope(self, source_row, source_parent):
        super().useFilterScope(source_row, source_parent)

        """filter contact_typ"""
        contact_type = self.filter_proxy.sourceModel() \
            .data(self.filter_proxy.sourceModel().index(source_row, 0),
                  Qt.EditRole)
        # if self.filter_type_input_wdg.currentText() != "--- alle Typen ---":
        if self.filter_type_input_wdg.currentData(Qt.UserRole) != -1:
            # return False
            if contact_type != self.filter_type_input_wdg.currentData(Qt.UserRole):
                return False
        """"""

    def getDeleteInfo(self, index=None):
        super().getDeleteInfo(index)

        del_info = self.filter_proxy.data(
            self.filter_proxy.index(
                index.row(), 1))

        return del_info

    def get_entity_widget_class(self, entity_mci):

        if entity_mci.rel_type.gemeinschaft:
            return Kontakt
        else:
            return KontaktEinzel

    def getMciList(self, session):

        stmt = (select(BKontakt)
        .options(
            joinedload(BKontakt.rel_type)
        )
                .where(BKontakt.blank_value == 0))

        mci = session.scalars(stmt).all()

        return mci

    def getCustomData(self, session):

        custom_data = {}

        type_stmt = select(BKontaktTyp).order_by(BKontaktTyp.sort)
        type_mci = session.scalars(type_stmt).all()

        custom_data['typ'] = type_mci

        vertr_kontakte_stmt = ((select(BKontakt)
                         .options(joinedload(BKontakt.rel_type)))
                         .where(BKontaktTyp.gemeinschaft == 0))
        vertr_kontakte_mci = session.scalars(vertr_kontakte_stmt).all()

        custom_data['vertr_kontakte'] = vertr_kontakte_mci

        return custom_data
