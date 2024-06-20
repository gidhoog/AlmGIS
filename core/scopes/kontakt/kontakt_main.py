from PyQt5.QtCore import Qt, QVariant
from qgis.PyQt.QtWidgets import (QLabel, QComboBox, QDialog, QLineEdit,
                                 QSpacerItem, QSizePolicy, QHBoxLayout)
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core import db_session_cm, config
from core.data_view import DataView, TableModel, DataViewEntityDialog
from core.entity import EntityDialog
from core.gis_layer import ZVectorLayer, Feature
from core.main_widget import MainWidget

from core.data_model import BKontakt, BKontaktTyp
from core.scopes.kontakt.kontakt import Kontakt

from qgis.core import QgsField


class KontaktEntityDialog(EntityDialog):

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.dialog_window_title = 'Kontakt'

    def accept(self):
        super().accept()

        if self.accepted_mci is not False:

            self.parent.updateMaintableNew(self.dialogWidget.purpose,
                                           self.accepted_mci)
            QDialog.accept(self)

        # self.dialogWidget.removeEntity()

        # if self.dialogWidget.acceptEntity() is not None:
        #
        #     new_mci = self.dialogWidget.acceptEntity()
        #
        #     self.parent.updateMaintableNew(self.dialogWidget.purpose, new_mci)
        #
        # QDialog.accept(self)

class KontaktMainWidget(MainWidget):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.uiTitleLbl.setText('alle Kontakte')

        self.kontakt_table = KontaktMain()

    def initMainWidget(self):
        super().initMainWidget()

        self.uiMainVLay.addWidget(self.kontakt_table)
        # self.kontakt_table.loadData()
        # self.kontakt_table.initDataView()


# class ContactModel(TableModel):
#
#     header = [
#         'Name',
#         'Straße',
#         'PLZ',
#         'Ort',
#         'Festnetz',
#         'Mobil'
#     ]
#
#     def data(self, index, role=None):
#
#         row = index.row()
#         # col = index.column()
#
#         # if role == Qt.TextAlignmentRole:
#         #
#         #     if index.column() in [5, 6]:
#         #
#         #         return Qt.AlignRight | Qt.AlignVCenter
#         #
#         #     if index.column() in [1, 2, 4]:
#         #
#         #         return Qt.AlignHCenter | Qt.AlignVCenter
#
#         if index.column() == 0:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].shown_name
#                 # return self.mci_list[row][0]
#
#         if index.column() == 1:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].street
#
#         if index.column() == 2:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].postcode
#                 # return self.mci_list[row][1]
#
#         if index.column() == 3:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].town
#
#         if index.column() == 4:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].phone
#
#         if index.column() == 5:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].mobile


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
        self.entity_widget_class = Kontakt

        self._entity_mc = BKontakt
        """"""

        self.setFeatureFields()
        self.setFilterUI()

        self._gis_layer = self.setLayer()

        self.loadData()

        self.addFeaturesFromMciList(self._mci_list)
        self.setTableView()

        self.initUi()

        self.finalInit()

        self.updateFooter()

        self.signals()

    def setLayer(self):

        layer = ZVectorLayer(
            "None",
            "KontaktAllLay",
            "memory",
            feature_fields=self.feature_fields
        )
        return layer

    # def addFeaturesFromMciList(self):
    #     super().addFeaturesFromMciList()
    #
    #     for contact in self._mci_list:
    #
    #         feat = Feature(self._gis_layer.fields(), self)
    #
    #         self.setFeatureAttributes(feat, contact)
    #
    #         self._gis_layer.data_provider.addFeatures([feat])

    def setFeatureFields(self):
        super().setFeatureFields()

        mci_id_fld = QgsField("id", QVariant.Int)

        typ_id_fld = QgsField("typ_id", QVariant.String)

        typ_name_fld = QgsField("typ_name", QVariant.String)
        typ_name_fld.setAlias('Typ')

        typ_color_fld = QgsField("typ_color", QVariant.String)

        name_fld = QgsField("name", QVariant.String)
        name_fld.setAlias('Name')

        adresse_fld = QgsField("adresse", QVariant.String)
        adresse_fld.setAlias('Adresse')

        telefon_fld = QgsField("telefon", QVariant.String)
        telefon_fld.setAlias('Telefon')

        mail_fld = QgsField("mail", QVariant.String)
        mail_fld.setAlias('e-Mail')

        self.feature_fields.append(mci_id_fld)
        self.feature_fields.append(typ_id_fld)
        self.feature_fields.append(typ_name_fld)
        self.feature_fields.append(typ_color_fld)
        self.feature_fields.append(name_fld)
        self.feature_fields.append(adresse_fld)
        self.feature_fields.append(telefon_fld)
        self.feature_fields.append(mail_fld)

    def changeAttributes(self, feature, mci):

        attrib = {0: mci.id,
                  1: mci.type_id,
                  2: mci.rel_type.name,
                  3: mci.rel_type.color,
                  4: mci.name,
                  5: mci.adresse,
                  6: mci.telefon_all,
                  7: mci.mail_all
                  }

        self._gis_layer.changeAttributeValues(feature.id(),
                                              attrib)

    def setFeatureAttributes(self, feature, mci):
        super().setFeatureAttributes(feature, mci)

        feature['id'] = mci.id
        feature['typ_id'] = mci.type_id
        feature['typ_name'] = mci.rel_type.name
        feature['typ_color'] = mci.rel_type.color
        feature['name'] = mci.name
        feature['adresse'] = mci.adresse
        feature['telefon'] = mci.telefon_all
        feature['mail'] = mci.mail_all

    def updateFeatureAttributes(self, *args):
        super().updateFeatureAttributes(args)

        mci = args[0][0]

        with db_session_cm() as session:

            session.add(mci)

            self.setFeatureAttributes(self.current_feature, mci)

    def getFeatureDeleteInfo(self, feature):

        return feature.attribute('name')

    def initUi(self):
        super().initUi()

        self.setStretchMethod(2)

    def finalInit(self):
        super().finalInit()

        self.view.setColumnHidden(0, True)
        self.view.setColumnHidden(1, True)
        self.view.setColumnHidden(3, True)

        self.view.sortByColumn(2, Qt.AscendingOrder)

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

        self.filter_type_input_wdg = QComboBox(self)
        """"""

        """filter name"""
        # filter_name = FilterElement(self)
        # filter_name.uiLabelLbl.setText('Name:')
        self.filter_name_lbl = QLabel(self)

        name_lbl_font = self.filter_name_lbl.font()
        name_lbl_font.setFamily(config.font_family)
        self.filter_name_lbl.setFont(name_lbl_font)

        self.filter_name_lbl.setText('Name:')
        self.filter_name_lbl.setVisible(False)

        self.filter_name_input_wdg = QLineEdit(self)

        name_input_wdg_font = self.filter_name_input_wdg.font()
        name_input_wdg_font.setPointSize(11)
        name_input_wdg_font.setFamily(config.font_family)
        self.filter_name_input_wdg.setFont(name_input_wdg_font)

        self.filter_name_input_wdg.setPlaceholderText('Name')
        self.filter_name_input_wdg.setClearButtonEnabled(True)
        self.filter_name_input_wdg.setMaximumWidth(200)
        # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)

        self.filter_name_input_wdg.textChanged.connect(self.useFilter)

        # filter_lay.addWidget(filter_name)
        """"""

        """filter adresse"""
        # filter_az = FilterElement(self)
        # filter_az.uiLabelLbl.setText('AZ:')

        self.filter_adr_lbl = QLabel(self)

        adr_lbl_font = self.filter_adr_lbl.font()
        adr_lbl_font.setFamily(config.font_family)
        self.filter_adr_lbl.setFont(adr_lbl_font)

        self.filter_adr_lbl.setText('Adresse:')
        self.filter_adr_lbl.setVisible(False)

        self.filter_adr_input_wdg = QLineEdit(self)
        self.filter_adr_input_wdg.setPlaceholderText('Adresse')
        adr_input_wdg_font = self.filter_adr_input_wdg.font()
        adr_input_wdg_font.setPointSize(11)
        adr_input_wdg_font.setFamily(config.font_family)
        self.filter_adr_input_wdg.setFont(adr_input_wdg_font)
        self.filter_adr_input_wdg.setClearButtonEnabled(True)
        self.filter_adr_input_wdg.setMaximumWidth(80)
        # filter_az.uiFilterElementLay.insertWidget(1, self.filter_adr_input_wdg)

        self.filter_adr_input_wdg.textChanged.connect(self.useFilter)

        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Minimum,
                                 QSizePolicy.Minimum)
        filter_lay.addItem(spacerItem1)

        filter_lay.addWidget(self.filter_type_lbl)
        filter_lay.addWidget(self.filter_type_input_wdg)
        filter_lay.addWidget(self.filter_name_lbl)
        filter_lay.addWidget(self.filter_name_input_wdg)
        filter_lay.addWidget(self.filter_adr_lbl)
        filter_lay.addWidget(self.filter_adr_input_wdg)

        """"""

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        filter_lay.addItem(spacerItem)

        self.uiHeaderHley.insertLayout(1, filter_lay)

    def useFilter(self):

        name_text = self.filter_name_input_wdg.text()
        adr_text = self.filter_adr_input_wdg.text()

        name_expr = f"lower(\"name\") LIKE '%{name_text}%'"
        adr_expr = f"lower(\"adresse\") LIKE '%{adr_text}%'"

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

        if expr_list == []:
            self._gis_layer.setSubsetString('')
        else:

            expr_string = " and ".join(expr for expr in expr_list)
            print(f'expression string: {expr_string}')
            self._gis_layer.setSubsetString(expr_string)

        self.updateFooter()

    def getDeleteInfo(self, index=None):
        super().getDeleteInfo(index)

        del_info = self.filter_proxy.data(
            self.filter_proxy.index(
                index.row(), 1))

        return del_info

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
