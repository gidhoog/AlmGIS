from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import QLabel, QComboBox, QDialog
from sqlalchemy import select

from core import db_session_cm
from core.data_view import DataView, TableModel, DataViewEntityDialog
from core.entity import EntityDialog
from core.gis_layer import KontaktAllLayer, Feature
from core.main_widget import MainWidget

from core.data_model import BKontakt
from core.scopes.kontakt.kontakt import Kontakt

from qgis.core import QgsField


class KontaktEntityDialog(EntityDialog):

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.dialog_window_title = 'Kontakt'

    def accept(self):
        super().accept()

        if self.dialogWidget.acceptEntity() is not None:

            new_mci = self.dialogWidget.acceptEntity()

            self.parent.updateMaintableNew(self.dialogWidget.purpose, new_mci)

        QDialog.accept(self)

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

        layer = KontaktAllLayer(
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

        mci_id_fld = QgsField("mci_id", QVariant.Int)
        mci_fld = QgsField("mci", QVariant.List)

        nachname_fld = QgsField("nachname", QVariant.String)
        nachname_fld.setAlias('Nachname')

        vorname_fld = QgsField("vorname", QVariant.String)
        vorname_fld.setAlias('Vorname')

        strasse_fld = QgsField("strasse", QVariant.String)
        strasse_fld.setAlias('Straße')

        plz_fld = QgsField("plz", QVariant.Int)
        plz_fld.setAlias('PLZ')

        ort_fld = QgsField("ort", QVariant.String)
        ort_fld.setAlias('Ort')

        telefon1_fld = QgsField("telefon1", QVariant.String)
        telefon1_fld.setAlias('Telefon')

        telefon2_fld = QgsField("telefon2", QVariant.String)
        telefon2_fld.setAlias('Telefon')

        telefon3_fld = QgsField("telefon3", QVariant.String)
        telefon3_fld.setAlias('Telefon')

        mail1_fld = QgsField("mail1", QVariant.String)
        mail1_fld.setAlias('e-Mail')

        mail2_fld = QgsField("mail2", QVariant.String)
        mail2_fld.setAlias('e-Mail')

        mail3_fld = QgsField("mail3", QVariant.String)
        mail3_fld.setAlias('e-Mail')

        self.feature_fields.append(mci_id_fld)
        self.feature_fields.append(mci_fld)
        self.feature_fields.append(nachname_fld)
        self.feature_fields.append(vorname_fld)
        self.feature_fields.append(strasse_fld)
        self.feature_fields.append(plz_fld)
        self.feature_fields.append(ort_fld)
        self.feature_fields.append(telefon1_fld)
        self.feature_fields.append(telefon2_fld)
        self.feature_fields.append(telefon3_fld)
        self.feature_fields.append(mail1_fld)
        self.feature_fields.append(mail2_fld)
        self.feature_fields.append(mail3_fld)

    def setFeatureAttributes(self, feature, mci):
        super().setFeatureAttributes(feature, mci)

        feature['mci_id'] = mci.id
        feature['mci'] = [mci]
        feature['nachname'] = mci.nachname
        feature['vorname'] = mci.vorname
        feature['strasse'] = mci.strasse
        feature['plz'] = mci.plz
        feature['ort'] = mci.ort
        feature['telefon1'] = mci.telefon1
        feature['telefon2'] = mci.telefon2
        feature['telefon3'] = mci.telefon3
        feature['mail1'] = mci.mail1
        feature['mail2'] = mci.mail2
        feature['mail3'] = mci.mail3

    def updateFeatureAttributes(self, *args):
        super().updateFeatureAttributes(args)

        mci = args[0][0]

        # with db_session_cm() as session:
        #
        #     session.add(mci)

        self.setFeatureAttributes(self.current_feature, mci)

    def getFeatureDeleteInfo(self, feature):

        return feature.attribute('nachname')

    def initUi(self):
        super().initUi()

        self.setStretchMethod(2)

    def finalInit(self):
        super().finalInit()

        self.view.setColumnHidden(0, True)

        self.view.sortByColumn(1, Qt.AscendingOrder)

        self.view.resizeColumnsToContents()

    # def setFilterScopeUI(self):
    #     super().setFilterScopeUI()
    #
    #     # filter Name  -----------------------------------------------------
    #     self.guiFiltNameLbl = QLabel("Name beginnt mit:")
    #     self.guiFiltNameCombo = QComboBox(self)
    #     self.uiTableFilterHLay.insertWidget(0, self.guiFiltNameLbl)
    #     self.uiTableFilterHLay.insertWidget(1, self.guiFiltNameCombo)
    #     #  -------------------------------------------------------<<<<<<<<<<

    # def setFilterScope(self):
    #     super().setFilterScope()
    #
    #     self.setFilterNameCombo()

    # def setFilterNameCombo(self):
    #
    #     try:
    #         self.guiFiltNameCombo.currentTextChanged.disconnect(
    #             self.filterMaintable)
    #     except:
    #         pass
    #     finally:
    #         prev_value = self.guiFiltNameCombo.currentText()
    #         self.guiFiltNameCombo.clear()
    #
    #         abc_list = []
    #         for i in range(self.main_table_model.rowCount()):
    #             name_letter = self.main_table_model.data(
    #                 self.main_table_model.index(i, 1), Qt.DisplayRole)[:1]
    #             if name_letter.islower():
    #                 abc_list.append(name_letter.upper()+' ...')
    #             else:
    #                 abc_list.append(name_letter+' ...')
    #
    #         self.guiFiltNameCombo.addItem('- Alle -')
    #
    #         self.guiFiltNameCombo.addItems(
    #             sorted(list(dict.fromkeys(abc_list))))
    #
    #         self.guiFiltNameCombo.setCurrentText(prev_value)
    #
    #         self.guiFiltNameCombo.currentTextChanged.connect(
    #             self.applyFilter)
    #
    # def useFilterScope(self, source_row, source_parent):
    #     super().useFilterScope(source_row, source_parent)
    #
    #     #  filter Name: ---------------------------------------------
    #     try:
    #         table_value = self.filter_proxy.sourceModel() \
    #             .data(self.filter_proxy.sourceModel().index(source_row, 1),
    #         Qt.DisplayRole)
    #         if self.guiFiltNameCombo.currentText() != "- Alle -":
    #             if table_value[:1].islower():
    #                 val = table_value[:1].upper()
    #             else:
    #                 val = table_value[:1]
    #             if val != self.guiFiltNameCombo.currentText()[:1]:
    #                 return False
    #     except:
    #         pass
    #     #  ----------------------------------------------------##############

    # def updateMainWidget(self):
    #
    #     self.updateMaintable()

    def getDeleteInfo(self, index=None):
        super().getDeleteInfo(index)

        del_info = self.filter_proxy.data(
            self.filter_proxy.index(
                index.row(), 1))

        return del_info

    def getMciList(self, session):

        stmt = select(
            BKontakt).where(BKontakt.blank_value == 0)

        mci = session.scalars(stmt).all()

        return mci
