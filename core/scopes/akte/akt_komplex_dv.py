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

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core import config, db_session_cm
from core.data_model import BGstZuordnung, BGst, BGstEz, \
    BGstVersion, BKatGem, BGstAwbStatus, BRechtsgrundlage, BCutKoppelGstAktuell, \
    BKomplex, BAkt, BKoppel, BAbgrenzung, BKomplexName
from core.entity import EntityDialog
from core.gis_item import GisItem
from core.gis_layer import setLayerStyle, ZVectorLayer, Feature
from core.gis_tools import cut_koppel_gstversion
from core.main_dialog import MainDialog
from core.data_view import DataView, TableModel, TableView, GisTableView, \
    GisTableModel
import typing

from operator import attrgetter

from core.scopes.gst.gst_zuordnung import GstZuordnung
from core.scopes.gst.gst_zuordnung_dataform import GstZuordnungDataForm


class KomplexDialog(EntityDialog):
    """
    dialog für die anzeige einer grundstückszuordnung
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        # self.parent = parent
        #
        # self.enableApply = True

        self.dialog_window_title = 'Komplex'
        # self.set_apply_button_text('&Speichern und Schließen')


    def accept(self):
        super().accept()

        if self.dialogWidget.acceptEntity() is not None:

            new_mci = self.dialogWidget.acceptEntity()

            self.parent.updateMaintableNew(self.dialogWidget.purpose, new_mci)

        QDialog.accept(self)


class KomplexModel(GisTableModel):

    def __init__(self, layerCache, parent=None):
        super(KomplexModel, self).__init__(layerCache, parent)

    def data(self, index: QModelIndex, role: int = ...):

        # feat = self.feature(index)

        if role == Qt.TextAlignmentRole:

            # if index.column() in [3]:
            #
            #     return Qt.AlignRight | Qt.AlignVCenter

            if index.column() in [2]:

                return Qt.AlignHCenter | Qt.AlignVCenter

    #     if index.column() == 3:
    #
    #         if role == Qt.DisplayRole:
    #
    #             return str(self.feature(index).attribute('kgnr'))
    #
    #     if index.column() == 9:  # gis_area
    #
    #         if role == Qt.DisplayRole:
    #
    #             area = self.feature(index).attribute('gis_area')
    #             area_r = '{:.4f}'.format(round(float(area) / 10000, 4)
    #                                      ).replace(".", ",")
    #             return area_r + ' ha'
    #
    #         # if role == Qt.EditRole:
    #         #     return area
    #
    #     if index.column() == 10:  # gb_area
    #
    #         if role == Qt.DisplayRole:
    #
    #             area = self.feature(index).attribute('gb_area')
    #             area_r = '{:.4f}'.format(round(float(area) / 10000, 4)
    #                                      ).replace(".", ",")
    #             return area_r + ' ha'
    #
    #         # if role == Qt.EditRole:
    #         #     return area
    #
        return super().data(index, role)


class KomplexAktDataView(DataView):
    """
    koppeltabelle im akt
    """

    _maintable_text = ["Komplex", "Komplexe", "keine Komplexe"]
    _delete_window_title = ["Komplex löschen", "Komplexe löschen"]
    _delete_window_text_single = "Soll der ausgewählte Komplex " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Komplexe wirklich gelöscht werden?"]
    _delete_text = ["Der Komplex", "kann nicht gelöscht werden, da er "
                                          "verwendet wird!"]

    # gst_zuordnung_wdg_class = GstZuordnung
    # gst_zuordnung_dlg_class = GstZuordnungMainDialog

    def __init__(self, parent=None, gis_mode=False):
        super(__class__, self).__init__(parent, gis_mode)

        self.entity_dialog_class = KomplexDialog
        # self.entity_widget_class = GstZuordnungDataForm

        self._entity_mc = BKoppel
        self._model_gis_class = KomplexModel

        self._commit_entity = False
        self.edit_entity_by = 'mci'

        """"""
        # self.setFeatureFields()
        # self.setFilterUI()
        # self.setCanvas(self.parent.guiMainGis.uiCanvas)
        #
        # self._gis_layer = self.setLayer()
        #
        # self.loadData()
        # self.setFeaturesFromMci()
        # self.setTableView()
        #
        # self.finalInit()
        #
        # self.updateFooter()
        #
        # self.signals()

    # def openGstZuordnung(self):
    #     """
    #     öffne den dialog um gst-zuordnungen durchführen zu können
    #     """
    #
    #     self.gst_zuordnung_widget = self.gst_zuordnung_wdg_class(
    #         self, self.parent.entity_id)
    #     self.zuordnungs_dialog = self.gst_zuordnung_dlg_class(self)
    #     self.gst_zuordnung_widget.dialog_widget = self.zuordnungs_dialog
    #
    #     self.zuordnungs_dialog.initDialog(self.gst_zuordnung_widget,
    #                                       width=1700,
    #                                       height=700)
    #     # self.gst_zuordnung_widget.initWidget()
    #
    #     result = self.zuordnungs_dialog.exec()
    #
    #     if result:
    #         self.updateMaintable()

    def initUi(self):
        super().initUi()

        self.uiTitleLbl.setVisible(True)

        self.uiTitleLbl.setText('Komplexe')

        # self.insertFooterLine('im AWB eingetrage Grundstücksfläche (GB):',
        #                       'ha', 'gb_area', 120,
        #                       0.0001, 4, 'awb_id',
        #                       '==', 1)
        # self.insertFooterLine('zugeordnete Grundstücksgesamtfläche (GIS):',
        #                       'ha', 'gis_area', 120,
        #                       0.0001, 4)
        # self.insertFooterLine('zugeordnete Grundstücksgesamtfläche (GB):',
        #                       'ha', 'gb_area', 120,
        #                       0.0001, 4)

    def loadData(self, session=None):

        # self._mci_list = self.parent._entity_mci.rel_abgrenzung.rel_komplex
        # self._mci_list = self.parent.abgrenzung_table._mci_list[0].rel_komplex
        self._mci_list = self.parent._entity_mci.rel_komplex_name

        # stmt = select(
        #     BKomplexName
        # ).options(
        #     joinedload(BKomplexName.rel_komplex)
        #          .joinedload(BKomplex.rel_koppel)
        # ).options(
        #     joinedload(BKomplexName.rel_komplex)
        #          .joinedload(BKomplex.rel_komplex_name)
        # ).where(BKomplexName.akt_id == self.parent._entity_id)
        #
        # self._mci_list = session.scalars(stmt).unique().all()

    def setLayer(self):

        layer = ZVectorLayer(
            "Polygon?crs=epsg:31259",
            "Komplexe",
            "memory",
            feature_fields=self.feature_fields
        )

        setLayerStyle(layer, 'komplex_rot')

        return layer

    # def getCustomEntityData(self):
    #
    #     print(f'...')
    #     """erhalte die mci-liste mit den gst-awb-statusen von der session
    #     bei der initialisierung des aktes"""
    #
    #     self.custom_entity_data['awb_status'] \
    #         = self.parent._custom_entity_data['gst_awb_status']
    #
    #     self.custom_entity_data['recht_status'] \
    #         = self.parent._custom_entity_data['gst_recht_status']
    #
    #     return self.custom_entity_data

    def setFeaturesFromMci(self):
        super().setFeaturesFromMci()

        for komplex_name in self._mci_list:

            if komplex_name.rel_komplex != []:

                for komplex in komplex_name.rel_komplex:

                    # komplex = komplex_name.rel_komplex

                    komplex_geom = None

                    feat = Feature(self._gis_layer.fields(), self)

                    self.setFeatureAttributes(feat, komplex)

                    # feat.setAttributes([gst_version.id,
                    #                     gst_zuor.rel_gst.gst,
                    #                     gst_version.rel_alm_gst_ez.ez,
                    #                     gst_version.rel_alm_gst_ez.kgnr,
                    #                     gst_version.rel_alm_gst_ez.rel_kat_gem.kgname,
                    #                     gst_zuor.awb_status_id,
                    #                     gst_zuor.rechtsgrundlage_id,
                    #                     '',
                    #                     gst_version.rel_alm_gst_ez.datenstand])

                    if komplex.rel_koppel != []:

                        for koppel in komplex.rel_koppel:

                            geom_wkt = to_shape(koppel.geometry).wkt
                            geom_new = QgsGeometry()
                            geom = geom_new.fromWkt(geom_wkt)

                            if komplex_geom == None:

                                komplex_geom = geom
                            else:
                                komplex_geom = komplex_geom.combine(geom)

                    # geom_wkt = to_shape(koppel.geometry).wkt
                    # geom_new = QgsGeometry()
                    # geom = geom_new.fromWkt(geom_wkt)

                    feat.setGeometry(komplex_geom)
                    # feat.setGeometry(geom)

                    self._gis_layer.data_provider.addFeatures([feat])

    def setFeatureFields(self):
        # super().setFeatureFields()

        abgrenzung_id_fld = QgsField("abgrenzung_id", QVariant.Int)

        komplex_id_fld = QgsField("komplex_id", QVariant.Int)

        komplex_nr_fld = QgsField("komplex_nr", QVariant.Int)
        komplex_nr_fld.setAlias('Nr')

        komplex_name_fld = QgsField("komplex_name", QVariant.String)
        komplex_name_fld.setAlias('Name')

        # koppel_id_fld = QgsField("koppel_id", QVariant.Int)
        #
        # koppel_nr_fld = QgsField("koppel_nr", QVariant.Int)
        #
        # koppel_name_fld = QgsField("koppel_name", QVariant.String)
        #
        # nicht_weide_fld = QgsField("nicht_weide", QVariant.String)
        #
        # koppel_area_fld = QgsField("koppel_area", QVariant.Double)

        self.feature_fields.append(abgrenzung_id_fld)
        self.feature_fields.append(komplex_id_fld)
        self.feature_fields.append(komplex_nr_fld)
        self.feature_fields.append(komplex_name_fld)
        # self.feature_fields.append(komplex_name_fld)
        # self.feature_fields.append(koppel_id_fld)
        # self.feature_fields.append(koppel_nr_fld)
        # self.feature_fields.append(koppel_name_fld)
        # self.feature_fields.append(nicht_weide_fld)
        # self.feature_fields.append(koppel_area_fld)

    def setFeatureAttributes(self, feature, mci):
        super().setFeatureAttributes(feature, mci)

        # """last_gst"""
        # gst_versionen_list = mci.rel_gst.rel_alm_gst_version
        # last_gst = max(gst_versionen_list,
        #                key=attrgetter('rel_alm_gst_ez.datenstand'))
        # """"""
        #
        # """gb_area"""
        # gb_area = 0
        # # gst_versionen_list = self.mci_list[row].rel_gst.rel_alm_gst_version
        # # last_gst = max(gst_versionen_list,
        # #                key=attrgetter('rel_alm_gst_ez.datenstand'))
        # for nutz in last_gst.rel_alm_gst_nutzung:
        #     gb_area = gb_area + nutz.area
        # """"""

        feature['abgrenzung_id'] = mci.abgrenzung_id
        feature['komplex_id'] = mci.id
        feature['komplex_nr'] = mci.rel_komplex_name.nr
        feature['komplex_name'] = mci.rel_komplex_name.name
        # feature['komplex_name'] = mci.rel_komplex.rel_komplex_name.name
        # feature['koppel_id'] = mci.id
        # feature['koppel_nr'] = mci.nr
        # feature['koppel_name'] = mci.name
        # feature['nicht_weide'] = mci.nicht_weide
        # feature['koppel_area'] = 1.23

    def updateFeatureAttributes(self, *args):
        super().updateFeatureAttributes(args)

        new_mci = args[0][0]

        self.setFeatureAttributes(self.current_feature, new_mci)

    # def setFilterUI(self):
    #     """
    #     setze das layout für die filter
    #     :return:
    #     """
    #
    #     filter_lay = QHBoxLayout(self)
    #
    #     """filter gst"""
    #     # filter_name = FilterElement(self)
    #     # filter_name.uiLabelLbl.setText('Name:')
    #     self.filter_gst_lbl = QLabel(self)
    #
    #     gst_lbl_font = self.filter_gst_lbl.font()
    #     gst_lbl_font.setFamily(config.font_family)
    #     self.filter_gst_lbl.setFont(gst_lbl_font)
    #
    #     self.filter_gst_lbl.setText('Gst:')
    #     self.filter_gst_lbl.setVisible(False)
    #
    #     self.filter_gst_input_wdg = QLineEdit(self)
    #
    #     gst_input_wdg_font = self.filter_gst_input_wdg.font()
    #     gst_input_wdg_font.setPointSize(11)
    #     gst_input_wdg_font.setFamily(config.font_family)
    #     self.filter_gst_input_wdg.setFont(gst_input_wdg_font)
    #
    #     self.filter_gst_input_wdg.setPlaceholderText('Gst')
    #     self.filter_gst_input_wdg.setClearButtonEnabled(True)
    #     self.filter_gst_input_wdg.setMaximumWidth(80)
    #     # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)
    #
    #     self.filter_gst_input_wdg.textChanged.connect(self.useFilter)
    #
    #     # filter_lay.addWidget(filter_name)
    #     """"""
    #
    #     """filter ez"""
    #     # filter_az = FilterElement(self)
    #     # filter_az.uiLabelLbl.setText('AZ:')
    #
    #     self.filter_ez_lbl = QLabel(self)
    #
    #     ez_lbl_font = self.filter_ez_lbl.font()
    #     ez_lbl_font.setFamily(config.font_family)
    #     self.filter_ez_lbl.setFont(ez_lbl_font)
    #
    #     self.filter_ez_lbl.setText('Ez:')
    #     self.filter_ez_lbl.setVisible(False)
    #
    #     self.filter_ez_input_wdg = QLineEdit(self)
    #     self.filter_ez_input_wdg.setPlaceholderText('EZ')
    #     ez_input_wdg_font = self.filter_ez_input_wdg.font()
    #     ez_input_wdg_font.setPointSize(11)
    #     ez_input_wdg_font.setFamily(config.font_family)
    #     self.filter_ez_input_wdg.setFont(ez_input_wdg_font)
    #     self.filter_ez_input_wdg.setClearButtonEnabled(True)
    #     self.filter_ez_input_wdg.setMaximumWidth(80)
    #     # filter_az.uiFilterElementLay.insertWidget(1, self.filter_adr_input_wdg)
    #
    #     self.filter_ez_input_wdg.textChanged.connect(self.useFilter)
    #     """"""
    #
    #     """filter kgnr"""
    #     # filter_name = FilterElement(self)
    #     # filter_name.uiLabelLbl.setText('Name:')
    #     self.filter_kgnr_lbl = QLabel(self)
    #
    #     kgnr_lbl_font = self.filter_kgnr_lbl.font()
    #     kgnr_lbl_font.setFamily(config.font_family)
    #     self.filter_kgnr_lbl.setFont(kgnr_lbl_font)
    #
    #     self.filter_kgnr_lbl.setText('KG-Nr:')
    #     self.filter_kgnr_lbl.setVisible(False)
    #
    #     self.filter_kgnr_input_wdg = QLineEdit(self)
    #
    #     kgnr_input_wdg_font = self.filter_kgnr_input_wdg.font()
    #     kgnr_input_wdg_font.setPointSize(11)
    #     kgnr_input_wdg_font.setFamily(config.font_family)
    #     self.filter_kgnr_input_wdg.setFont(kgnr_input_wdg_font)
    #
    #     self.filter_kgnr_input_wdg.setPlaceholderText('KG-Nr')
    #     self.filter_kgnr_input_wdg.setClearButtonEnabled(True)
    #     self.filter_kgnr_input_wdg.setMaximumWidth(80)
    #     # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)
    #
    #     self.filter_kgnr_input_wdg.textChanged.connect(self.useFilter)
    #
    #     # filter_lay.addWidget(filter_name)
    #     """"""
    #
    #     """filter kgname"""
    #     # filter_name = FilterElement(self)
    #     # filter_name.uiLabelLbl.setText('Name:')
    #     self.filter_kgname_lbl = QLabel(self)
    #
    #     kgname_lbl_font = self.filter_kgname_lbl.font()
    #     kgname_lbl_font.setFamily(config.font_family)
    #     self.filter_kgname_lbl.setFont(kgname_lbl_font)
    #
    #     self.filter_kgname_lbl.setText('KG-Name:')
    #     self.filter_kgname_lbl.setVisible(False)
    #
    #     self.filter_kgname_input_wdg = QLineEdit(self)
    #
    #     kgname_input_wdg_font = self.filter_kgname_input_wdg.font()
    #     kgname_input_wdg_font.setPointSize(11)
    #     kgname_input_wdg_font.setFamily(config.font_family)
    #     self.filter_kgname_input_wdg.setFont(kgname_input_wdg_font)
    #
    #     self.filter_kgname_input_wdg.setPlaceholderText('KG-Name')
    #     self.filter_kgname_input_wdg.setClearButtonEnabled(True)
    #     self.filter_kgname_input_wdg.setMaximumWidth(200)
    #     # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)
    #
    #     self.filter_kgname_input_wdg.textChanged.connect(self.useFilter)
    #
    #     # filter_lay.addWidget(filter_name)
    #     """"""
    #
    #     """filter awb_status"""
    #     # filter_name = FilterElement(self)
    #     # filter_name.uiLabelLbl.setText('Name:')
    #     self.filter_awb_lbl = QLabel(self)
    #
    #     awb_lbl_font = self.filter_awb_lbl.font()
    #     awb_lbl_font.setFamily(config.font_family)
    #     self.filter_awb_lbl.setFont(awb_lbl_font)
    #
    #     self.filter_awb_lbl.setText('AWB-Status:')
    #     self.filter_awb_lbl.setVisible(False)
    #
    #     self.filter_awb_input_wdg = QLineEdit(self)
    #
    #     awb_input_wdg_font = self.filter_awb_input_wdg.font()
    #     awb_input_wdg_font.setPointSize(11)
    #     awb_input_wdg_font.setFamily(config.font_family)
    #     self.filter_awb_input_wdg.setFont(awb_input_wdg_font)
    #
    #     self.filter_awb_input_wdg.setPlaceholderText('AWB-Status')
    #     self.filter_awb_input_wdg.setClearButtonEnabled(True)
    #     self.filter_awb_input_wdg.setMaximumWidth(200)
    #     # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)
    #
    #     self.filter_awb_input_wdg.textChanged.connect(self.useFilter)
    #
    #     # filter_lay.addWidget(filter_name)
    #     """"""
    #
    #     """filter recht"""
    #     # filter_name = FilterElement(self)
    #     # filter_name.uiLabelLbl.setText('Name:')
    #     self.filter_recht_lbl = QLabel(self)
    #
    #     recht_lbl_font = self.filter_recht_lbl.font()
    #     recht_lbl_font.setFamily(config.font_family)
    #     self.filter_recht_lbl.setFont(recht_lbl_font)
    #
    #     self.filter_recht_lbl.setText('Rechtsgrundlage:')
    #     self.filter_recht_lbl.setVisible(False)
    #
    #     self.filter_recht_input_wdg = QLineEdit(self)
    #
    #     recht_input_wdg_font = self.filter_recht_input_wdg.font()
    #     recht_input_wdg_font.setPointSize(11)
    #     recht_input_wdg_font.setFamily(config.font_family)
    #     self.filter_recht_input_wdg.setFont(recht_input_wdg_font)
    #
    #     self.filter_recht_input_wdg.setPlaceholderText('Rechtsgrundlage')
    #     self.filter_recht_input_wdg.setClearButtonEnabled(True)
    #     self.filter_recht_input_wdg.setMaximumWidth(200)
    #     # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)
    #
    #     self.filter_recht_input_wdg.textChanged.connect(self.useFilter)
    #
    #     # filter_lay.addWidget(filter_name)
    #     """"""
    #
    #     spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Minimum,
    #                              QSizePolicy.Minimum)
    #     filter_lay.addItem(spacerItem1)
    #
    #     filter_lay.addWidget(self.filter_gst_lbl)
    #     filter_lay.addWidget(self.filter_gst_input_wdg)
    #     filter_lay.addWidget(self.filter_ez_lbl)
    #     filter_lay.addWidget(self.filter_ez_input_wdg)
    #     filter_lay.addWidget(self.filter_kgnr_lbl)
    #     filter_lay.addWidget(self.filter_kgnr_input_wdg)
    #     filter_lay.addWidget(self.filter_kgname_lbl)
    #     filter_lay.addWidget(self.filter_kgname_input_wdg)
    #     filter_lay.addWidget(self.filter_awb_lbl)
    #     filter_lay.addWidget(self.filter_awb_input_wdg)
    #     filter_lay.addWidget(self.filter_recht_lbl)
    #     filter_lay.addWidget(self.filter_recht_input_wdg)
    #     """"""
    #
    #     spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    #     filter_lay.addItem(spacerItem)
    #
    #     self.uiHeaderHley.insertLayout(1, filter_lay)

    def useSubsetString(self):

        self._gis_layer.setSubsetString(
            self.parent.filter_komplex_from_abgr_string)

        self.updateFooter()

    # def useFilter(self):
    #
    #     gst_text = self.filter_gst_input_wdg.text()
    #     ez_text = self.filter_ez_input_wdg.text()
    #     kgnr_text = self.filter_kgnr_input_wdg.text()
    #     kgname_text = self.filter_kgname_input_wdg.text()
    #     awb_text = self.filter_awb_input_wdg.text()
    #     recht_text = self.filter_recht_input_wdg.text()
    #
    #     gst_expr = f"lower(\"gst\") LIKE '%{gst_text}%'"
    #     ez_expr = f"to_string(\"ez\") LIKE '%{ez_text}%'"
    #     kgnr_expr = f"to_string(\"kgnr\") LIKE '%{kgnr_text}%'"
    #     kgname_expr = f"lower(\"kgname\") LIKE '%{kgname_text}%'"
    #     awb_expr = f"lower(\"awb_status\") LIKE '%{awb_text}%'"
    #     recht_expr = f"lower(\"recht_status\") LIKE '%{recht_text}%'"
    #
    #     expr_list = []
    #
    #     if gst_text != '':
    #         self.filter_gst_lbl.setVisible(True)
    #         expr_list.append(gst_expr)
    #     else:
    #         self.filter_gst_lbl.setVisible(False)
    #
    #     if ez_text != '':
    #         self.filter_ez_lbl.setVisible(True)
    #         expr_list.append(ez_expr)
    #     else:
    #         self.filter_ez_lbl.setVisible(False)
    #
    #     if kgnr_text != '':
    #         self.filter_kgnr_lbl.setVisible(True)
    #         expr_list.append(kgnr_expr)
    #     else:
    #         self.filter_kgnr_lbl.setVisible(False)
    #
    #     if kgname_text != '':
    #         self.filter_kgname_lbl.setVisible(True)
    #         expr_list.append(kgname_expr)
    #     else:
    #         self.filter_kgname_lbl.setVisible(False)
    #
    #     if awb_text != '':
    #         self.filter_awb_lbl.setVisible(True)
    #         expr_list.append(awb_expr)
    #     else:
    #         self.filter_awb_lbl.setVisible(False)
    #
    #     if recht_text != '':
    #         self.filter_recht_lbl.setVisible(True)
    #         expr_list.append(recht_expr)
    #     else:
    #         self.filter_recht_lbl.setVisible(False)
    #
    #     if expr_list == []:
    #         self._gis_layer.setSubsetString('')
    #     else:
    #
    #         expr_string = " and ".join(expr for expr in expr_list)
    #         print(f'expression string: {expr_string}')
    #         self._gis_layer.setSubsetString(expr_string)
    #
    #     self.updateFooter()

    def signals(self):
        super().signals()

        self.uiAddDataTbtn.clicked.disconnect(self.add_row)
        # self.uiAddDataTbtn.clicked.connect(self.openGstZuordnung)

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

        self.setStretchMethod(2)

        self.view.setColumnHidden(0, True)
        self.view.setColumnHidden(1, True)

        self.view.sortByColumn(2, Qt.AscendingOrder)

        """setzt bestimmte spaltenbreiten"""
        self.view.setColumnWidth(2, 50)
        """"""

        # self.setMaximumWidth(300)

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
