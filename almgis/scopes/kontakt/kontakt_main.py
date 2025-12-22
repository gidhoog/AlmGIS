import weakref

from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QColor
from qga.core.fields import QgaField
from qga.core.main_wdg import QgaMainWdg
from qga.gui.data_view_gui import QgaDataViewGui
from qgis.PyQt.QtCore import QVariant
from qgis._gui import QgsAttributeTableView
from sqlalchemy import select, URL

from almgis.core.data_view import AlmDataView, AlmTableModel
from almgis.core.entity import AlmEntityDialog
from almgis.core.fields import GeneralField
from almgis.database.models import DmKontakt, DmKontaktType


class KontaktEntityDialog(AlmEntityDialog):

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent
        # self.ui.setWindowTitle(self.ui.windowTitle() + ' - Kontakt')


class KontaktTableModel(AlmTableModel):

    def __init__(self, layerCache=None,
                     columns=None, parent=None):
            super().__init__(layerCache, columns, parent)

    def data(self, index: QModelIndex, role: int = ...):

        # print(f'////////////////////////////////////////////////////')

        # if role == Qt.TextAlignmentRole:
        #     # Set alignment for the "Age" column (column index 1)
        #     if index.column() == 1:
        #         return Qt.AlignHCenter | Qt.AlignVCenter

        if index.column() == 1:

            if role == Qt.BackgroundRole:

                return QColor(200, 100, 120)

        return super().data(index, role)


class KontaktMain(AlmDataView):
    """
    class for kontakts
    """

    """weak container to store all live instances of the class"""
    _instances = weakref.WeakSet()
    """"""

    _dmi_dict = {}
    _type_dmc = DmKontaktType

    _entity_dialog_class = KontaktEntityDialog

    _entity_amount_text = ["Kontakt", "Kontakte", "kein Kontakt"]
    _delete_window_title = ["Kontakt löschen", "Kontakte löschen"]
    _delete_window_text_single = "Soll der ausgewählte Kontakt " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Kontakte wirklich gelöscht werden?"]
    _delete_text = ["Der Kontakt", "kann nicht gelöscht werden, da er "
                    "verwendet wird!"]

    def __init__(self, parent=None, gis_mode=False):
        super(__class__, self).__init__(gis_mode)

        # self._instances.add(self)

        # self.dmi_dict = KontaktMain._dmi_dict
        self.dmi_dict = self._dmi_dict
        self.edit_entity_by = 'dmi'

        self._entity_dmc = DmKontakt

        self.model_cls = KontaktTableModel

        print(f'_instances add: {self._instances}')
        # self.setupWdgGui()

    def initUi(self):
        super().initUi()

        self.ui.titleLbl.setText(f'eine Liste mit allen Kontakten'
                                 f' {str(self.inst_number)}')

    # def onDelete(self):
    #
    #     print(f'.....onDelete KontaktMain')
    #     self._instances.remove(self)
    #     print(f'_instances remove: {self._instances}')

    # def addEntity(self):
    #
    #     print(f'add new kontakt!')
    #     new = DmKontakt()
    #     new.nachname = 'new1'
    #
    #     self.session.add(new)
    #     self.session.commit()
    #     self.session.close()

    # def getDefaultDmi(self):
    #
    #     dmi = self._entity_dmc()
    #
    #     dmi.nachname = 'AA'
    #     dmi.vorname = 'aa'
    #
    #     return dmi

    def getDmiList(self):

        url_object = URL.create(
            "sqlite",
            database="appdb.db",
        )

        stmt = select(self._entity_dmc).where(DmKontakt.blank_value == 0)
        dmi = self.session.scalars(stmt).all()

        return dmi

    def createFeatureFields(self):

        # k_uuid = GeneralField.Uuid()
        k_id = GeneralField.Id()
        k_type_id = GeneralField.TypeId()
        k_name = Fields.Name()
        k_adresse = Fields.Adresse()
        k_telefon_all = Fields.TelefonAll()
        k_vertreter_id = Fields.VertreterId()

        # self._fields.append(k_uuid)
        self._fields.append(k_id)
        self._fields.append(k_type_id)
        self._fields.append(k_name)
        self._fields.append(k_adresse)
        self._fields.append(k_telefon_all)
        self._fields.append(k_vertreter_id)

#     def deleteCheck(self, dmi):
#
#         with session_cm() as session:
#             all_vertreter_ids_stmt = select(DmKontakt.vertreter_id)
#             all_vertreter_ids = session.scalars(all_vertreter_ids_stmt).all()
#
#             bewirtschafter_ids_stmt = select(DmAkt.bewirtschafter_id)
#             bewirtschafter_ids = session.scalars(bewirtschafter_ids_stmt).all()
#
#         if dmi.id in all_vertreter_ids or dmi.id in bewirtschafter_ids:
#             print(f'====> dmi in use: {dmi}')
#             return False
#         else:
#             return True
#
#     def signals(self):
#         super().signals()
#
#     def initUi(self):
#         super().initUi()
#
#         self.setStretchMethod(2)
#
#         # """auswahl in der 'add-toolbox' um aus einzel- und gemeinschafts-
#         # kontakt wählen zu können"""
#
#         # self.add_menu = QMenu(self)
#
#         # self.action_einzel = QAction(self.uiAddDataTbtn)
#         # self.action_einzel.setText('Einzelperson')
#         # self.action_einzel.setIcon(QIcon(":/svg/icons/person.svg"))
#         # self.uiAddDataTbtn.addAction(self.action_einzel)
#         #
#         # self.action_gemeinschaft = QAction(self.uiAddDataTbtn)
#         # self.action_gemeinschaft.setText('Gemeinschaft')
#         # self.action_gemeinschaft.setIcon(QIcon(":/svg/icons/group.svg"))
#         # self.uiAddDataTbtn.addAction(self.action_gemeinschaft)
#         #
#         # self.action_einzel.triggered.connect(self.addEinzelKontakt)
#         # # self.action_einzel..connect(lambda x: self.fn(x))
#         # self.action_gemeinschaft.triggered.connect(self.addGemKontakt)
#         #
#         # # self.add_menu.addAction(self.action_einzel)
#         # # self.add_menu.addAction(action_gemeinschaft)
#         #
#         # """"""
#         #
#         # # self.uiAddDataTbtn.setMenu(self.add_menu)
#         # self.uiAddDataTbtn.setPopupMode(QToolButton.InstantPopup)
#
#     # # @pyqtSlot()
#     # @staticmethod
#     # def fn(checked):
#     #
#     #     print(f'ff: {checked}')
#     #     # self.addKontakt('einzel')
#
#     def addEinzelKontakt(self):
#
#         print(f'...')
#
#         entity_widget = KontaktEinzel(self)
#         self.addEntity(entity_wdg=entity_widget)
#         # self.openNewKontakt(entity_widget)
#
#     def addGemKontakt(self):
#
#         print(f'...')
#
#         entity_widget = Kontakt(self)
#         self.addEntity(entity_wdg=entity_widget)
#
#         # self.openNewKontakt(entity_widget)
#
#     # def openNewKontakt(self, entity_widget):
#     #
#     #     # entity_widget.initEntityWidget()
#     #     entity_widget.setupCodeUi()
#     #
#     #     dmi = BKontakt()
#     #
#     #     entity_widget.purpose = 'add'
#     #
#     #     self.edit_entity = dmi
#     #     self.session.add(dmi)
#     #
#     #     self.editRow(entity_widget=entity_widget,
#     #                  entity_dmi=dmi)
#
#     # def addKontakt(self, type='einzel'):
#     #
#     #     print(f'...')
#     #
#     #     if type == 'einzel':
#     #         entity_widget = KontaktEinzel(self)
#     #     elif type == 'gem':
#     #         entity_widget = Kontakt(self)
#     #
#     #     entity_widget.initEntityWidget()
#     #
#     #     dmi = BKontakt()
#     #
#     #     entity_widget.purpose = 'add'
#     #
#     #     self.edit_entity = dmi
#     #     self.dataview_session.add(dmi)
#     #
#     #     self.editRow(entity_widget=entity_widget,
#     #                  entity_dmi=dmi)
#
#     def finalInit(self):
#         super().finalInit()
#
#         # self.view.setColumnHidden(0, True)
#         # self.view.setColumnHidden(1, True)
#         # self.view.setColumnHidden(3, True)
#
#         """füge den button erst nach dem einfügen der filter ein!!!"""
#         self.uiInfoBtnFilter = AlmInfoButton(self)
#         self.uiInfoBtnFilter.setObjectName('FilterBtn')
#         self.uiFilterItemsHlay.insertWidget(self.uiFilterItemsHlay.count(),
#                                             self.uiInfoBtnFilter)
#         """"""
#
#         self.view.sortByColumn(1, Qt.AscendingOrder)
#
#         self.view.resizeColumnsToContents()
#
#         new_contact = DmKontaktEinzel()
#         # new_contact.id = 999
#         new_contact.vorname = 'aaa1'
#         new_contact.nachname = 'AAA'
#         # new_contact.type_id = 1
#         # new_contact.vertreter_id = 0
#
#         self.session.add(new_contact)
#         self.session.commit()
#
#         print(f'...')
#
#     def getFeatureFields(self):
#
#         k_id = GeneralField.Id()
#         k_name = KontaktField.Name()
#         k_adresse = KontaktField.Adresse()
#         k_telefon_all = KontaktField.TelefonAll()
#
#         # type_fld = QgaField("type", QVariant.String)
#         # gem_type_fld = QgaField("gem_type", QVariant.String)
#         # name_fld = QgaField("name", QVariant.String)
#         # adresse_fld = QgaField("adresse", QVariant.String)
#
#         self.fields.append(k_id)
#         self.fields.append(k_name)
#         self.fields.append(k_adresse)
#         self.fields.append(k_telefon_all)
#
#         return self.fields
#
#     # def setFeatureFields(self):
#     #
#     #     type_fld = QgaField("type", QVariant.String)
#     #     gem_type_fld = QgaField("gem_type", QVariant.String)
#     #     name_fld = QgaField("name", QVariant.String)
#     #     adresse_fld = QgaField("adresse", QVariant.String)
#     #
#     #     self.fields.append(type_fld,
#     #                        gem_type_fld,
#     #                        name_fld,
#     #                        adresse_fld
#     #                        )
#
#     def setFeatureAttributes(self, feature, dmi):
#
#         # feature['type'] = dmi.rel_type.name
#         # feature['gem_type'] = dmi.rel_gem_type.name
#         # feature['name'] = dmi.name
#         # feature['adresse'] = dmi.adresse
#
#         for field in self.fields:
#
#             # feature[field.name()] = field.fieldValue(dmi)
#             feature[field.name()] = field.getFieldValue(dmi)
#
#         # feature['id'] = dmi.rel_type.name
#         # feature['name'] = dmi.rel_gem_type.name
#         # feature['adresse'] = dmi.name
#         # feature['telefon_all'] = dmi.adresse
#
#     def setFeaturesFromDmi(self):
#         super().setFeaturesFromDmi()
#
#         for kontakt in self.dmi_list:
#
#             feat = QgaFeature(self.layer.fields(), self)
#
#             feat.dmi = kontakt
#
#             self.setFeatureAttributes(feat, kontakt)
#
#             # geom_wkt = to_shape(gst_version.geometry).wkt
#             # geom_new = QgsGeometry()
#             # geom = geom_new.fromWkt(geom_wkt)
#             #
#             # feat.setGeometry(geom)
#
#             self.layer.provider.addFeatures([feat])
#
#     def setFilterUI(self):
#         """
#         setze das layout für die filter
#         :return:
#         """
#         # self.bbb = QLabel(self)
#         # self.bbb.setText('BBBBBBBBBBBBBB')
#         # self.uiMainVlay.addWidget(self.bbb)
#
#         # filter_lay = QHBoxLayout(self)
#
#         """filter typen"""
#         self.filter_type_lbl = QLabel(self)
#         self.filter_type_lbl.setText('Typ:')
#         self.filter_type_lbl.setVisible(False)
#         kontakt_type_lbl_font = self.filter_type_lbl.font()
#         # kontakt_type_lbl_font.setFamily(config.font_family)
#         kontakt_type_lbl_font.setFamily(settings_general.font_family)
#         self.filter_type_lbl.setFont(kontakt_type_lbl_font)
#
#         self.filter_type_input_wdg = QComboBox(self)
#
#         self.filter_type_input_wdg.addItem('--- alle Typen ---', -1)
#
#         with session_cm(name='contact type filter') as session:
#
#             contact_type_stmt = select(DmKontaktGemTyp)
#             contact_type_list = session.scalars(contact_type_stmt).all()
#
#             for kontact_type in contact_type_list:
#                 self.filter_type_input_wdg.addItem(kontact_type.name,
#                                                    kontact_type.id)
#
#         kontakt_type_input_wdg_font = self.filter_type_input_wdg.font()
#         kontakt_type_input_wdg_font.setPointSize(11)
#         kontakt_type_input_wdg_font.setFamily(settings_general.font_family)
#         self.filter_type_input_wdg.setFont(kontakt_type_input_wdg_font)
#
#         # self.filter_type_input_wdg.currentIndexChanged.connect(self.useFilter)
#         self.filter_type_input_wdg.currentTextChanged.connect(
#             self.applyFilter)
#         """"""
#
#         """filter name"""
#         # filter_name = FilterElement(self)
#         # filter_name.uiLabelLbl.setText('Name:')
#         self.filter_name_lbl = QLabel(self)
#
#         name_lbl_font = self.filter_name_lbl.font()
#         name_lbl_font.setFamily(settings_general.font_family)
#         self.filter_name_lbl.setFont(name_lbl_font)
#
#         self.filter_name_lbl.setText('Name:')
#         self.filter_name_lbl.setVisible(False)
#
#         self.filter_name_input_wdg = QLineEdit(self)
#
#         name_input_wdg_font = self.filter_name_input_wdg.font()
#         name_input_wdg_font.setPointSize(11)
#         name_input_wdg_font.setFamily(settings_general.font_family)
#         self.filter_name_input_wdg.setFont(name_input_wdg_font)
#
#         self.filter_name_input_wdg.setPlaceholderText('Name')
#         self.filter_name_input_wdg.setClearButtonEnabled(True)
#         self.filter_name_input_wdg.setMaximumWidth(200)
#         # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)
#
#         # self.filter_name_input_wdg.textChanged.connect(self.useFilter)
#         self.filter_name_input_wdg.textChanged.connect(self.applyFilter)
#
#         # filter_lay.addWidget(filter_name)
#         """"""
#
#         # """filter adresse"""
#         # # filter_az = FilterElement(self)
#         # # filter_az.uiLabelLbl.setText('AZ:')
#         #
#         # self.filter_adr_lbl = QLabel(self)
#         #
#         # adr_lbl_font = self.filter_adr_lbl.font()
#         # adr_lbl_font.setFamily(config.font_family)
#         # self.filter_adr_lbl.setFont(adr_lbl_font)
#         #
#         # self.filter_adr_lbl.setText('Adresse:')
#         # self.filter_adr_lbl.setVisible(False)
#         #
#         # self.filter_adr_input_wdg = QLineEdit(self)
#         # self.filter_adr_input_wdg.setPlaceholderText('Adresse')
#         # adr_input_wdg_font = self.filter_adr_input_wdg.font()
#         # adr_input_wdg_font.setPointSize(11)
#         # adr_input_wdg_font.setFamily(config.font_family)
#         # self.filter_adr_input_wdg.setFont(adr_input_wdg_font)
#         # self.filter_adr_input_wdg.setClearButtonEnabled(True)
#         # self.filter_adr_input_wdg.setMaximumWidth(80)
#         # # filter_az.uiFilterElementLay.insertWidget(1, self.filter_adr_input_wdg)
#         #
#         # self.filter_adr_input_wdg.textChanged.connect(self.useFilter)
#
#         # spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Minimum,
#         #                          QSizePolicy.Minimum)
#         # filter_lay.addItem(spacerItem1)
#
#         self.uiFilterItemsHlay.addWidget(self.filter_type_lbl)
#         self.uiFilterItemsHlay.addWidget(self.filter_type_input_wdg)
#         self.uiFilterItemsHlay.addWidget(self.filter_name_lbl)
#         self.uiFilterItemsHlay.addWidget(self.filter_name_input_wdg)
#         # filter_lay.addWidget(self.filter_adr_lbl)
#         # filter_lay.addWidget(self.filter_adr_input_wdg)
#
#         """"""
#
#         # self.setFilterRemoveBtn()
#         #
#         # spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
#         # self.uiFilterItemsHlay.addItem(spacerItem)
#
#        #  self.uiHeaderHley.insertLayout(1, self.uiFilterItemsHlay)
#         # self.uiMainVlay.addLayout(filter_lay)
#
#         # self.uiMainVlay.addWidget(self.filter_type_lbl)
#         # print(f'...')
#         # self.uiHeaderHley.insertWidget(1, self.filter_type_lbl)
#
#         super().setFilterUI()
#
#     def applyFilter(self):
#
#         filter = False
#
#         if self.filter_type_input_wdg.currentData(Qt.UserRole) == -1:
#             self.filter_type_lbl.setVisible(False)
#         else:
#             self.filter_type_lbl.setVisible(True)
#             filter = True
#
#         if self.filter_name_input_wdg.text() != '':
#             self.filter_name_lbl.setVisible(True)
#             filter = True
#         else:
#             self.filter_name_lbl.setVisible(False)
#
#         """filter remove button"""
#         if filter:
#             self.uiFilterRemovePbtn.setVisible(True)
#         else:
#             self.uiFilterRemovePbtn.setVisible(False)
#         """"""
#
#         super().applyFilter()
#
#     def removeFilter(self):
#
#         self.filter_name_input_wdg.setText('')
#         self.filter_type_input_wdg.setCurrentIndex(0)
#
#     def useFilter(self):
#
#         name_text = self.filter_name_input_wdg.text()
#         # adr_text = self.filter_adr_input_wdg.text()
#         # kontakt_type_id = self.filter_type_input_wdg.currentData(Qt.UserRole)
#
#         name_expr = f"lower(\"name\") LIKE '%{name_text}%'"
#         # adr_expr = f"lower(\"adresse\") LIKE '%{adr_text}%'"
#         # kontakt_type_expr = f"(\"typ_id\") = {kontakt_type_id}"
#
#         expr_list = []
#
#         if name_text != '':
#             self.filter_name_lbl.setVisible(True)
#             expr_list.append(name_expr)
#         else:
#             self.filter_name_lbl.setVisible(False)
#
#         # if adr_text != '':
#         #     self.filter_adr_lbl.setVisible(True)
#         #     expr_list.append(adr_expr)
#         # else:
#         #     self.filter_adr_lbl.setVisible(False)
#         #
#         # if kontakt_type_id != -1:
#         #     self.filter_type_lbl.setVisible(True)
#         #     expr_list.append(kontakt_type_expr)
#         # else:
#         #     self.filter_type_lbl.setVisible(False)
#
#         if expr_list == []:
#             self._gis_layer.setSubsetString('')
#         else:
#
#             expr_string = " and ".join(expr for expr in expr_list)
#             self._gis_layer.setSubsetString(expr_string)
#
#             print(f'expression string: {expr_string}')
#
#         print(f'expr_list: {expr_list}')
#
#         self.updateFooter()
#
#     def useFilterScope(self, source_row, source_parent):
#         super().useFilterScope(source_row, source_parent)
#
#         """filter contact_typ"""
#         contact_type = self.filter_proxy.sourceModel() \
#             .data(self.filter_proxy.sourceModel().index(source_row, 0),
#                   Qt.EditRole)
#         if self.filter_type_input_wdg.currentData(Qt.UserRole) != -1:
#             if contact_type != self.filter_type_input_wdg.currentData(Qt.UserRole):
#                 return False
#         """"""
#
#         """filter name"""
#         name = self.filter_proxy.sourceModel() \
#             .data(self.filter_proxy.sourceModel().index(source_row, 1),
#                   Qt.EditRole)
#         if self.filter_name_input_wdg.text() != '':
#             if name != '' and name is not None:
#                 if self.filter_name_input_wdg.text().lower() not in name.lower():
#                     return False
#         """"""
#
#     def getDeleteInfo(self, index=None):
#         super().getDeleteInfo(index)
#
#         del_info = self.filter_proxy.data(
#             self.filter_proxy.index(
#                 index.row(), 1))
#
#         return del_info
#
#     # def get_entity_widget_class(self, entity_dmi):
#     #
#     #     if entity_dmi.rel_type.gemeinschaft:
#     #         return Kontakt
#     #     else:
#     #         return KontaktEinzel
#
#     def getDmiList(self):
#
#         # session = DbSession()
#
#         stmt = (select(DmKontakt)
#                 .options(
#             joinedload(DmKontakt.rel_type)
#         )
#                 .where(DmKontakt.blank_value == 0))
#
#         dmi = self.session.scalars(stmt).all()
#
#         return dmi
#
#     # def getCustomData(self, session):
#     #
#     #     custom_data = {}
#     #
#     #     type_stmt = select(BKontaktGemTyp).order_by(BKontaktGemTyp.sort)
#     #     type_dmi = session.scalars(type_stmt).all()
#     #
#     #     custom_data['typ'] = type_dmi
#     #
#     #     vertr_kontakte_stmt = ((select(BKontakt)
#     #                      .options(joinedload(BKontakt.rel_type)))
#     #                            .where(BKontaktGemTyp.gemeinschaft == 0))
#     #     vertr_kontakte_dmi = session.scalars(vertr_kontakte_stmt).all()
#     #
#     #     custom_data['vertr_kontakte'] = vertr_kontakte_dmi
#     #
#     #     return custom_data
#
#     def set_columns(self):
#
#         # self.col_name = KontaktTypeCol('Typ')
#         # self.columns.append(self.col_name)
#         #
#         # self.col_name = KontaktGemTypeCol('Gemeinschafts-Typ')
#         # self.columns.append(self.col_name)
#         #
#         # self.col_name = KontaktNameCol('Name')
#         # self.columns.append(self.col_name)
#         #
#         # self.col_name = KontaktAdresseCol('Adresse')
#         # self.columns.append(self.col_name)
#
#         self.columns.append(KontaktTypeCol('Typ'))
#         self.columns.append(KontaktGemTypeCol('Gemeinschafts-Typ', False))
#         self.columns.append(KontaktNameCol('Name'))
#         self.columns.append(KontaktAdresseCol('Adresse'))
#
#         vertreter = KontaktNameCol('Vertreter')
#         vertreter.set_dmi_attr('rel_vertreter')
#         self.columns.append(vertreter)


class KontaktMainWdg(QgaMainWdg):

    content_wdg_cls = KontaktMain

    def __init__(self, parent=None):
        super().__init__(parent)

        self.content_wdg = self.content_wdg_cls(self)
        # self.ui.uiContentVlay.addWidget(self.main_wdg.ui)

        self.content_wdg.updateDataViewSgn.connect(self.updateMainWdg)
        self.parent.updateAppSgn.connect(self.content_wdg.updateDataView)

        # self.setupWdgGui()
        # self.initUi()

    def initUi(self):
        super().initUi()

        # self.content_wdg.initUi()
        self.ui.setTitle(self.title + '+/+1')

    def loadData(self):
        self.content_wdg.loadData()

    # def setupWdg(self):
    #     super().setupWdg()

    # self.content_wdg.setupWdg()

    # def finalizeMainWidget(self):
    # def setupWdgGui(self):
    #     super().setupWdgGui()
    #
    #     self.main_wdg.initUi()
    #     self.ui.setTitle('alle Kontakte 11')
    #
    #     # vvv = QgsAttributeTableView()
    #     # self.main_wdg.ui.tableVlay.addWidget(vvv)
    #
    #     # self.main_wdg.finalSetupDataView()
    #     self.ui.mainVlay.addWidget(self.main_wdg.ui)
    #
    #     # self.main_wdg.updateDataViewSgn.connect(self.updateMainWdg)
    #     # self.parent.updateAppSgn.connect(self.main_wdg.updateDataView)


class Fields:
    """
    represent the fields according to the data_model 'Kontakt'
    """

    class VertreterId(QgaField):

        def __init__(self):
            super().__init__()

            self.name = 'vertreter_name'
            self.type = QVariant.String

            self.dmi_attr = 'rel_vertreter.name'
            self.alias = 'Vertreter Name'

            self.visible = False

    class Name(QgaField):

        def __init__(self):
            super().__init__()

            self.name = 'name'
            self.type = QVariant.String

            self.alias = 'Name'
            self.dmi_attr = 'name'

    class Adresse(QgaField):

        def __init__(self):
            super().__init__()

            self.name = 'adresse'
            self.type = QVariant.String

            self.alias = 'Adresse'
            self.dmi_attr = 'adresse'

    class Strasse(QgaField):

        def __init__(self):
            super().__init__()

            self.name = 'strasse'
            self.type = QVariant.String

            self.alias = 'Straße'
            self.dmi_attr = 'strasse'

    class TelefonAll(QgaField):

        def __init__(self):
            super().__init__()

            self.name = 'telefon_all'
            self.type = QVariant.String

            self.alias = 'Telefonnummern'
            self.dmi_attr = 'telefon_all'
