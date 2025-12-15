import weakref

from qga.data_view import QgaTableModel
from qga.dialog import QgaDialog
from qga.fields import QgaField
from qga.layer import QgaVectorLayer, setLayerStyle, GstZuordLayer, QgaFeature, \
    VectorLayerFactory, GeometryType
from qga.tools import convertMtoHaWithHa
from qgis.PyQt.QtCore import Qt, QModelIndex, QAbstractTableModel
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import (QHeaderView, QPushButton, QDialog, QDockWidget,
                                 QAbstractItemView, QSpacerItem, QLineEdit,
                                 QLabel, QHBoxLayout, QSizePolicy)

from geoalchemy2.shape import to_shape
from qgis.core import QgsFeature, QgsGeometry, QgsVectorLayerCache, QgsVectorLayer, QgsField, QgsPointXY
from qgis.PyQt.QtCore import QVariant

from qgis._gui import QgsAttributeTableModel, QgsAttributeTableView, QgsAttributeTableFilterModel

from geoalchemy2.shape import to_shape

from sqlalchemy import func, select

from almgis.data_model import DmGstZuordnung, DmGst, DmGstEz, \
    DmGstVersion, DmKatGem, DmGstAwbStatus, DmRechtsgrundlage, DmCutKoppelGstAktuell, \
    DmKomplex, DmAkt, DmKoppel, DmAbgrenzung
from almgis.data_view import AlmDataView
from almgis.entity import AlmEntityDialog
# from almgis.gis_item import GisItem
# from almgis.gis_layer import setLayerStyle, ZVectorLayer, Feature
# from almgis.gis_tools import cut_koppel_gstversion
# from almgis.main_dialog import MainDialog
# from almgis.data_view import AlmDataView, QgaTableModel, TableView, GisTableView, \
#     almgis, AlmDataView
import typing

from operator import attrgetter

# from almgis.main_gis import MainGis
from qga.main_wdg import QgaMainWdg

from almgis.fields import GeneralField, GstZuordnungField

from almgis.core.data_view import AlmTableModel


# from almgis.scopes.gst.gst_zuordnung import GstZuordnung
# from almgis.scopes.gst.gst_zuordnung_dataform import GstZuordnungDataForm
# from almgis.tools import getDmiState, getDmiSession


class GstDialog(AlmEntityDialog):
    """
    dialog für die anzeige einer grundstückszuordnung
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.dialog_size = [1880, 800]

        self.dialog_window_title = 'Grundstückszuordnung'


class GstGisDock(QDockWidget):
    """
    baseclass für das GisDock in der klasse 'Akt'
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.setWindowTitle('Kartenansicht')


class GstAllMainWidget(QgaMainWdg):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui.setTitle('zugeordnete Gst')

        self.main_wdg = GstAllDataView(self)

        self.main_wdg.updateDataViewSgn.connect(self.updateMainWdg)

        self.parent.updateAppSgn.connect(self.main_wdg.updateDataView)

        # with session_cm(name='main-widget - kontakt',
        #                    expire_on_commit=False) as session:

        # """erzeuge ein main_gis widget und füge es in ein GisDock ein"""
        # self.uiGisDock = GstGisDock(self)
        # self.guiMainGis = MainGis(self.uiGisDock, self)
        # self.guiMainGis.setMaingisSession(self.mainwidget_session)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.uiGisDock)
        # self.uiGisDock.setWidget(self.guiMainGis)
        # """"""
        #
        # """setzte den 'scope_id'; damit die richtigen layer aus dem
        # daten_model 'BGisScopeLayer' für dieses main_gis widget geladen werden"""
        # # self.guiMainGis.scope_id = 1
        # """"""
        #
        # self.guiMainGis.project_instance.addMapLayer(self.gst_table._gis_layer)
        # """"""
        #
        # """setzte die karte auf die ausdehnung des gst-layers"""
        # self.gst_table._gis_layer.updateExtents()
        # extent = self.gst_table._gis_layer.extent()
        # self.guiMainGis.uiCanvas.setExtent(extent)
        # """"""
        #
        # self.uiGisDock.topLevelChanged.connect(self.changedGisDockLevel)

    def setupMainWidget(self):
        super().setupMainWidget()

        self.main_wdg.setupDataView()
        self.ui.mainVlay.addWidget(self.main_wdg.ui)

    # def initMainWidget(self):
    #     super().initMainWidget()
    #
    #     self.uiMainVlay.addWidget(self.main_wdg)
    #     # self.kontakt_table.loadData()
    #     # self.kontakt_table.initDataView()
    #
    # def createMw(self):
    #
    #     self.main_wdg.initDataView()
    #
    #     self.initMainWidget()

    def changedGisDockLevel(self, level):
        """
        überwache den level des GisDock; zeige die schaltfläche 'uiUnfloatDock'
        nur wenn es losgelöst ist
        """
        if level:
            self.uiGisDock.setWindowFlags(Qt.CustomizeWindowHint |
                                          Qt.Window |
                                          Qt.WindowMinimizeButtonHint |
                                          Qt.WindowMaximizeButtonHint |
                                          Qt.WindowCloseButtonHint)
            self.uiGisDock.widget().uiUnfoatDock.setVisible(True)
            self.uiGisDock.show()
        else:
            self.uiGisDock.widget().uiUnfoatDock.setVisible(False)


class GstZuordnungMainDialog(QgaDialog):
    """
    dialog mit dem eine grundstückszuordnung erstellt wird
    """

    def __init__(self, parent=None):
        super(GstZuordnungMainDialog, self).__init__(parent)

        self.parent = parent

        self.dialog_window_title = 'Grundstücke zuordnen'
        self.set_reject_button_text('&Schließen')


class GstAllTableModel(AlmTableModel):
# class GstAllTableModel(QgsAttributeTableModel):

    def __init__(self, layerCache=None,
                 columns=None, parent=None):
        super().__init__(layerCache, columns, parent)

    # def __init__(self, dmi_list=None, layerCache=None,
    #              columns=None, parent=None):
    #     super().__init__(dmi_list, layerCache, columns, parent)
        print(f'...1')

    def data(self, index: QModelIndex, role: int = ...):

        print(f'////////////////////////////////////////////////////')

        # if role == Qt.TextAlignmentRole:
        #     # Set alignment for the "Age" column (column index 1)
        #     if index.column() == 1:
        #         return Qt.AlignHCenter | Qt.AlignVCenter
        #
        # if role == Qt.DisplayRole:
        #
        #     if self.layer().fields().field(index.column()).name() == 'akt_name':
        #         current_value = super().data(index, Qt.EditRole)
        #         return f"Akt: {current_value}"
        #
        #     if (self.layer().fields().field(index.column()).name() in
        #             ['last_gb_area', 'last_koppel_area', 'last_gis_area']):
        #         current_value = super().data(index, Qt.EditRole)
        #         return convertMtoHaWithHa(current_value)

        return super().data(index, role)

    #     # if role == Qt.BackgroundRole and getDmiState(self.feature(index).attribute('dmi')[0]) == "transient":
    #     #
    #     #     return color.added_data
    #     #
    #     # if role == Qt.TextAlignmentRole:
    #     #
    #     #     if index.column() in [5]:
    #     #
    #     #         return Qt.AlignRight | Qt.AlignVCenter
    #     #
    #     #     if index.column() in [3, 4]:
    #     #
    #     #         return Qt.AlignHCenter | Qt.AlignVCenter
    #     #
    #     # if role == Qt.BackgroundRole:
    #     #
    #     #     if index.column() == 8:
    #     #
    #     #         if self.feature(index).attribute('awb_id') == 0:  # nicht
    #     #             return QColor(234, 216, 54)
    #     #         elif self.feature(index).attribute('awb_id') == 1:  # eingetragen
    #     #             return QColor(189, 239, 255)
    #     #         elif self.feature(index).attribute('awb_id') == 2:  # gelöscht
    #     #             return QColor(234, 163, 165)
    #     #         elif self.feature(index).attribute('awb_id') == 3:  # teilweise
    #     #             return QColor(214, 239, 225)
    #     #         else:
    #     #             return QColor(255, 255, 255)
    #
    #     if index.column() == 11:  # gis_area
    #
    #         if role == Qt.DisplayRole:
    #
    #             area = self.feature(index).attribute('gis_area')
    #             area_r = '{:.4f}'.format(round(float(area) / 10000, 4)
    #                                      ).replace(".", ",")
    #             return area_r + ' ha'
    #
    #     if index.column() == 12:  # gb_area
    #
    #         if role == Qt.DisplayRole:
    #
    #             area = self.feature(index).attribute('gb_area')
    #             area_r = '{:.4f}'.format(round(float(area) / 10000, 4)
    #                                      ).replace(".", ",")
    #             return area_r + ' ha'
    #
    #     if index.column() == 13:  # bew_area
    #
    #         if role == Qt.DisplayRole:
    #             area = self.feature(index).attribute('bew_area')
    #             area_r = '{:.4f}'.format(round(float(area) / 10000, 4)
    #                                      ).replace(".", ",")
    #             return area_r + ' ha'
    #
    #     return super().data(index, role)


class GstAllDataView(AlmDataView):
    """
    alle gst mit akt
    """

    """weak container to store all live instances of the class"""
    _instances = weakref.WeakSet()
    """"""

    _maintable_text = ["Grundstück", "Grundstücke", "kein Grundstück"]
    _delete_window_title = ["Grundstück löschen", "Grundstücke löschen"]
    _delete_window_text_single = "Soll das ausgewählte Grundstück " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Grundstücke wirklich gelöscht werden?"]
    _delete_text = ["Das Grundstück", "kann nicht gelöscht werden, da es "
                                          "verwendet wird!"]

    # gst_zuordnung_wdg_class = GstZuordnung
    # gst_zuordnung_dlg_class = GstZuordnungMainDialog

    def __init__(self, parent=None, gis_mode=False):
        super(__class__, self).__init__(parent, gis_mode)

        # self.entity_dialog_class = GstDialog
        # self.entity_widget_class = GstZuordnungDataForm

        self.dmi_dict = self._dmi_dict

        self._entity_dmc = DmGstZuordnung
        self.model_class = GstAllTableModel
        # self._model_class = QgaTableModel

        # self.uiAddDataTbtn.setVisible(False)

        # _model_gis_class = GisTableModel
        # _view_gis_class = GisTableView

        # self._commit_entity = False
        # self.edit_entity_by = 'dmi'

        # self.layer = VectorLayerFactory.createLayer(
        #     'gst_all_main',
        #     geometry_type=GeometryType.POLYGON,
        #     fields_list=self.getFeatureFields()
        # )

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

    # def loadData(self, session=None):
    #
    #     self._dmi_list = self.parent._entity_dmi.rel_gst_zuordnung

    def getDmiList(self):

        stmt = ((select(DmGstZuordnung))
                .join(DmGstZuordnung.rel_gst)
                .group_by(DmGst.id))

        """stmt für gst die zugeordnet sind"""
        # stmt = ((select(DmGstZuordnung))
        #         .join(DmGstZuordnung.rel_gst)
        #         .group_by(DmGst.id))
        """"""
        # dmi = session.scalars(stmt).unique().all()
        dmi = self.session.scalars(stmt).all()

        return dmi

    def createFeatureFields(self):

        # k_uuid = GeneralField.Uuid()
        f_id = GeneralField.Id()
        f_type_id = GeneralField.TypeId()
        f_gst = Fields.GstNr()
        f_adresse = Fields.Adresse()
        f_telefon_all = Fields.TelefonAll()
        f_vertreter_id = Fields.VertreterId()

        # self._fields.append(k_uuid)
        self._fields.append(f_id)
        self._fields.append(f_type_id)
        self._fields.append(f_gst)
        self._fields.append(k_adresse)
        self._fields.append(k_telefon_all)
        self._fields.append(k_vertreter_id)

    def setLayer(self):

        # layer = GstZuordLayer(
        #     "Polygon?crs=epsg:31259",
        #     "Grundstücke",
        #     "memory",
        #     fields=self.fields,
        #     data_view=self
        # )
        layer = GstZuordLayer(
            "Polygon?crs=epsg:31259",
            "Grundstücke",
            "memory"
        )
        layer.base = True

        # layer.entity_dialog = GstDialog
        # layer.entity_form = GstZuordnungDataForm
        layer.dmi_list = self.dmi_list

        # setLayerStyle(layer, 'gst_awbuch_status')

        layer.data_provider = layer.dataProvider()

        layer.data_provider.addAttributes(self.fields)
        layer.updateFields()

        return layer

    def getCustomEntityData(self):

        print(f'...')
        """erhalte die dmi-liste mit den gst-awb-statusen von der session
        bei der initialisierung des aktes"""

        self.custom_entity_data['awb_status'] \
            = self.parent._custom_entity_data['gst_awb_status']

        self.custom_entity_data['recht_status'] \
            = self.parent._custom_entity_data['gst_recht_status']

        return self.custom_entity_data

    def setFeaturesFromDmi(self):
        super().setFeaturesFromDmi()

        for dmi in self.dmi_list:

            feat = QgaFeature(self.layer.fields(), self)

            self.setFeatureAttributes(feat, dmi)

            # geom_wkt = to_shape(gst_version.geometry).wkt
            # geom_new = QgsGeometry()
            # geom = geom_new.fromWkt(geom_wkt)
            #
            # feat.setGeometry(geom)

            self.layer.provider.addFeatures([feat])

        # for gst_zuor in self.dmi_list:
        #
        #     for gst_version in gst_zuor.rel_gst.rel_alm_gst_version:
        #
        #         feat = QgaFeature(self.layer.fields(), self)
        #
        #         self.setFeatureAttributes(feat, gst_zuor)
        #
        #         # feat.setAttributes([gst_version.id,
        #         #                     gst_zuor.rel_gst.gst,
        #         #                     gst_version.rel_alm_gst_ez.ez,
        #         #                     gst_version.rel_alm_gst_ez.kgnr,
        #         #                     gst_version.rel_alm_gst_ez.rel_kat_gem.kgname,
        #         #                     gst_zuor.awb_status_id,
        #         #                     gst_zuor.rechtsgrundlage_id,
        #         #                     '',
        #         #                     gst_version.rel_alm_gst_ez.datenstand])
        #
        #         geom_wkt = to_shape(gst_version.geometry).wkt
        #         geom_new = QgsGeometry()
        #         geom = geom_new.fromWkt(geom_wkt)
        #
        #         feat.setGeometry(geom)
        #
        #         self.layer.provider.addFeatures([feat])

    def getFeatureFields(self):
        # super().setFeatureFields()

        # gst_version_id_fld = QgaField("id", QVariant.Int)
        #
        # az_fld = QgaField("az", QVariant.Int)
        # az_fld.setAlias('AZ')
        #
        # akt_name_fld = QgaField("akt_name", QVariant.String)
        # akt_name_fld.setAlias('Aktname')
        #
        # gst_fld = QgaField("gst", QVariant.String)
        # gst_fld.setAlias('Gst')
        #
        # ez_fld = QgaField("ez", QVariant.Int)
        # ez_fld.setAlias('EZ')
        #
        # kgnr_fld = QgaField("kgnr", QVariant.Int)
        # kgnr_fld.setAlias('KG-Nr')
        #
        # kgname_fld = QgaField("kgname", QVariant.String)
        # kgname_fld.setAlias('KG-Name')
        #
        # awb_id_fld = QgaField("awb_id", QVariant.Int)
        #
        # awb_status_fld = QgaField("awb_status", QVariant.String)
        # awb_status_fld.setAlias('AWB-Status')
        #
        # recht_id_fld = QgaField("recht_id", QVariant.Int)
        #
        # recht_status_fld = QgaField("recht_status", QVariant.String)
        # recht_status_fld.setAlias('Rechtsgrundlage')
        #
        # gis_area_fld = QgaField("gis_area", QVariant.Double)
        # gis_area_fld.setAlias('GIS-Fläche')
        #
        # gb_area_fld = QgaField("gb_area", QVariant.Double)
        # gb_area_fld.setAlias('GB-Fläche')
        #
        # bew_area_fld = QgaField("bew_area", QVariant.Double)
        # bew_area_fld.setAlias('beweidet')
        #
        # datenstand_fld = QgaField("datenstand", QVariant.String)
        # datenstand_fld.setAlias('Datenstand')
        #
        # dmi_fld = QgaField("dmi", QVariant.List)
        #
        # self.fields.append(gst_version_id_fld)
        # self.fields.append(az_fld)
        # self.fields.append(akt_name_fld)
        # self.fields.append(gst_fld)
        # self.fields.append(ez_fld)
        # self.fields.append(kgnr_fld)
        # self.fields.append(kgname_fld)
        # self.fields.append(awb_id_fld)
        # self.fields.append(awb_status_fld)
        # self.fields.append(recht_id_fld)
        # self.fields.append(recht_status_fld)
        # self.fields.append(gis_area_fld)
        # self.fields.append(gb_area_fld)
        # self.fields.append(bew_area_fld)
        # self.fields.append(datenstand_fld)
        # self.fields.append(dmi_fld)

        gz_id = GeneralField.Id()
        gz_id.setAlias('gst_zuordnung_id')
        # gz_id.visible = True
        gz_akt_id = GstZuordnungField.AktId()
        gz_akt_name = GstZuordnungField.AktName()
        gz_awb_id = GstZuordnungField.AwbStatusId()
        gz_recht_id = GstZuordnungField.RechtsgrundlageId()
        gz_gb_area = GstZuordnungField.GstLastGbArea()
        gz_koppel_area = GstZuordnungField.GstLastKoppelArea()
        gz_gis_area = GstZuordnungField.GstLastGisArea()

        self.fields.append(gz_id)
        self.fields.append(gz_akt_id)
        self.fields.append(gz_akt_name)
        self.fields.append(gz_awb_id)
        self.fields.append(gz_recht_id)
        self.fields.append(gz_gb_area)
        self.fields.append(gz_koppel_area)
        self.fields.append(gz_gis_area)

        return self.fields

    def setFeatureAttributes(self, feature, dmi):
        super().setFeatureAttributes(feature, dmi)

        for field in self.fields:

            feature[field.name()] = field.getFieldValue(dmi)

        # """last_gst"""
        # gst_versionen_list = dmi.rel_gst.rel_alm_gst_version
        # last_gst = max(gst_versionen_list,
        #                key=attrgetter('rel_alm_gst_ez.datenstand'))
        # """"""
        #
        # """gb_area"""
        # gb_area = 0
        # for nutz in last_gst.rel_alm_gst_nutzung:
        #     gb_area = gb_area + nutz.area
        # """"""
        #
        # """summe der koppel-verschnitt-flächen pro gst"""
        # sum_cut = 0.00
        # for cut in last_gst.rel_cut_koppel_gst:
        #     sum_cut = sum_cut + cut.cut_area
        # """"""
        #
        # feature['id'] = dmi.id
        # feature['az'] = dmi.rel_akt.az
        # feature['akt_name'] = dmi.rel_akt.name
        # feature['gst'] = dmi.rel_gst.gst
        # feature['ez'] = last_gst.rel_alm_gst_ez.ez
        # feature['kgnr'] = dmi.rel_gst.kgnr
        # feature['kgname'] = dmi.rel_gst.rel_kat_gem.kgname
        # feature['awb_id'] = dmi.awb_status_id
        # feature['awb_status'] = dmi.rel_awb_status.name
        # feature['recht_id'] = dmi.rechtsgrundlage_id
        # feature['recht_status'] = dmi.rel_rechtsgrundlage.name
        # feature['gis_area'] = last_gst.gst_gis_area
        # feature['gb_area'] = gb_area
        # feature['bew_area'] = sum_cut
        # feature['datenstand'] = last_gst.rel_alm_gst_ez.datenstand
        # feature['dmi'] = [dmi]

    def changeAttributes(self, feature, dmi):

        """last_gst"""
        gst_versionen_list = dmi.rel_gst.rel_alm_gst_version
        last_gst = max(gst_versionen_list,
                       key=attrgetter('rel_alm_gst_ez.datenstand'))
        """"""

        """gb_area"""
        gb_area = 0
        for nutz in last_gst.rel_alm_gst_nutzung:
            gb_area = gb_area + nutz.area
        """"""

        """summe der koppel-verschnitt-flächen pro gst"""
        sum_cut = 0.00
        for cut in last_gst.rel_cut_koppel_gst:
            sum_cut = sum_cut + cut.cut_area
        """"""

        attrib = {0: dmi.id,
                  1: dmi.rel_akt.az,
                  2: dmi.rel_akt.name,
                  3: dmi.rel_gst.gst,
                  4: last_gst.rel_alm_gst_ez.ez,
                  5: dmi.rel_gst.kgnr,
                  6: dmi.rel_gst.rel_kat_gem.kgname,
                  7: dmi.awb_status_id,
                  8: dmi.rel_awb_status.name,
                  9: dmi.rechtsgrundlage_id,
                  10: dmi.rel_rechtsgrundlage.name,
                  11: last_gst.gst_gis_area,
                  12: gb_area,
                  13: sum_cut,
                  14: last_gst.rel_alm_gst_ez.datenstand,
                  15: [dmi]
                  }

        self.layer.changeAttributeValues(feature.id(),
                                              attrib)

    # def updateFeatureAttributes(self, *args):
    #     super().updateFeatureAttributes(args)
    #
    #     new_dmi = args[0][0]
    #     update_feat = args[0][2]
    #
    #     self.setFeatureAttributes(update_feat, new_dmi)

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
    #
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

        # self.uiAddDataTbtn.clicked.disconnect(self.add_row)
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

        # self.view.setColumnHidden(0, True)
        # self.view.setColumnHidden(7, True)
        # self.view.setColumnHidden(9, True)
        # self.view.setColumnHidden(15, True)

        self.view.sortByColumn(1, Qt.AscendingOrder)

        # self.insertFooterLine('im AWB eingetrage Grundstücksfläche (GB):',
        #                       'ha', 'gb_area', value_width=120,
        #                       factor=0.0001, decimal=4, filter_col='awb_id',
        #                       filter_operator='==', filter_criterion=1)
        # self.insertFooterLine('davon beweidet (GIS)',
        #                       'ha', 'bew_area', value_width=120,
        #                       factor=0.0001, decimal=4)
        # self.insertFooterLine('zugeordnete Grundstücksgesamtfläche (GIS):',
        #                       'ha', 'gis_area', value_width=120,
        #                       factor=0.0001, decimal=4)
        # self.insertFooterLine('zugeordnete Grundstücksgesamtfläche (GB):',
        #                       'ha', 'gb_area', value_width=120,
        #                       factor=0.0001, decimal=4)

        """setzt bestimmte spaltenbreiten"""
        self.view.setColumnWidth(1, 20)
        self.view.setColumnWidth(2, 130)
        self.view.setColumnWidth(3, 50)
        self.view.setColumnWidth(4, 20)
        self.view.setColumnWidth(5, 40)
        self.view.setColumnWidth(6, 100)
        self.view.setColumnWidth(8, 80)
        self.view.setColumnWidth(10, 85)
        self.view.setColumnWidth(11, 75)
        self.view.setColumnWidth(12, 75)
        self.view.setColumnWidth(13, 75)
        """"""

        """passe die Zeilenhöhen an den Inhalt an"""
        # self.view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        """"""

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
#     def __init__(self, parent, dmi_list=None):
#         super(__class__, self).__init__(parent)
#
#         self.dmi_list = dmi_list
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
#         if self.dmi_list:
#             return len(self.dmi_list)
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


class Fields:
    """
    represent the fields according to the data_model 'GstAllTableModel'
    """

    class GstNr(QgaField):

        def __init__(self):
            super().__init__()

            self.name = 'gstnr'
            self.type = QVariant.String

            self.alias = 'Gst-Nr'
            self.dmi_attr = 'gst'