from pathlib import Path

from PyQt5.QtCore import pyqtSlot, QVariant, QModelIndex, QAbstractTableModel
from PyQt5.QtWidgets import QDialog
from qga.filter import QgaFilter
from qga.layer import VectorLayerFactory, GeometryType, QgaFeature
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (QLabel, QComboBox, QLineEdit,
                                 QSpacerItem, QSizePolicy, QHBoxLayout,
                                 QMenu, QAction, QToolButton)
from qgis.PyQt.QtGui import QIcon
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from almgis import settings_general
# from almgis.data_session import session_cm
from qga.data_view import QgaTableModel, QgaDataView

from almgis.data_session import session_cm
from almgis.data_view import AlmDataView
from qga.main_widget import QgaMainWidget

from almgis.data_model import DmKontakt, DmKontaktGemTyp, DmAkt, DmKontaktType
from almgis.entity import AlmEntityDialog
from almgis.fields import KontaktField, GeneralField
from almgis.scopes.kontakt.kontakt import Kontakt, KontaktEinzel
from almgis.scopes.kontakt.kontakt_columns import KontaktNameCol, \
    KontaktAdresseCol, KontaktTypeCol, KontaktGemTypeCol


class KontaktEntityDialog(AlmEntityDialog):

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.dialog_window_title = 'Kontakt'

    def accept(self):
        # super().accept()

        accepted_entity = self.dialogWidget.acceptEntity()

        if accepted_entity is not False:

            if self.dialogWidget.purpose == 'add':
                self.parent.dmi_list.append(accepted_entity)

            self.parent.update_data_view.emit(self.dialogWidget.purpose,
                                              False)

            QDialog.accept(self)


class KontaktMainWidget(QgaMainWidget):

    def __init__(self, parent=None, session=None):
        super().__init__(parent, session)

        self.uiTitleLbl.setText('alle Kontakte')
        self.main_wdg = KontaktMain(self)

    def createMw(self):

        self.main_wdg.initDataView()

        self.initMainWidget()

    def initMainWidget(self):
        super().initMainWidget()

        self.uiMainVlay.addWidget(self.main_wdg)


class KontaktModel(QgaTableModel):
# class KontaktModel(QgaGisTableModel):

    # header = [
    #     'Typ',
    #     'Name',
    #     'Vertreter',
    #     'Adresse',
    #     'Telefon',
    #     'e-Mail',
    #     'Verwendung'
    # ]

    def __init__(self, dmi_list=None, layerCache=None,
                 columns=None, parent=None):
        super().__init__(dmi_list, layerCache, columns, parent)

        print(f'....')

    def data(self, index: QModelIndex, role: int = ...):

        if role == Qt.TextAlignmentRole:
            # Set alignment for the "Age" column (column index 1)
            if index.column() == 1:
                return Qt.AlignHCenter | Qt.AlignVCenter

        if role == Qt.DisplayRole:
            # Append a string to the "Name" column (column index 0)
            if index.column() == 1:
                current_value = super().data(index, role)
                # return f"{current_value} - Edited"
                return f"{current_value} - AAA"

        return super().data(index, role)

    # def data(self, index, role):
    #
    #     if not self.parent.gis_mode:
    #
    #         if role == Qt.TextAlignmentRole:
    #             # Set alignment for the "Age" column (column index 1)
    #             if index.column() == 0:
    #                 return Qt.AlignHCenter | Qt.AlignVCenter
    #
    #         if role == Qt.DisplayRole:
    #
    #             column = self._columns[index.column()]
    #             # value = self._dmi_list[index.row()][index.column()]
    #             dmi = self._dmi_list[index.row()]
    #
    #             # Delegate role handling to the column class
    #             return column.handle_role(role, dmi)
    #
    #     return super().data(index, role)
    #
    # def rowCount(self, parent: QModelIndex = ...):
    #     """
    #     definiere die zeilenanzahl
    #     """
    #
    #     return len(self._dmi_list)
    #
    # def columnCount(self, parent: QModelIndex = ...):
    #     """
    #     definiere die spaltenanzahl
    #     """
    #     # return len(self.header)
    #     return len(self._columns)
    #
    # def headerData(self, column, orientation, role=None):
    #     """
    #     wenn individuelle überschriften gesetzt sind (in 'self.header')
    #     dann nehme diese
    #     """
    #     if orientation == Qt.Horizontal and role == Qt.DisplayRole:
    #         return self._columns[column].name
    #     return QVariant()

    # def flags(self, index):  # to make the table(-cells) editable
    #     if not index.isValid():
    #         return Qt.ItemIsEnabled
    #
    #     return Qt.ItemFlags(
    #         QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)


        # if not index.isValid():
        #     return QVariant()
        #
        # column = self._columns[index.column()]
        # # value = self._dmi_list[index.row()][index.column()]
        # dmi = self._dmi_list[index.row()]
        #
        # # Delegate role handling to the column class
        # return column.handle_role(role, dmi)

    # def data(self, index, role=None):
    #
    #     row = index.row()
    #     # col = index.column()
    #
    #     # if role == Qt.TextAlignmentRole:
    #     #
    #     #     if index.column() in [5, 6]:
    #     #
    #     #         return Qt.AlignRight | Qt.AlignVCenter
    #     #
    #     #     if index.column() in [1, 2, 4]:
    #     #
    #     #         return Qt.AlignHCenter | Qt.AlignVCenter
    #
    #     if index.column() == 0:
    #         if role == Qt.DisplayRole:
    #
    #             if self.parent.dmi_list[row].type_id == 0:
    #                 return self.parent.dmi_list[row].rel_type.name
    #             else:
    #                 return self.parent.dmi_list[row].rel_gem_type.name
    #             # return self.dmi_list[row][0]
    #
    #         if role == Qt.EditRole:
    #             return self.parent.dmi_list[row].rel_type.id
    #
    #     if index.column() == 1:
    #         if role == Qt.DisplayRole:
    #             return self.parent.dmi_list[row].name
    #         if role == Qt.EditRole:
    #             return self.parent.dmi_list[row].name
    #
    #     if index.column() == 2:
    #         if role == Qt.DisplayRole:
    #
    #             if self.parent.dmi_list[row].rel_type.id == 0:
    #                 return ''
    #             else:
    #                 return self.parent.dmi_list[row].rel_vertreter.name
    #
    #     if index.column() == 3:
    #         if role == Qt.DisplayRole:
    #             return self.parent.dmi_list[row].adresse
    #             # return self.dmi_list[row][1]
    #
    #     if index.column() == 4:
    #         if role == Qt.DisplayRole:
    #             return self.parent.dmi_list[row].telefon_all
    #
    #     if index.column() == 5:
    #         if role == Qt.DisplayRole:
    #             return self.parent.dmi_list[row].mail_all
    #
    #     if index.column() == 6:
    #         if role == Qt.DisplayRole:
    #             verwendung = []
    #             if self.parent.dmi_list[row].rel_akt is not None:
    #                 for a in self.parent.dmi_list[row].rel_akt:
    #                     verwendung.append(f'Akt: {a.name}')
    #             if self.parent.dmi_list[row].children is not None:
    #                 for n in self.parent.dmi_list[row].children:
    #                     verwendung.append(f'VertreterIn: {n.name}')
    #
    #             verwendung_text = ", ".join(str(v) for v in verwendung)
    #
    #             return verwendung_text


class KontaktMain(AlmDataView):

    _model_class = KontaktModel
    _entity_dmc = DmKontakt
    _type_dmc = DmKontaktType

    entity_dialog_class = KontaktEntityDialog

    entitiy_amount_text = ["Kontakt", "Kontakte", "kein Kontakt"]
    _delete_window_title = ["Kontakt löschen", "Kontakte löschen"]
    _delete_window_text_single = "Soll der ausgewählte Kontakt " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Kontakte wirklich gelöscht werden?"]
    _delete_text = ["Der Kontakt", "kann nicht gelöscht werden, da er "
                    "verwendet wird!"]

    def __init__(self, parent=None, gis_mode=False):
        super(__class__, self).__init__(parent, gis_mode)
        # self.initUi()

        filter_name = QgaFilter('Name', str)
        self.filters.append(filter_name)

        self.layer = VectorLayerFactory.createLayer(
            'kontakte',
            geometry_type=GeometryType.NONE,
            fields_list=self.getFeatureFields()
        )

    def deleteCheck(self, dmi):

        with session_cm() as session:
            all_vertreter_ids_stmt = select(DmKontakt.vertreter_id)
            all_vertreter_ids = session.scalars(all_vertreter_ids_stmt).all()

            bewirtschafter_ids_stmt = select(DmAkt.bewirtschafter_id)
            bewirtschafter_ids = session.scalars(bewirtschafter_ids_stmt).all()

        if dmi.id in all_vertreter_ids or dmi.id in bewirtschafter_ids:
            print(f'====> dmi in use: {dmi}')
            return False
        else:
            return True

    def signals(self):
        super().signals()

        # self.uiAddDataTbtn.clicked.disconnect(self.add_row)

    def initUi(self):
        super().initUi()

        self.setStretchMethod(2)

        # """auswahl in der 'add-toolbox' um aus einzel- und gemeinschafts-
        # kontakt wählen zu können"""

        # self.add_menu = QMenu(self)

        # self.action_einzel = QAction(self.uiAddDataTbtn)
        # self.action_einzel.setText('Einzelperson')
        # self.action_einzel.setIcon(QIcon(":/svg/resources/icons/person.svg"))
        # self.uiAddDataTbtn.addAction(self.action_einzel)
        #
        # self.action_gemeinschaft = QAction(self.uiAddDataTbtn)
        # self.action_gemeinschaft.setText('Gemeinschaft')
        # self.action_gemeinschaft.setIcon(QIcon(":/svg/resources/icons/group.svg"))
        # self.uiAddDataTbtn.addAction(self.action_gemeinschaft)
        #
        # self.action_einzel.triggered.connect(self.addEinzelKontakt)
        # # self.action_einzel..connect(lambda x: self.fn(x))
        # self.action_gemeinschaft.triggered.connect(self.addGemKontakt)
        #
        # # self.add_menu.addAction(self.action_einzel)
        # # self.add_menu.addAction(action_gemeinschaft)
        #
        # """"""
        #
        # # self.uiAddDataTbtn.setMenu(self.add_menu)
        # self.uiAddDataTbtn.setPopupMode(QToolButton.InstantPopup)

    def testAction(self, bbb):

        print(f'test action: {bbb}')

    # @pyqtSlot()
    @staticmethod
    def fn(checked):

        print(f'ff: {checked}')
        # self.addKontakt('einzel')

    def addEinzelKontakt(self):

        print(f'...')

        entity_widget = KontaktEinzel(self)
        self.addEntity(entity_wdg=entity_widget)
        # self.openNewKontakt(entity_widget)

    def addGemKontakt(self):

        print(f'...')

        entity_widget = Kontakt(self)
        self.addEntity(entity_wdg=entity_widget)

        # self.openNewKontakt(entity_widget)

    # def openNewKontakt(self, entity_widget):
    #
    #     # entity_widget.initEntityWidget()
    #     entity_widget.setupCodeUi()
    #
    #     dmi = BKontakt()
    #
    #     entity_widget.purpose = 'add'
    #
    #     self.edit_entity = dmi
    #     self.session.add(dmi)
    #
    #     self.editRow(entity_widget=entity_widget,
    #                  entity_dmi=dmi)

    # def addKontakt(self, type='einzel'):
    #
    #     print(f'...')
    #
    #     if type == 'einzel':
    #         entity_widget = KontaktEinzel(self)
    #     elif type == 'gem':
    #         entity_widget = Kontakt(self)
    #
    #     entity_widget.initEntityWidget()
    #
    #     dmi = BKontakt()
    #
    #     entity_widget.purpose = 'add'
    #
    #     self.edit_entity = dmi
    #     self.dataview_session.add(dmi)
    #
    #     self.editRow(entity_widget=entity_widget,
    #                  entity_dmi=dmi)

    def finalInit(self):
        super().finalInit()

        # self.view.setColumnHidden(0, True)
        # self.view.setColumnHidden(1, True)
        # self.view.setColumnHidden(3, True)

        self.view.sortByColumn(1, Qt.AscendingOrder)

        self.view.resizeColumnsToContents()

    def getFeatureFields(self):

        k_id = GeneralField.Id()
        k_name = KontaktField.Name()
        k_adresse = KontaktField.Adresse()
        k_telefon_all = KontaktField.TelefonAll()

        # type_fld = QgaField("type", QVariant.String)
        # gem_type_fld = QgaField("gem_type", QVariant.String)
        # name_fld = QgaField("name", QVariant.String)
        # adresse_fld = QgaField("adresse", QVariant.String)

        self.fields.append(k_id)
        self.fields.append(k_name)
        self.fields.append(k_adresse)
        self.fields.append(k_telefon_all)

        return self.fields

    # def setFeatureFields(self):
    #
    #     type_fld = QgaField("type", QVariant.String)
    #     gem_type_fld = QgaField("gem_type", QVariant.String)
    #     name_fld = QgaField("name", QVariant.String)
    #     adresse_fld = QgaField("adresse", QVariant.String)
    #
    #     self.fields.append(type_fld,
    #                        gem_type_fld,
    #                        name_fld,
    #                        adresse_fld
    #                        )

    def setFeatureAttributes(self, feature, dmi):

        # feature['type'] = dmi.rel_type.name
        # feature['gem_type'] = dmi.rel_gem_type.name
        # feature['name'] = dmi.name
        # feature['adresse'] = dmi.adresse

        for field in self.fields:

            # feature[field.name()] = field.fieldValue(dmi)
            feature[field.name()] = field.getFieldValue(dmi)

        # feature['id'] = dmi.rel_type.name
        # feature['name'] = dmi.rel_gem_type.name
        # feature['adresse'] = dmi.name
        # feature['telefon_all'] = dmi.adresse

    def setFeaturesFromDmi(self):
        super().setFeaturesFromDmi()

        for kontakt in self.dmi_list:

            feat = QgaFeature(self.layer.fields(), self)

            self.setFeatureAttributes(feat, kontakt)

            # geom_wkt = to_shape(gst_version.geometry).wkt
            # geom_new = QgsGeometry()
            # geom = geom_new.fromWkt(geom_wkt)
            #
            # feat.setGeometry(geom)

            self.layer.provider.addFeatures([feat])

    def setFilterUI(self):
        """
        setze das layout für die filter
        :return:
        """
        # self.bbb = QLabel(self)
        # self.bbb.setText('BBBBBBBBBBBBBB')
        # self.uiMainVlay.addWidget(self.bbb)

        # filter_lay = QHBoxLayout(self)

        """filter typen"""
        self.filter_type_lbl = QLabel(self)
        self.filter_type_lbl.setText('Typ:')
        self.filter_type_lbl.setVisible(False)
        kontakt_type_lbl_font = self.filter_type_lbl.font()
        # kontakt_type_lbl_font.setFamily(config.font_family)
        kontakt_type_lbl_font.setFamily(settings_general.font_family)
        self.filter_type_lbl.setFont(kontakt_type_lbl_font)

        self.filter_type_input_wdg = QComboBox(self)

        self.filter_type_input_wdg.addItem('--- alle Typen ---', -1)

        with session_cm(name='contact type filter') as session:

            contact_type_stmt = select(DmKontaktGemTyp)
            contact_type_list = session.scalars(contact_type_stmt).all()

            for kontact_type in contact_type_list:
                self.filter_type_input_wdg.addItem(kontact_type.name,
                                                   kontact_type.id)

        kontakt_type_input_wdg_font = self.filter_type_input_wdg.font()
        kontakt_type_input_wdg_font.setPointSize(11)
        kontakt_type_input_wdg_font.setFamily(settings_general.font_family)
        self.filter_type_input_wdg.setFont(kontakt_type_input_wdg_font)

        # self.filter_type_input_wdg.currentIndexChanged.connect(self.useFilter)
        self.filter_type_input_wdg.currentTextChanged.connect(
            self.applyFilter)
        """"""

        """filter name"""
        # filter_name = FilterElement(self)
        # filter_name.uiLabelLbl.setText('Name:')
        self.filter_name_lbl = QLabel(self)

        name_lbl_font = self.filter_name_lbl.font()
        name_lbl_font.setFamily(settings_general.font_family)
        self.filter_name_lbl.setFont(name_lbl_font)

        self.filter_name_lbl.setText('Name:')
        self.filter_name_lbl.setVisible(False)

        self.filter_name_input_wdg = QLineEdit(self)

        name_input_wdg_font = self.filter_name_input_wdg.font()
        name_input_wdg_font.setPointSize(11)
        name_input_wdg_font.setFamily(settings_general.font_family)
        self.filter_name_input_wdg.setFont(name_input_wdg_font)

        self.filter_name_input_wdg.setPlaceholderText('Name')
        self.filter_name_input_wdg.setClearButtonEnabled(True)
        self.filter_name_input_wdg.setMaximumWidth(200)
        # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)

        # self.filter_name_input_wdg.textChanged.connect(self.useFilter)
        self.filter_name_input_wdg.textChanged.connect(self.applyFilter)

        # filter_lay.addWidget(filter_name)
        """"""

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

        # spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Minimum,
        #                          QSizePolicy.Minimum)
        # filter_lay.addItem(spacerItem1)

        self.uiFilterItemsHlay.addWidget(self.filter_type_lbl)
        self.uiFilterItemsHlay.addWidget(self.filter_type_input_wdg)
        self.uiFilterItemsHlay.addWidget(self.filter_name_lbl)
        self.uiFilterItemsHlay.addWidget(self.filter_name_input_wdg)
        # filter_lay.addWidget(self.filter_adr_lbl)
        # filter_lay.addWidget(self.filter_adr_input_wdg)

        """"""

        # self.setFilterRemoveBtn()
        # 
        # spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.uiFilterItemsHlay.addItem(spacerItem)

       #  self.uiHeaderHley.insertLayout(1, self.uiFilterItemsHlay)
        # self.uiMainVlay.addLayout(filter_lay)

        # self.uiMainVlay.addWidget(self.filter_type_lbl)
        # print(f'...')
        # self.uiHeaderHley.insertWidget(1, self.filter_type_lbl)
    
        super().setFilterUI()

    def applyFilter(self):

        filter = False

        if self.filter_type_input_wdg.currentData(Qt.UserRole) == -1:
            self.filter_type_lbl.setVisible(False)
        else:
            self.filter_type_lbl.setVisible(True)
            filter = True

        if self.filter_name_input_wdg.text() != '':
            self.filter_name_lbl.setVisible(True)
            filter = True
        else:
            self.filter_name_lbl.setVisible(False)

        """filter remove button"""
        if filter:
            self.uiFilterRemovePbtn.setVisible(True)
        else:
            self.uiFilterRemovePbtn.setVisible(False)
        """"""

        super().applyFilter()

    def removeFilter(self):

        self.filter_name_input_wdg.setText('')
        self.filter_type_input_wdg.setCurrentIndex(0)

    def useFilter(self):

        name_text = self.filter_name_input_wdg.text()
        # adr_text = self.filter_adr_input_wdg.text()
        # kontakt_type_id = self.filter_type_input_wdg.currentData(Qt.UserRole)

        name_expr = f"lower(\"name\") LIKE '%{name_text}%'"
        # adr_expr = f"lower(\"adresse\") LIKE '%{adr_text}%'"
        # kontakt_type_expr = f"(\"typ_id\") = {kontakt_type_id}"

        expr_list = []

        if name_text != '':
            self.filter_name_lbl.setVisible(True)
            expr_list.append(name_expr)
        else:
            self.filter_name_lbl.setVisible(False)

        # if adr_text != '':
        #     self.filter_adr_lbl.setVisible(True)
        #     expr_list.append(adr_expr)
        # else:
        #     self.filter_adr_lbl.setVisible(False)
        #
        # if kontakt_type_id != -1:
        #     self.filter_type_lbl.setVisible(True)
        #     expr_list.append(kontakt_type_expr)
        # else:
        #     self.filter_type_lbl.setVisible(False)

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
        if self.filter_type_input_wdg.currentData(Qt.UserRole) != -1:
            if contact_type != self.filter_type_input_wdg.currentData(Qt.UserRole):
                return False
        """"""

        """filter name"""
        name = self.filter_proxy.sourceModel() \
            .data(self.filter_proxy.sourceModel().index(source_row, 1),
                  Qt.EditRole)
        if self.filter_name_input_wdg.text() != '':
            if name != '' and name is not None:
                if self.filter_name_input_wdg.text().lower() not in name.lower():
                    return False
        """"""

    def getDeleteInfo(self, index=None):
        super().getDeleteInfo(index)

        del_info = self.filter_proxy.data(
            self.filter_proxy.index(
                index.row(), 1))

        return del_info

    # def get_entity_widget_class(self, entity_dmi):
    #
    #     if entity_dmi.rel_type.gemeinschaft:
    #         return Kontakt
    #     else:
    #         return KontaktEinzel

    def getDmiList(self):

        # session = DbSession()

        stmt = (select(DmKontakt)
                .options(
            joinedload(DmKontakt.rel_type)
        )
                .where(DmKontakt.blank_value == 0))

        dmi = self.session.scalars(stmt).all()

        return dmi

    # def getCustomData(self, session):
    #
    #     custom_data = {}
    #
    #     type_stmt = select(BKontaktGemTyp).order_by(BKontaktGemTyp.sort)
    #     type_dmi = session.scalars(type_stmt).all()
    #
    #     custom_data['typ'] = type_dmi
    #
    #     vertr_kontakte_stmt = ((select(BKontakt)
    #                      .options(joinedload(BKontakt.rel_type)))
    #                            .where(BKontaktGemTyp.gemeinschaft == 0))
    #     vertr_kontakte_dmi = session.scalars(vertr_kontakte_stmt).all()
    #
    #     custom_data['vertr_kontakte'] = vertr_kontakte_dmi
    #
    #     return custom_data

    def set_columns(self):

        # self.col_name = KontaktTypeCol('Typ')
        # self.columns.append(self.col_name)
        #
        # self.col_name = KontaktGemTypeCol('Gemeinschafts-Typ')
        # self.columns.append(self.col_name)
        #
        # self.col_name = KontaktNameCol('Name')
        # self.columns.append(self.col_name)
        #
        # self.col_name = KontaktAdresseCol('Adresse')
        # self.columns.append(self.col_name)

        self.columns.append(KontaktTypeCol('Typ'))
        self.columns.append(KontaktGemTypeCol('Gemeinschafts-Typ', False))
        self.columns.append(KontaktNameCol('Name'))
        self.columns.append(KontaktAdresseCol('Adresse'))

        vertreter = KontaktNameCol('Vertreter')
        vertreter.set_dmi_attr('rel_vertreter')
        self.columns.append(vertreter)
