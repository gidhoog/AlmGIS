from qgis.PyQt.QtCore import Qt, QModelIndex, QAbstractTableModel
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import (QHeaderView, QPushButton, QDialog,
                                 QAbstractItemView, QSpacerItem, QLineEdit,
                                 QLabel, QHBoxLayout, QSizePolicy)

from geoalchemy2.shape import to_shape
from qgis.core import QgsFeature, QgsGeometry, QgsVectorLayerCache, QgsVectorLayer, QgsField, QgsPointXY
from qgis.PyQt.QtCore import QVariant

from qgis.gui import QgsAttributeTableModel, QgsAttributeTableView, QgsAttributeTableFilterModel

from geoalchemy2.shape import to_shape

from sqlalchemy import func

from core import config
from core.data_model import BGstZuordnung, BGst, BGstEz, \
    BGstVersion, BKatGem, BGstAwbStatus, BRechtsgrundlage, BCutKoppelGstAktuell, \
    BKomplex, BAkt, BKoppel, BAbgrenzung
from core.entity import EntityDialog
from core.gis_item import GisItem
from core.gis_layer import setLayerStyle, GstZuordLayer, Feature
from core.gis_tools import cut_koppel_gstversion
from core.main_dialog import MainDialog
from core.data_view import DataView, TableModel, TableView, GisTableView, \
    GisTableModel
import typing

from operator import attrgetter

from core.scopes.gst.gst_zuordnung import GstZuordnung
from core.scopes.gst.gst_zuordnung_dataform import GstZuordnungDataForm


class GstDialog(EntityDialog):
    """
    dialog für die anzeige einer grundstückszuordnung
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        # self.parent = parent
        #
        # self.enableApply = True

        self.dialog_window_title = 'Grundstückszuordnung'
        # self.set_apply_button_text('&Speichern und Schließen')


    def accept(self):
        super().accept()

        if self.dialogWidget.acceptEntity() is not None:

            new_mci = self.dialogWidget.acceptEntity()

            self.parent.updateMaintableNew(self.dialogWidget.purpose, new_mci)

        QDialog.accept(self)


class GstZuordnungMainDialog(MainDialog):
    """
    dialog mit dem eine grundstückszuordnung erstellt wird
    """

    def __init__(self, parent=None):
        super(GstZuordnungMainDialog, self).__init__(parent)

        self.parent = parent

        self.dialog_window_title = 'Grundstücke zuordnen'
        self.set_reject_button_text('&Schließen')


# class GstModel(TableModel):
#
#     def __init__(self, parent, mci_list=[]):
#         super(self.__class__, self).__init__(parent, mci_list=mci_list)
#
#         # self.parent = parent
#         # self.mci_list = mci_list
#
#         self.header = ['Gst-Nr',
#                        'EZ',
#                        'KG-Nr',
#                        'KG-Name',
#                        'AWB',
#                        'Rechtsgrundlage',
#                        'beweidet (ha)',
#                        'beweidet (%)',
#                        'Gst-Fläche (ha)',
#                        'Datenstand']
#
#     def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
#
#         row = index.row()
#         col = index.column()
#
#         # if role == Qt.TextAlignmentRole:
#         #
#         #     if index.column() in [5, 6, 7]:
#         #
#         #         return Qt.AlignRight | Qt.AlignVCenter
#         #
#         #     if index.column() in [0, 2, 3]:
#         #
#         #         return Qt.AlignHCenter | Qt.AlignVCenter
#         #
#         # if role == Qt.BackgroundRole:
#         #
#         #     if index.column() == 2:
#         #
#         #         if self.mci_list[row].rel_bearbeitungsstatus is not None:
#         #
#         #             color_str = self.mci_list[row].rel_bearbeitungsstatus.color
#         #             color_list = color_str.split(", ")
#         #
#         #             return QColor(int(color_list[0]),
#         #                           int(color_list[1]),
#         #                           int(color_list[2]))
#
#
#         if index.column() == 0:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].rel_gst.gst
#             # if role == Qt.EditRole:
#             #     return self.mci_list[row].az
#
#         # if role == Qt.BackgroundRole:
#         #     if index.column() == 5:
#         #         val_5 = self.data(self.index(index.row(), index.column()), Qt.DisplayRole)
#         #         if val_5 == 'eingetragen':
#         #             return QColor(189, 239, 255)
#         #         if val_5 == 'nicht eingetragen':
#         #             return QColor(234, 216, 54)
#         #         if val_5 == 'gelöscht':
#         #             return QColor(234, 163, 165)
#         #         if val_5 == 'historisch':
#         #             return QColor(170, 170, 170)
#         #
#         # if role == Qt.DisplayRole:
#         #
#         #     if index.column() == 7:  # beweidet ha
#         #         val = self.data(index, Qt.EditRole)
#         #         if val:
#         #             try:
#         #                 return '{:.4f}'.format(
#         #                     round(float(val) / 10000, 4)).replace(".", ",")
#         #             except ValueError:
#         #                 pass
#         #     """errechne den anteil der beweidet wird"""
#         #     if index.column() == 8:  # beweidet %
#         #         bew_val = self.data(self.index(index.row(), 7), Qt.EditRole)
#         #         total_val = self.data(self.index(index.row(), 9), Qt.EditRole)
#         #         if not bew_val:
#         #             return ''
#         #         else:
#         #             val = (bew_val / total_val) * 100
#         #             try:
#         #                 return '{:.2f}'.format(
#         #                     round(float(val), 2)).replace(".", ",")
#         #             except ValueError:
#         #                 pass
#         #     """"""
#         #
#         #     if index.column() == 9:  # Gst-Fläche
#         #         val = self.data(index, Qt.EditRole)
#         #         if val:
#         #             try:
#         #                 return '{:.4f}'.format(
#         #                     round(float(val) / 10000, 4)).replace(".", ",")
#         #             except ValueError:
#         #                 pass
#         #
#         # return super().data(index, role)

# class GstModelNew(TableModel):
#
#     # def __init__(self, parent, mci_list=[]):
#     #     super(__class__, self).__init__(parent, mci_list=mci_list)
#     def __init__(self, parent):
#         super(__class__, self).__init__(parent)
#
#         # self.mci_list = self.parent.parent._entity_mci.rel_gst_zuordnung
#
#         self.header = ['Gst-Nr',
#                        'Ez',
#                        'KG-Nr',
#                        'KG-Name',
#                        'AWB',
#                        'Rechtsgrundlage',
#                        'GB-Fläche',
#                        'GIS-Fläche',
#                        'davon beweidet',
#                        'beweidet (%)',
#                        'Datenstand']
#
#     def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
#
#         """
#         erzeuge ein basis-model
#         """
#         row = index.row()
#         col = index.column()
#
#         if role == Qt.TextAlignmentRole:
#
#             if index.column() in [2, 6, 7, 8, 9]:
#
#                 return Qt.AlignRight | Qt.AlignVCenter
#
#             if index.column() in [1, 10]:
#
#                 return Qt.AlignHCenter | Qt.AlignVCenter
#
#         if index.column() == 0:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].rel_gst.gst
#
#         if index.column() == 1:
#             if role == Qt.DisplayRole:
#
#                 gst_versionen_list = self.mci_list[row].rel_gst.rel_alm_gst_version
#                 last_gst = max(gst_versionen_list,
#                                key=attrgetter('rel_alm_gst_ez.datenstand'))
#
#                 return last_gst.rel_alm_gst_ez.ez
#
#         if index.column() == 2:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].rel_gst.kgnr
#
#         if index.column() == 3:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].rel_gst.rel_kat_gem.kgname
#
#         if index.column() == 4:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].rel_awb_status.name
#                 # return self.mci_list[row].awb_status_id
#
#             if role == Qt.EditRole:
#                 return self.mci_list[row].rel_awb_status.id
#
#             if role == Qt.BackgroundRole:
#
#                     if self.mci_list[row].rel_awb_status.id == 1:
#                         return QColor(189, 239, 255)
#                     if self.mci_list[row].rel_awb_status.id == 0:
#                         return QColor(234, 216, 54)
#                     if self.mci_list[row].rel_awb_status.id == 2:
#                         return QColor(234, 163, 165)
#
#         if index.column() == 5:
#             if role == Qt.DisplayRole:
#                 return self.mci_list[row].rel_rechtsgrundlage.name
#
#         if index.column() == 7 or index.column() == 8 or index.column() == 9:  # davon beweidet
#
#             gst_versionen_list = self.mci_list[row].rel_gst.rel_alm_gst_version
#             last_gst = max(gst_versionen_list,
#                            key=attrgetter('rel_alm_gst_ez.datenstand'))
#
#             gst_geom = QgsGeometry.fromWkt(
#                 to_shape(last_gst.geometry).wkt)
#
#             cut_area = 0.00
#             for cut in last_gst.rel_cut_koppel_gst:
#                 cut_geom = QgsGeometry.fromWkt(to_shape(cut.geometry).wkt)
#                 cut_area = cut_area + cut_geom.area()
#
#             if index.column() == 7:  # gis_area
#
#                 if role == Qt.DisplayRole:
#                     return ('{:.4f}'.format(
#                         round(float(gst_geom.area()) / 10000, 4))
#                             .replace(".", ",")) + ' ha'
#
#             if index.column() == 8:  # davon beweidet
#
#                 if role == Qt.EditRole:
#
#                     # return ('{:.0f}'.format(round(cut_area, 0)))
#                     return int(cut_area)
#
#                 if role == Qt.DisplayRole:
#
#                     return ('{:.4f}'.format(round(float(cut_area) / 10000, 4))
#                             .replace(".", ",")) + ' ha'
#
#             if index.column() == 9:  # % beweidet
#
#                 cut_anteil = cut_area / gst_geom.area() * 100
#
#                 if role == Qt.EditRole:
#                     # return ('{:.0f}'.format(round(cut_area, 0)))
#                     return ('{:.1f}'.format(round(float(cut_anteil), 1)))
#
#                 if role == Qt.DisplayRole:
#
#                     return ('{:.1f}'.format(round(float(cut_anteil), 1))
#                             .replace(".", ",")) + ' %'

        # if index.column() == 7:  # gis_area
        #     if role == Qt.DisplayRole:
        #
        #         gst_versionen_list = self.mci_list[row].rel_gst.rel_alm_gst_version
        #         last_gst = max(gst_versionen_list,
        #                        key=attrgetter('rel_alm_gst_ez.datenstand'))
        #
        #         gst_geom = QgsGeometry.fromWkt(
        #             to_shape(last_gst.geometry).wkt
        #         )
        #
        #         return ('{:.4f}'.format(round(float(gst_geom.area()) / 10000, 4))
        #                 .replace(".", ",")) + ' ha'

        # if index.column() == 6:  # gb_area
        #
        #     area = 0
        #     gst_versionen_list = self.mci_list[row].rel_gst.rel_alm_gst_version
        #     last_gst = max(gst_versionen_list,
        #                    key=attrgetter('rel_alm_gst_ez.datenstand'))
        #     for nutz in last_gst.rel_alm_gst_nutzung:
        #         area = area + nutz.area
        #
        #     if role == Qt.EditRole:
        #
        #         return area
        #
        #     if role == Qt.DisplayRole:
        #
        #         return ('{:.4f}'.format(round(float(area) / 10000, 4))
        #                 .replace(".", ",")) + ' ha'
        #
        # if index.column() == 10: # datenstand
        #     if role == Qt.DisplayRole:
        #
        #         gst_versionen_list = self.mci_list[row].rel_gst.rel_alm_gst_version
        #         last_gst = max(gst_versionen_list,
        #                        key=attrgetter('rel_alm_gst_ez.datenstand'))
        #
        #         return last_gst.rel_alm_gst_ez.datenstand[:10]

        # return super().data(index, role)

    # def rowCount(self, parent: QModelIndex = ...):
    #     """
    #     definiere die zeilenanzahl
    #     """
    #
    #     if self.mci_list:
    #         return len(self.mci_list)
    #     else:
    #         return 0
    #
    # def columnCount(self, parent: QModelIndex = ...):
    #     """
    #     definiere die spaltenanzahl
    #     """
    #     return 11
    #
    # def headerData(self, column, orientation, role=None):
    #     """
    #     wenn individuelle überschriften gesetzt sind (in 'maintable_columns')
    #     dann nehme diese
    #     """
    #     super().headerData(column, orientation, role)
    #
    #     if self.header:
    #         if role == Qt.DisplayRole and orientation == Qt.Horizontal:
    #
    #             return self.header[column]
    #     # else:
    #     #     return super().headerData(column, orientation, role)


class GstTableModel(GisTableModel):

    def __init__(self, layerCache, parent=None):
        super(GisTableModel, self).__init__(layerCache, parent)

    def data(self, index: QModelIndex, role: int = ...):

        # feat = self.feature(index)

        if role == Qt.TextAlignmentRole:

            if index.column() in [3]:

                return Qt.AlignRight | Qt.AlignVCenter

            if index.column() in [1, 2]:

                return Qt.AlignHCenter | Qt.AlignVCenter

        if index.column() == 3:

            if role == Qt.DisplayRole:

                return str(self.feature(index).attribute('kgnr'))

        if index.column() == 9:  # gis_area

            if role == Qt.DisplayRole:

                area = self.feature(index).attribute('gis_area')
                area_r = '{:.4f}'.format(round(float(area) / 10000, 4)
                                         ).replace(".", ",")
                return area_r + ' ha'

            # if role == Qt.EditRole:
            #     return area

        if index.column() == 10:  # gb_area

            if role == Qt.DisplayRole:

                area = self.feature(index).attribute('gb_area')
                area_r = '{:.4f}'.format(round(float(area) / 10000, 4)
                                         ).replace(".", ",")
                return area_r + ' ha'

            # if role == Qt.EditRole:
            #     return area

        return super().data(index, role)


class GstAktDataView(DataView):
    """
    grundstückstabelle im akt
    """
    # gis_relation = {"gis_id_column": 0,
    #                 "gis_layer_style_id": 99,
    #                 "gis_layer_id_column": 'id'}

    # entity_widget_class = GstZuordnungDataForm
    # entity_dialog_class = GstDialog
    # _entity_mc = BGstZuordnung
    # _model_class = GstModelNew
    # _data_source = 'di'

    # _main_table_model_class = GstModelNew
    # _model_class = GstModelNew

    _maintable_text = ["Grundstück", "Grundstücke", "kein Grundstück"]
    _delete_window_title = ["Grundstück löschen", "Grundstücke löschen"]
    _delete_window_text_single = "Soll das ausgewählte Grundstück " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Grundstücke wirklich gelöscht werden?"]
    _delete_text = ["Das Grundstück", "kann nicht gelöscht werden, da es "
                                          "verwendet wird!"]

    # _commit_entity = False
    # edit_entity_by = 'mci'

    # _gis_table_model_class = GstTableModel
    # data_view_class = GisTableView

    gst_zuordnung_wdg_class = GstZuordnung
    gst_zuordnung_dlg_class = GstZuordnungMainDialog

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.entity_dialog_class = GstDialog
        self.entity_widget_class = GstZuordnungDataForm

        self._entity_mc = BGstZuordnung
        self._gis_table_model_class = GstTableModel

        self._commit_entity = False
        self.edit_entity_by = 'mci'

        """"""
        self.setFeatureFields()
        self.setFilterUI()
        self.setCanvas(self.parent.guiMainGis.uiCanvas)

        self._gis_layer = self.setLayer()

        self.loadData()
        self.setFeaturesFromMci()
        self.setTableView()

        self.finalInit()

        self.updateFooter()

        self.signals()


        # self.vector_layer_cache = QgsVectorLayerCache(gis_layer, 10000)
        # self.attribute_table_model = QgsAttributeTableModel(self.vector_layer_cache)
        # self.attribute_table_model.loadLayer()
        #
        # self.attribute_table_filter_model = QgsAttributeTableFilterModel(
        #     canvas,
        #     self.attribute_table_model
        # )
        # # self.attribute_table_view = self.data_view_class(self)
        # self.attribute_table_view = GisTableView(self)
        # self.attribute_table_view.setModel(self.attribute_table_filter_model)
        #
        # # self.attribute_table_view.setSelectionBehavior(
        # #     QAbstractItemView.SelectRows)
        #
        # self.uiTableVlay.addWidget(self.attribute_table_view)

    def openGstZuordnung(self):
        """
        öffne den dialog um gst-zuordnungen durchführen zu können
        """

        self.gst_zuordnung_widget = self.gst_zuordnung_wdg_class(
            self, self.parent.entity_id)
        self.zuordnungs_dialog = self.gst_zuordnung_dlg_class(self)
        self.gst_zuordnung_widget.dialog_widget = self.zuordnungs_dialog

        self.zuordnungs_dialog.initDialog(self.gst_zuordnung_widget,
                                          width=1700,
                                          height=700)
        # self.gst_zuordnung_widget.initWidget()

        result = self.zuordnungs_dialog.exec()

        if result:
            self.updateMaintable()

    def initUi(self):
        super().initUi()

        self.uiTitleLbl.setVisible(True)

        self.uiTitleLbl.setText('zugeordnete Grundstücke')

        # self.setStretchMethod(2)

        # self.insertFooterLine('im AWB eingetragen und beweidet:',
        #                       'ha', 8, 120,
        #                       0.0001, 4, 4,
        #                       '==', 1)
        # # self.insertFooterLine('beweidet:',
        # #                       'ha', 8, 120,
        # #                       0.0001, 4)
        self.insertFooterLine('im AWB eingetrage Grundstücksfläche (GB):',
                              'ha', 'gb_area', 120,
                              0.0001, 4, 'awb_id',
                              '==', 1)
        self.insertFooterLine('zugeordnete Grundstücksgesamtfläche (GIS):',
                              'ha', 'gis_area', 120,
                              0.0001, 4)
        self.insertFooterLine('zugeordnete Grundstücksgesamtfläche (GB):',
                              'ha', 'gb_area', 120,
                              0.0001, 4)
        #
        # self.uiAddDataTbtn.setToolTip("ordne diesem Akt Grundstücke zu")
        #
        # self.test_cut_btn = QPushButton()
        # self.test_cut_btn.setText('test_cut')
        # self.uiTableFilterHLay.addWidget(self.test_cut_btn)
        #
        # self.test_update_btn = QPushButton()
        # self.test_update_btn.setText('test_update')
        # self.uiTableFilterHLay.addWidget(self.test_update_btn)

    def loadData(self):

        self._mci_list = self.parent._entity_mci.rel_gst_zuordnung

    def setLayer(self):

        layer = GstZuordLayer(
            "Polygon?crs=epsg:31259",
            "GstZuordnungLay",
            "memory",
            feature_fields=self.feature_fields
        )
        return layer

    def getCustomEntityData(self):

        print(f'...')
        """erhalte die mci-liste mit den gst-awb-statusen von der session
        bei der initialisierung des aktes"""

        self.custom_entity_data['awb_status'] \
            = self.parent._custom_entity_data['gst_awb_status']

        self.custom_entity_data['recht_status'] \
            = self.parent._custom_entity_data['gst_recht_status']

        return self.custom_entity_data

    def setFeaturesFromMci(self):
        super().setFeaturesFromMci()

        for gst_zuor in self._mci_list:

            for gst_version in gst_zuor.rel_gst.rel_alm_gst_version:

                feat = Feature(self._gis_layer.fields(), self)

                self.setFeatureAttributes(feat, gst_zuor)

                # feat.setAttributes([gst_version.id,
                #                     gst_zuor.rel_gst.gst,
                #                     gst_version.rel_alm_gst_ez.ez,
                #                     gst_version.rel_alm_gst_ez.kgnr,
                #                     gst_version.rel_alm_gst_ez.rel_kat_gem.kgname,
                #                     gst_zuor.awb_status_id,
                #                     gst_zuor.rechtsgrundlage_id,
                #                     '',
                #                     gst_version.rel_alm_gst_ez.datenstand])

                geom_wkt = to_shape(gst_version.geometry).wkt
                geom_new = QgsGeometry()
                geom = geom_new.fromWkt(geom_wkt)

                feat.setGeometry(geom)

                self._gis_layer.data_provider.addFeatures([feat])

    def setFeatureFields(self):
        # super().setFeatureFields()

        gst_version_id_fld = QgsField("gst_version_id", QVariant.Int)

        gst_fld = QgsField("gst", QVariant.String)
        gst_fld.setAlias('Gst')

        ez_fld = QgsField("ez", QVariant.Int)
        ez_fld.setAlias('EZ')

        kgnr_fld = QgsField("kgnr", QVariant.Int)
        kgnr_fld.setAlias('KG-Nr')

        kgname_fld = QgsField("kgname", QVariant.String)
        kgname_fld.setAlias('KG-Name')

        awb_id_fld = QgsField("awb_id", QVariant.Int)

        awb_status_fld = QgsField("awb_status", QVariant.String)
        awb_status_fld.setAlias('AWB-Status')

        recht_id_fld = QgsField("recht_id", QVariant.Int)

        recht_status_fld = QgsField("recht_status", QVariant.String)
        recht_status_fld.setAlias('Rechtsgrundlage')

        gis_area_fld = QgsField("gis_area", QVariant.Double)
        gis_area_fld.setAlias('GIS-Fläche')

        gb_area_fld = QgsField("gb_area", QVariant.Double)
        gb_area_fld.setAlias('GB-Fläche')

        datenstand_fld = QgsField("datenstand", QVariant.String)
        datenstand_fld.setAlias('Datenstand')

        self.feature_fields.append(gst_version_id_fld)
        self.feature_fields.append(gst_fld)
        self.feature_fields.append(ez_fld)
        self.feature_fields.append(kgnr_fld)
        self.feature_fields.append(kgname_fld)
        self.feature_fields.append(awb_id_fld)
        self.feature_fields.append(awb_status_fld)
        self.feature_fields.append(recht_id_fld)
        self.feature_fields.append(recht_status_fld)
        self.feature_fields.append(gis_area_fld)
        self.feature_fields.append(gb_area_fld)
        self.feature_fields.append(datenstand_fld)

    def setFeatureAttributes(self, feature, mci):
        super().setFeatureAttributes(feature, mci)

        # """weide_area"""
        # weide_area = 0.00
        # if mci.rel_abgrenzung != []:
        #     last_abgrenzung = max(mci.rel_abgrenzung,
        #                           key=attrgetter('jahr'))
        #     for komplex in last_abgrenzung.rel_komplex:
        #         for koppel in komplex.rel_koppel:
        #             weide_area = weide_area + koppel.koppel_area
        # """weide_area"""
        #
        # """awb area"""
        # gst_area = 0
        # for gst_zuord in mci.rel_gst_zuordnung:
        #
        #     if gst_zuord.awb_status_id == 1:
        #         gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
        #         last_gst = max(gst_versionen_list,
        #                        key=attrgetter('rel_alm_gst_ez.datenstand'))
        #
        #         gst_nutz_area = 0
        #         for ba in last_gst.rel_alm_gst_nutzung:
        #             gst_nutz_area = gst_nutz_area + ba.area
        #         gst_area = gst_area + gst_nutz_area
        # """"""
        #
        # """awb beweidet"""
        # cut_area = 0
        # for gst_zuord in mci.rel_gst_zuordnung:
        #
        #     if gst_zuord.awb_status_id == 1:
        #         gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
        #         last_gst = max(gst_versionen_list,
        #                        key=attrgetter('rel_alm_gst_ez.datenstand'))
        #
        #         for cut in last_gst.rel_cut_koppel_gst:
        #             cut_area = cut_area + cut.cutarea
        # """"""
        """last_gst"""
        gst_versionen_list = mci.rel_gst.rel_alm_gst_version
        last_gst = max(gst_versionen_list,
                       key=attrgetter('rel_alm_gst_ez.datenstand'))
        """"""

        """gb_area"""
        gb_area = 0
        # gst_versionen_list = self.mci_list[row].rel_gst.rel_alm_gst_version
        # last_gst = max(gst_versionen_list,
        #                key=attrgetter('rel_alm_gst_ez.datenstand'))
        for nutz in last_gst.rel_alm_gst_nutzung:
            gb_area = gb_area + nutz.area
        """"""

        feature['gst_version_id'] = mci.id
        feature['gst'] = mci.rel_gst.gst
        feature['ez'] = last_gst.rel_alm_gst_ez.ez
        feature['kgnr'] = mci.rel_gst.kgnr
        feature['kgname'] = mci.rel_gst.rel_kat_gem.kgname
        feature['awb_id'] = mci.awb_status_id
        feature['awb_status'] = mci.rel_awb_status.name
        feature['recht_id'] = mci.rechtsgrundlage_id
        feature['recht_status'] = mci.rel_rechtsgrundlage.name
        feature['gis_area'] = last_gst.gst_gis_area
        feature['gb_area'] = gb_area
        feature['datenstand'] = last_gst.rel_alm_gst_ez.datenstand

    def updateFeatureAttributes(self, *args):
        super().updateFeatureAttributes(args)

        new_mci = args[0][0]

        self.setFeatureAttributes(self.current_feature, new_mci)

    def setFilterUI(self):
        """
        setze das layout für die filter
        :return:
        """

        filter_lay = QHBoxLayout(self)

        """filter gst"""
        # filter_name = FilterElement(self)
        # filter_name.uiLabelLbl.setText('Name:')
        self.filter_gst_lbl = QLabel(self)

        gst_lbl_font = self.filter_gst_lbl.font()
        gst_lbl_font.setFamily(config.font_family)
        self.filter_gst_lbl.setFont(gst_lbl_font)

        self.filter_gst_lbl.setText('Gst:')
        self.filter_gst_lbl.setVisible(False)

        self.filter_gst_input_wdg = QLineEdit(self)

        gst_input_wdg_font = self.filter_gst_input_wdg.font()
        gst_input_wdg_font.setPointSize(11)
        gst_input_wdg_font.setFamily(config.font_family)
        self.filter_gst_input_wdg.setFont(gst_input_wdg_font)

        self.filter_gst_input_wdg.setPlaceholderText('Gst')
        self.filter_gst_input_wdg.setClearButtonEnabled(True)
        self.filter_gst_input_wdg.setMaximumWidth(80)
        # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)

        self.filter_gst_input_wdg.textChanged.connect(self.useFilter)

        # filter_lay.addWidget(filter_name)
        """"""

        """filter ez"""
        # filter_az = FilterElement(self)
        # filter_az.uiLabelLbl.setText('AZ:')

        self.filter_ez_lbl = QLabel(self)

        ez_lbl_font = self.filter_ez_lbl.font()
        ez_lbl_font.setFamily(config.font_family)
        self.filter_ez_lbl.setFont(ez_lbl_font)

        self.filter_ez_lbl.setText('Ez:')
        self.filter_ez_lbl.setVisible(False)

        self.filter_ez_input_wdg = QLineEdit(self)
        self.filter_ez_input_wdg.setPlaceholderText('EZ')
        ez_input_wdg_font = self.filter_ez_input_wdg.font()
        ez_input_wdg_font.setPointSize(11)
        ez_input_wdg_font.setFamily(config.font_family)
        self.filter_ez_input_wdg.setFont(ez_input_wdg_font)
        self.filter_ez_input_wdg.setClearButtonEnabled(True)
        self.filter_ez_input_wdg.setMaximumWidth(80)
        # filter_az.uiFilterElementLay.insertWidget(1, self.filter_az_input_wdg)

        self.filter_ez_input_wdg.textChanged.connect(self.useFilter)
        """"""

        """filter kgnr"""
        # filter_name = FilterElement(self)
        # filter_name.uiLabelLbl.setText('Name:')
        self.filter_kgnr_lbl = QLabel(self)

        kgnr_lbl_font = self.filter_kgnr_lbl.font()
        kgnr_lbl_font.setFamily(config.font_family)
        self.filter_kgnr_lbl.setFont(kgnr_lbl_font)

        self.filter_kgnr_lbl.setText('KG-Nr:')
        self.filter_kgnr_lbl.setVisible(False)

        self.filter_kgnr_input_wdg = QLineEdit(self)

        kgnr_input_wdg_font = self.filter_kgnr_input_wdg.font()
        kgnr_input_wdg_font.setPointSize(11)
        kgnr_input_wdg_font.setFamily(config.font_family)
        self.filter_kgnr_input_wdg.setFont(kgnr_input_wdg_font)

        self.filter_kgnr_input_wdg.setPlaceholderText('KG-Nr')
        self.filter_kgnr_input_wdg.setClearButtonEnabled(True)
        self.filter_kgnr_input_wdg.setMaximumWidth(80)
        # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)

        self.filter_kgnr_input_wdg.textChanged.connect(self.useFilter)

        # filter_lay.addWidget(filter_name)
        """"""

        """filter kgname"""
        # filter_name = FilterElement(self)
        # filter_name.uiLabelLbl.setText('Name:')
        self.filter_kgname_lbl = QLabel(self)

        kgname_lbl_font = self.filter_kgname_lbl.font()
        kgname_lbl_font.setFamily(config.font_family)
        self.filter_kgname_lbl.setFont(kgname_lbl_font)

        self.filter_kgname_lbl.setText('KG-Name:')
        self.filter_kgname_lbl.setVisible(False)

        self.filter_kgname_input_wdg = QLineEdit(self)

        kgname_input_wdg_font = self.filter_kgname_input_wdg.font()
        kgname_input_wdg_font.setPointSize(11)
        kgname_input_wdg_font.setFamily(config.font_family)
        self.filter_kgname_input_wdg.setFont(kgname_input_wdg_font)

        self.filter_kgname_input_wdg.setPlaceholderText('KG-Name')
        self.filter_kgname_input_wdg.setClearButtonEnabled(True)
        self.filter_kgname_input_wdg.setMaximumWidth(200)
        # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)

        self.filter_kgname_input_wdg.textChanged.connect(self.useFilter)

        # filter_lay.addWidget(filter_name)
        """"""

        """filter awb_status"""
        # filter_name = FilterElement(self)
        # filter_name.uiLabelLbl.setText('Name:')
        self.filter_awb_lbl = QLabel(self)

        awb_lbl_font = self.filter_awb_lbl.font()
        awb_lbl_font.setFamily(config.font_family)
        self.filter_awb_lbl.setFont(awb_lbl_font)

        self.filter_awb_lbl.setText('AWB-Status:')
        self.filter_awb_lbl.setVisible(False)

        self.filter_awb_input_wdg = QLineEdit(self)

        awb_input_wdg_font = self.filter_awb_input_wdg.font()
        awb_input_wdg_font.setPointSize(11)
        awb_input_wdg_font.setFamily(config.font_family)
        self.filter_awb_input_wdg.setFont(awb_input_wdg_font)

        self.filter_awb_input_wdg.setPlaceholderText('AWB-Status')
        self.filter_awb_input_wdg.setClearButtonEnabled(True)
        self.filter_awb_input_wdg.setMaximumWidth(200)
        # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)

        self.filter_awb_input_wdg.textChanged.connect(self.useFilter)

        # filter_lay.addWidget(filter_name)
        """"""

        """filter recht"""
        # filter_name = FilterElement(self)
        # filter_name.uiLabelLbl.setText('Name:')
        self.filter_recht_lbl = QLabel(self)

        recht_lbl_font = self.filter_recht_lbl.font()
        recht_lbl_font.setFamily(config.font_family)
        self.filter_recht_lbl.setFont(recht_lbl_font)

        self.filter_recht_lbl.setText('Rechtsgrundlage:')
        self.filter_recht_lbl.setVisible(False)

        self.filter_recht_input_wdg = QLineEdit(self)

        recht_input_wdg_font = self.filter_recht_input_wdg.font()
        recht_input_wdg_font.setPointSize(11)
        recht_input_wdg_font.setFamily(config.font_family)
        self.filter_recht_input_wdg.setFont(recht_input_wdg_font)

        self.filter_recht_input_wdg.setPlaceholderText('Rechtsgrundlage')
        self.filter_recht_input_wdg.setClearButtonEnabled(True)
        self.filter_recht_input_wdg.setMaximumWidth(200)
        # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)

        self.filter_recht_input_wdg.textChanged.connect(self.useFilter)

        # filter_lay.addWidget(filter_name)
        """"""

        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Minimum,
                                 QSizePolicy.Minimum)
        filter_lay.addItem(spacerItem1)

        filter_lay.addWidget(self.filter_gst_lbl)
        filter_lay.addWidget(self.filter_gst_input_wdg)
        filter_lay.addWidget(self.filter_ez_lbl)
        filter_lay.addWidget(self.filter_ez_input_wdg)
        filter_lay.addWidget(self.filter_kgnr_lbl)
        filter_lay.addWidget(self.filter_kgnr_input_wdg)
        filter_lay.addWidget(self.filter_kgname_lbl)
        filter_lay.addWidget(self.filter_kgname_input_wdg)
        filter_lay.addWidget(self.filter_awb_lbl)
        filter_lay.addWidget(self.filter_awb_input_wdg)
        filter_lay.addWidget(self.filter_recht_lbl)
        filter_lay.addWidget(self.filter_recht_input_wdg)
        """"""

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        filter_lay.addItem(spacerItem)

        self.uiHeaderHley.insertLayout(1, filter_lay)

    def useFilter(self):

        gst_text = self.filter_gst_input_wdg.text()
        ez_text = self.filter_ez_input_wdg.text()
        kgnr_text = self.filter_kgnr_input_wdg.text()
        kgname_text = self.filter_kgname_input_wdg.text()
        awb_text = self.filter_awb_input_wdg.text()
        recht_text = self.filter_recht_input_wdg.text()

        gst_expr = f"lower(\"gst\") LIKE '%{gst_text}%'"
        ez_expr = f"to_string(\"ez\") LIKE '%{ez_text}%'"
        kgnr_expr = f"to_string(\"kgnr\") LIKE '%{kgnr_text}%'"
        kgname_expr = f"lower(\"kgname\") LIKE '%{kgname_text}%'"
        awb_expr = f"lower(\"awb_status\") LIKE '%{awb_text}%'"
        recht_expr = f"lower(\"recht_status\") LIKE '%{recht_text}%'"

        expr_list = []

        if gst_text != '':
            self.filter_gst_lbl.setVisible(True)
            expr_list.append(gst_expr)
        else:
            self.filter_gst_lbl.setVisible(False)

        if ez_text != '':
            self.filter_ez_lbl.setVisible(True)
            expr_list.append(ez_expr)
        else:
            self.filter_ez_lbl.setVisible(False)

        if kgnr_text != '':
            self.filter_kgnr_lbl.setVisible(True)
            expr_list.append(kgnr_expr)
        else:
            self.filter_kgnr_lbl.setVisible(False)

        if kgname_text != '':
            self.filter_kgname_lbl.setVisible(True)
            expr_list.append(kgname_expr)
        else:
            self.filter_kgname_lbl.setVisible(False)

        if awb_text != '':
            self.filter_awb_lbl.setVisible(True)
            expr_list.append(awb_expr)
        else:
            self.filter_awb_lbl.setVisible(False)

        if recht_text != '':
            self.filter_recht_lbl.setVisible(True)
            expr_list.append(recht_expr)
        else:
            self.filter_recht_lbl.setVisible(False)

        if expr_list == []:
            self._gis_layer.setSubsetString('')
        else:

            expr_string = " and ".join(expr for expr in expr_list)
            print(f'expression string: {expr_string}')
            self._gis_layer.setSubsetString(expr_string)

        self.updateFooter()

    def signals(self):
        super().signals()

        self.uiAddDataTbtn.clicked.disconnect(self.add_row)
        self.uiAddDataTbtn.clicked.connect(self.openGstZuordnung)

        # self.test_cut_btn.clicked.connect(self.test_cut)
        # self.test_update_btn.clicked.connect(self.test_update)

    def test_update(self):

        topLeft = self.model.createIndex(0, 0)
        bottomRight = self.model.createIndex(11, 10)
        self.model.dataChanged.emit(topLeft, bottomRight)

        print(f'...')

    def test_cut(self):

        print(f'...')

        current_koppel_layer = self.parent.current_abgrenzung_item.data(GisItem.KoppelLayer_Role)
        cut_koppel_gstversion(current_koppel_layer)

    def finalInit(self):
        super().finalInit()

        self.view.setColumnHidden(0, True)
        self.view.setColumnHidden(5, True)
        self.view.setColumnHidden(7, True)

        self.view.sortByColumn(1, Qt.AscendingOrder)

        # """setzt bestimmte spaltenbreiten"""
        # self.view.setColumnWidth(1, 70)
        # self.view.setColumnWidth(2, 50)
        # self.view.setColumnWidth(3, 70)
        # self.view.setColumnWidth(4, 120)
        # self.view.setColumnWidth(5, 120)
        # self.view.setColumnWidth(6, 120)
        # self.view.setColumnWidth(7, 80)
        # """"""

        """passe die Zeilenhöhen an den Inhalt an"""
        # self.view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        """"""

        # self.view.resizeColumnsToContents()

    # def setMaintableColumns(self):
    #     super().setMaintableColumns()

        # self.maintable_columns[0] = MaintableColumn(column_type='int',
        #                                             visible=False)
        # self.maintable_columns[1] = MaintableColumn(heading='Gst-Nr',
        #                                             column_type='str',
        #                                             alignment='c')
        # self.maintable_columns[2] = MaintableColumn(heading='EZ',
        #                                             column_type='str',
        #                                             alignment='c')
        # self.maintable_columns[3] = MaintableColumn(heading='KG-Nr',
        #                                             column_type='int')
        # self.maintable_columns[4] = MaintableColumn(heading='KG-Name',
        #                                             column_type='str',
        #                                             alignment='l')
        # self.maintable_columns[5] = MaintableColumn(heading='AWB',
        #                                             column_type='str')
        # self.maintable_columns[6] = MaintableColumn(heading='Rechtsgrundlage',
        #                                             column_type='str',
        #                                             alignment='l')
        # self.maintable_columns[7] = MaintableColumn(heading='beweidet (ha)',
        #                                             column_type='float')
        # self.maintable_columns[8] = MaintableColumn(heading='beweidet (%)',
        #                                             column_type='float')
        # self.maintable_columns[9] = MaintableColumn(heading='Gst-Fläche (ha)',
        #                                             column_type='str')
        # self.maintable_columns[10] = MaintableColumn(heading='Datenstand',
        #                                              column_type='str')

    # def getMainQuery(self, session):
    #     super().getMainQuery(session)

        # """subquery um die flaeche des verschnittes von koppel und
        # gst-version zu bekommen"""
        # sub_cutarea = session.query(
        #     BCutKoppelGstAktuell.gst_version_id,
        #     func.sum(func.ST_Area(BCutKoppelGstAktuell.geometry)).label("bew_area"),
        #     func.max(BAbgrenzung.jahr)
        # )\
        #     .select_from(BCutKoppelGstAktuell)\
        #     .join(BKoppel)\
        #     .join(BKomplex)\
        #     .join(BAbgrenzung)\
        #     .join(BAkt)\
        #     .filter(BAkt.id == self.parent._entity_mci.id)\
        #     .group_by(BCutKoppelGstAktuell.gst_version_id)\
        #     .subquery()
        # """"""
        #
        # query = session.query(BGstZuordnung.id,
        #                       BGst.gst,
        #                       BGstEz.ez,
        #                       BGst.kgnr,
        #                       BKatGem.kgname,
        #                       BGstAwbStatus.name,
        #                       BRechtsgrundlage.name,
        #                       sub_cutarea.c.bew_area,
        #                       None,  # platzhalter für 'beweidet %'
        #                       func.ST_Area(BGstVersion.geometry),
        #                       func.max(BGstEz.datenstand)) \
        #     .select_from(BGstZuordnung) \
        #     .join(BGst) \
        #     .join(BGstVersion) \
        #     .join(BGstEz) \
        #     .join(BKatGem) \
        #     .join(BGstAwbStatus) \
        #     .join(BRechtsgrundlage) \
        #     .outerjoin(sub_cutarea, BGstVersion.id == sub_cutarea.c.gst_version_id) \
        #     .filter(BGstZuordnung.akt_id == self.parent._entity_mci.id) \
        #     .group_by(BGstZuordnung.id)
        #
        # return query

    def updateMaintable(self):

        super().updateMaintable()

    def getDeleteInfo(self, index=None):
        super().getDeleteInfo(index)

        del_info = self.filter_proxy.data(
            self.filter_proxy.index(
                index.row(), 1))

        return del_info

    # def setMainTableModel(self):
    #     super().setMainTableModel()

        # return GstModel(self, self.maintable_dataarray)


# class GstModelNew(QAbstractTableModel):
#
#     def __init__(self, parent, mci_list=None):
#         super(__class__, self).__init__(parent)
#
#         self.mci_list = mci_list
#
#         self.header = ['aa', 'bb', 'cc', 'cc', 'cc', 'cc', 'cc', 'cc', 'cc', 'cc']
#
#     def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
#         """
#         erzeuge ein basis-model
#         """
#
#     def rowCount(self, parent: QModelIndex = ...):
#         """
#         definiere die zeilenanzahl
#         """
#
#         if self.mci_list:
#             return len(self.mci_list)
#         else:
#             return 0
#
#     def columnCount(self, parent: QModelIndex = ...):
#         """
#         definiere die spaltenanzahl
#         """
#         return 10
#
#     def headerData(self, column, orientation, role=None):
#         """
#         wenn individuelle überschriften gesetzt sind (in 'maintable_columns')
#         dann nehme diese
#         """
#         super().headerData(column, orientation, role)
#
#         if self.header:
#             if role == Qt.DisplayRole and orientation == Qt.Horizontal:
#
#                 return self.header[column]
#         # else:
#         #     return super().headerData(column, orientation, role)
