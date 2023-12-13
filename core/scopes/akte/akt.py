import os
import typing
from pathlib import Path

from qgis.PyQt.QtGui import (QFont, QIntValidator, QIcon, QStandardItem, QColor,
                             QStandardItemModel)
from qgis.PyQt.QtWidgets import (QLabel, QSpacerItem, QDockWidget, QToolButton, \
    QMenu, QAction, QTreeView, QHBoxLayout, QComboBox, QAbstractItemView,
                                 QPushButton)
from qgis.PyQt.QtCore import Qt, QSize, QAbstractItemModel, QModelIndex
from geoalchemy2 import functions
from geoalchemy2.shape import to_shape
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsLayoutExporter, QgsFeature, QgsVectorLayer, \
    QgsGeometry, edit, QgsField
from sqlalchemy import desc, select, and_, func
from sqlalchemy.orm import joinedload, contains_eager

from core import entity, db_session_cm
from core.data_model import BAkt, BBearbeitungsstatus, BGisStyle, \
    BGisScopeLayer, BGisStyleLayerVar, BKomplex, BKomplexVersion, BKoppel
from core.gis_control import GisControl
from core.gis_item import GisItem
from core.gis_layer import setLayerStyle
from core.gis_tools import cut_koppel_gstversion
from core.main_gis import MainGis
from core.print_layouts.awb_auszug import AwbAuszug
from core.scopes.akte import akt_UI
from core.scopes.akte.akt_gst_main import GstMaintable
from core.scopes.akte.akt_komplexe_main import KomplexMaintable
from core.scopes.komplex.komplex_item import KomplexItem, KomplexVersionItem
from core.scopes.koppel.koppel_item import KoppelItem


class Akt(akt_UI.Ui_Akt, entity.Entity, GisControl):
    """
    baseclass für einen akt-datensatz
    """

    data_class = BAkt

    _alm_bnr = 0
    _anm = ''
    _az = 0
    _alias = ''
    _name = ''
    _stz = ''
    _status = 0

    _komplex_jahr = 0

    @property  # getter
    def alm_bnr(self):

        if self.uiAlmBnrLedit.text() != '':
            self._alm_bnr = int(self.uiAlmBnrLedit.text())
        else:
            self._alm_bnr = ''
        return self._alm_bnr

    @alm_bnr.setter
    def alm_bnr(self, value):

        if value == 'None' or value == None:
            self._alm_bnr = ''
        else:
            self.uiAlmBnrLedit.setText(str(value))
            self._alm_bnr = value

    @property  # getter
    def alias(self):

        self._alias = self.uiAliasLedit.text()
        return self._alias

    @alias.setter
    def alias(self, value):

        self.uiAliasLedit.setText(value)
        self._alias = value

    @property  # getter
    def anm(self):

        self._anm = self.uiAnmTedit.toPlainText()
        return self._anm

    @anm.setter
    def anm(self, value):

        self.uiAnmTedit.setText(str(value))
        self._anm = value

    @property  # getter
    def az(self):

        return self._az

    @az.setter
    def az(self, value):

        self.uicAzLbl.setText(f'AZ {str(value)}')
        self._az = value

    @property  # getter
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        self.guiHeaderTextLbl.setText(value)
        self._name = value

    @property  # getter
    def status(self):

        self._status = self.uiStatusCombo.currentData(Qt.UserRole)
        return self._status

    @status.setter
    def status(self, value):

        self.uiStatusCombo.setCurrentIndex(
            self.uiStatusCombo.findData(value, Qt.UserRole)
        )
        self._status = value

    @property  # getter
    def stz(self):

        return self._stz

    @stz.setter
    def stz(self, value):

        self.uiStzLbl.setText(value)
        self._stz = value

    @property  # getter
    def komplex_jahr(self):

        self._komplex_jahr = self.uicKkJahrCombo.currentText()

        return self._komplex_jahr

    @komplex_jahr.setter
    def komplex_jahr(self, value):

        self.uicKkJahrCombo.setCurrentText(value)
        self._komplex_jahr = value

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        """erlaube nur integer in uiAlmBnr"""
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 99999999)
        self.uiAlmBnrLedit.setValidator(onlyInt)
        """"""

        """lade die einträge für das status-combo"""
        self.setStatusComboData()
        """"""

        """erzeuge ein main_gis widget und füge es in ein GisDock ein"""
        self.uiGisDock = GisDock(self)
        self.guiMainGis = MainGis(self.uiGisDock, self)
        self.guiMainGis.komplex_jahr = 2018
        self.addDockWidget(Qt.RightDockWidgetArea, self.uiGisDock)
        self.uiGisDock.setWidget(self.guiMainGis)
        """"""

        """setzte den 'scope_id'; damit die richtigen layer aus dem 
        daten_model 'BGisScopeLayer' für dieses main_gis widget geladen werden"""
        self.guiMainGis.scope_id = 1
        """"""

        """definiere notwendige tabellen und füge sie ein"""
        self.gst_table = GstMaintable(self)
        self.uiGstListeVlay.addWidget(self.gst_table)

        # self.komplex_table = KomplexMaintable(self)
        # self.uiKomplexeGisListeVlay.addWidget(self.komplex_table)
        """"""

        """erzeuge ein Layout über dem Komplex-TreeView mit Elementen"""
        self.komplex_tree_header_layer = QHBoxLayout(self)
        self.uicKkJahrLbl = QLabel(self)
        self.uicKkJahrLbl.setText('Jahr:')
        self.uicKkJahrCombo = QComboBox(self)
        self.uicKkJahrComboNew = QComboBox(self)
        space = QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding,
                    QtWidgets.QSizePolicy.Fixed)
        self.uicAddKoppelTbtn = QToolButton(self)
        self.uicAddKoppelTbtn.setIcon(QIcon(":/svg/resources/icons/plus_green.svg"))
        self.uicAddKoppelTbtn.setToolTip('füge eine oder mehrere Koppeln ein')
        self.uicAddKoppelTbtn.setIconSize(QSize(25, 25))
        self.uicAddKoppelTbtn.setPopupMode(QToolButton.InstantPopup)

        self.uicCollapsNodesPbtn = QPushButton(self)
        self.uicCollapsNodesPbtn.setIcon(QIcon(":/svg/resources/icons/treeview_collapse.svg"))
        self.uicCollapsNodesPbtn.setToolTip('alle Knoten einklappen')
        self.uicCollapsNodesPbtn.setIconSize(QSize(25, 25))

        self.uicExpandNodesPbtn = QPushButton(self)
        self.uicExpandNodesPbtn.setIcon(QIcon(":/svg/resources/icons/treeview_expand.svg"))
        self.uicExpandNodesPbtn.setToolTip('alle Knoten ausklappen')
        self.uicExpandNodesPbtn.setIconSize(QSize(25, 25))

        self.actionAddKoppel = QAction(self)
        self.actionAddKoppel.setText('füge eine neue Koppel beim ausgewählten Layer ein')
        self.actionAddKoppelByYear = QAction(self)
        self.actionAddKoppelByYear.setText('kopiere alle Koppeln eines Jahres')

        self.uicAddKoppelMenu = QMenu(self)
        self.uicAddKoppelMenu.addAction(self.actionAddKoppel)
        self.uicAddKoppelMenu.addAction(self.actionAddKoppelByYear)
        self.uicAddKoppelTbtn.setMenu(self.uicAddKoppelMenu)

        self.komplex_tree_header_layer.addWidget(self.uicKkJahrLbl)
        self.komplex_tree_header_layer.addWidget(self.uicKkJahrCombo)
        self.komplex_tree_header_layer.addWidget(self.uicKkJahrComboNew)
        self.komplex_tree_header_layer.addSpacerItem(space)
        self.komplex_tree_header_layer.addWidget(self.uicExpandNodesPbtn)
        self.komplex_tree_header_layer.addWidget(self.uicCollapsNodesPbtn)
        self.komplex_tree_header_layer.addWidget(self.uicAddKoppelTbtn)

        self.uiKomplexeGisListeVlay.addLayout(self.komplex_tree_header_layer)
        """"""

        """erzeuge ein TreeView für Komplexe und Koppeln"""
        self.komplexe_view = QTreeView(self)
        self.komplexe_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.uiKomplexeGisListeVlay.addWidget(self.komplexe_view)
        """"""

        """erzeuge einen neuen TreeView für die neue Item-basierte Layererstellung"""
        self.komplexe_view_new = QTreeView(self)
        # self.komplexe_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.uiKomplexeGisListeVlay.addWidget(self.komplexe_view_new)
        """"""

        # """erzeuge ein selection-model für das tree-view"""
        # self.tree_selection_model = self.komplexe_view.selectionModel()
        # """"""

        """erzeuge einen Layer für die Koppeln und füge ihn ins canvas ein"""
        self.koppel_layer = QgsVectorLayer("Polygon?crs=epsg:31259",
                                           "Koppeln",
                                           "memory")
        self.koppel_dp = self.koppel_layer.dataProvider()

        # add fields
        self.koppel_dp.addAttributes([QgsField("id", QVariant.Int),
                                      QgsField("name", QVariant.String),
                                      QgsField("bearbeiter", QVariant.String),
                                      QgsField("aw_ha", QVariant.String),
                                      QgsField("aw_proz", QVariant.String),
                                      QgsField("area", QVariant.String)])

        self.koppel_layer.updateFields()  # tell the vector layer to fetch changes from the provider

        self.koppel_layer.back = False
        self.koppel_layer.base = True
        setLayerStyle(self.koppel_layer, 'koppel_gelb')
        self.guiMainGis.addLayer(self.koppel_layer)
        """"""

        """erzeuge einen Layer für die Koppeln und füge ihn ins canvas ein"""
        self.koppel_layer_new = QgsVectorLayer("Polygon?crs=epsg:31259",
                                           "Koppeln",
                                           "memory")
        self.koppel_dp_new = self.koppel_layer_new.dataProvider()

        # add fields
        self.koppel_dp_new.addAttributes([QgsField("id", QVariant.Int),
                                      QgsField("name", QVariant.String),
                                      QgsField("bearbeiter", QVariant.String),
                                      QgsField("aw_ha", QVariant.String),
                                      QgsField("aw_proz", QVariant.String),
                                      QgsField("area", QVariant.String)])

        self.koppel_layer_new.updateFields()  # tell the vector layer to fetch changes from the provider

        self.koppel_layer_new.back = False
        self.koppel_layer_new.base = True
        setLayerStyle(self.koppel_layer_new, 'koppel_gelb')
        self.guiMainGis.addLayer(self.koppel_layer_new)
        """"""

        """erzeuge einen Layer für die Komplexe und füge ihn ins canvas ein"""
        self.komplex_layer = QgsVectorLayer("Polygon?crs=epsg:31259",
                                            "Komplexe",
                                            "memory")
        self.komplex_dp = self.komplex_layer.dataProvider()
        self.komplex_layer.back = False
        self.komplex_layer.base = True
        setLayerStyle(self.komplex_layer, 'komplex_rot')
        self.guiMainGis.addLayer(self.komplex_layer)
        """"""

    def initUi(self):
        super().initUi()



    def finalInit(self):
        super().finalInit()

        """stetze eine minimum widget-größe"""
        self.setMinimumWidth(1800)
        self.setMinimumHeight(900)
        """"""

        """stelle eine relation von gis-layern und datentabellen her und
        aktiviere die überwachung dieser relation"""
        # self.linked_gis_widgets[99] = self.gst_table
        # self.linked_gis_widgets[104] = self.komplex_table
        # self.activateGisControl()
        """"""

    def mapData(self):
        super().mapData()

        self.name = self.data_instance.name
        self.az = self.data_instance.az
        self.stz = self.data_instance.stz

        self.alias = self.data_instance.alias
        self.alm_bnr = self.data_instance.alm_bnr
        self.anm = self.data_instance.anm
        self.status = self.data_instance.bearbeitungsstatus_id

        self.guiMainGis.entity_id = self.data_instance.id

        # self.loadGisLayer()

    def loadSubWidgets(self):
        super().loadSubWidgets()

        self.gst_table.initMaintable(self.session)
        # self.komplex_table.initMaintable(self.session)

        self.setJahrCombo(self.session)
        self.loadKKTree()

        self.loadKKGis()

        self.loadGisLayer()  # lade layer die in der db definiert sind

    def loadKKTree(self):
        """
        lade die Elemente des Komplex/Koppel TreeView's
        :param session:
        :return:
        """

        self.komplex_model = KomplexModel()
        self.komplex_root_item = self.komplex_model.invisibleRootItem()

        """entferne alle features vom layer Koppeln"""
        with edit(self.koppel_layer):
            listOfIds = [feat.id() for feat in self.koppel_layer.getFeatures()]
            self.koppel_layer.deleteFeatures(listOfIds)
        """"""

        """entferne alle features vom layer Komplexe"""
        with edit(self.komplex_layer):
            listOfIds = [feat.id() for feat in self.komplex_layer.getFeatures()]
            self.komplex_layer.deleteFeatures(listOfIds)
        """"""

        with (self.session):

            komplex_inst = self.session.scalars(select(BKomplex)
                                    .join(BKomplex.rel_komplex_version)
                                    .where(and_((BKomplexVersion.jahr == int(self.uicKkJahrCombo.currentText())),
                                                (BKomplex.akt_id == self.data_instance.id)))
                                    .options(contains_eager(BKomplex.rel_komplex_version)))\
                .unique().all()
            #################################

            komplex_inst_new = self.session.scalars(select(BKomplexVersion)
                                    .where(BKomplexVersion.akt_id == self.data_instance.id)
                                    .order_by(desc(BKomplexVersion.jahr))
                                                    ).unique().all()

            self.komplex_years = {}

            for komplex_version in komplex_inst_new:

                komplex_item = KomplexVersionItem(komplex_version)

                if komplex_version.jahr not in self.komplex_years:

                    year_item = QStandardItem()
                    year_item.setData(komplex_version.jahr, Qt.DisplayRole)
                    year_item.setData(komplex_version.jahr, Qt.EditRole)

                    year_item.appendRow(komplex_item)

                    self.komplex_years[komplex_version.jahr] = year_item
                    self.komplex_root_item.appendRow(year_item)

                else:
                    self.komplex_years[komplex_version.jahr].appendRow(komplex_item)

                for koppel in komplex_version.rel_koppel:

                    koppel_item = KoppelItem(koppel)
                    komplex_item.appendRow([koppel_item, None, None, None])

                    """erzeuge das Koppel-Feature"""
                    koppel_feat = QgsFeature(self.koppel_layer_new.fields())
                    koppel_feat.setAttributes([koppel_item.data(GisItem.Name_Role), None])
                    koppel_feat.setGeometry(QgsGeometry.fromWkt(
                        to_shape(koppel_item.data(GisItem.Geometry_Role)).wkt)
                    )
                    (result, added_kop_feat) = self.koppel_dp_new.addFeatures([koppel_feat])
                    koppel_item.setData(added_kop_feat[0], GisItem.Feature_Role)
                    """"""

            # for komp in komplex_inst:
            #
            #     komplex_item = KomplexItem(komp)
            #     self.komplex_root_item.appendRow(komplex_item)
            #
            #     for kop in komp.rel_komplex_version[0].rel_koppel:
            #
            #         koppel_item = KoppelItem(kop)
            #         koppel_item.id = kop.id
            #         komplex_item.appendRow([koppel_item, None, None, None])
            #
            self.komplexe_view_new.setModel(self.komplex_model)
            self.uiVersionTv.setModel(self.komplex_model)
            self.uiKKTv.setModel(self.komplex_model)

            self.uicKkJahrComboNew.setModel(self.komplex_model)

            print(f'***')
            #
            # self.koppel_features_new = []
            # self.koppel_list = []
            # for kx in range(self.komplex_root_item.rowCount()):
            #
            #     komplex = self.komplex_root_item.child(kx)
            #     for ko in range(komplex.rowCount()):
            #         koppel = komplex.child(ko)
            #         self.koppel_list.append(koppel)
            #         # kop_feat = QgsFeature(self.koppel_layer_new.fields())
            #         # kop_feat.setAttributes([koppel.data(GisItem.Name_Role), None])
            #         # kop_feat.setGeometry(QgsGeometry.fromWkt(to_shape(koppel.data(GisItem.Geometry_Role)).wkt))
            #         # koppel.setData(kop_feat, GisItem.Feature_Role)
            #         # self.koppel_features_new.append(kop_feat)
            #
            # for koo in self.koppel_list:
            #     kop_feat = QgsFeature(self.koppel_layer_new.fields())
            #     kop_feat.setAttributes([koo.data(GisItem.Name_Role)])
            #     kop_feat.setGeometry(QgsGeometry.fromWkt(to_shape(koo.data(GisItem.Geometry_Role)).wkt))
            #     # self.koppel_features_new.append(kop_feat)
            #
            #     (result, added_kop_feat) = self.koppel_dp_new.addFeatures([kop_feat])
            #     koo.setData(added_kop_feat[0], GisItem.Feature_Role)
            #
            # self.koppel_layer_new.setName(f'Koppeln neu')
            #
            # for f in self.koppel_layer_new.getFeatures():
            #     print(f'new feature.id(): {f.id()} - [id]: {f["id"]}')
            ####################################

            self.kk_tree_model = KKTreeModel(self, komplex_inst)
            self.komplexe_view.setModel(self.kk_tree_model)
            self.komplexe_view.expandAll()

            """erzeuge ein selection-model für das tree-view"""
            self.kk_selection_model = self.komplexe_view_new.selectionModel()
            self.komplexe_view_new.setSelectionMode(
                QAbstractItemView.ExtendedSelection)
            """"""

            """erzeuge ein selection-model für das tree-view"""
            self.tree_selection_model = self.komplexe_view.selectionModel()
            self.komplexe_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
            """"""

            self.komplex_features = []
            self.koppel_features = []

            """iter durch die abgefragten komplexe und lege diese an"""
            for komplex in komplex_inst:
                new_komp_feat = QgsFeature()
                new_komp_feat.setAttributes \
                    ([komplex.id, komplex.name])

                """iter durch die koppeln, lege diese an"""
                for koppel in komplex.rel_komplex_version[0].rel_koppel:
                    new_kopp_feat = QgsFeature(self.koppel_layer.fields())
                    new_kopp_feat.setAttributes \
                        ([koppel.id, koppel.name, None, None, None, '0,123'])
                    new_kopp_feat.setGeometry(
                        QgsGeometry.fromWkt(to_shape(koppel.geometry).wkt))
                    self.koppel_features.append(new_kopp_feat)
                """"""

                """erzeuge einen Komplex aus den Koppeln"""
                new_komp_geom = self.koppel_features[0].geometry()
                for i in range(len(self.koppel_features) - 1):
                    new_komp_geom = self.koppel_features[i+1].geometry().combine(new_komp_geom)
                """"""

                new_komp_feat.setGeometry(new_komp_geom)
                self.komplex_features.append(new_komp_feat)

        (res, kop_feat) = self.koppel_dp.addFeatures(self.koppel_features)
        self.koppel_layer.setName(f'Koppeln {self.uicKkJahrCombo.currentText()}')

        for f in self.koppel_layer.getFeatures():
            print(f'feature.id(): {f.id()} - [id]: {f["id"]}')


        self.komplex_dp.addFeatures(self.komplex_features)
        self.komplex_layer.setName(
            f'Komplexe {self.uicKkJahrCombo.currentText()}')

        extent = self.komplex_layer.extent()
        self.guiMainGis.uiCanvas.setExtent(extent)

    def changedYear(self, index):

        print(f'index: {index}')
        self.loadKKGis()

    def loadKKGis(self):

        with edit(self.koppel_layer_new):
            listOfIds = [feat.id() for feat in self.koppel_layer_new.getFeatures()]
            self.koppel_layer_new.deleteFeatures(listOfIds)

        year = self.uicKkJahrComboNew.currentText()

        found_year = self.komplex_model.findItems(year)

        for kom in range(found_year[0].rowCount()):

            komplex = found_year[0].child(kom)
            for ko in range(komplex.rowCount()):
                koppel = komplex.child(ko)
                koppel_feat = koppel.data(GisItem.Feature_Role)
                (result, added_kop_feat) = self.koppel_dp_new.addFeatures(
                    [koppel_feat])
                koppel.setData(added_kop_feat[0], GisItem.Feature_Role)

        # for y in range(self.komplex_root_item.rowCount()):
        #
        #     year_item = self.komplex_root_item.child(y)
        #     year = year_item.data(Qt.DisplayRole)
        #
        #     if str(year) == self.uicKkJahrCombo.currentText():
        #
        #         for kom in range(year_item.rowCount()):
        #
        #             komplex_item = year_item.child(kom)
        #             for ko in range(komplex_item.rowCount()):
        #
        #                 koppel_item = komplex_item.child(ko)
        #
        #                 koppel_feat = QgsFeature(self.koppel_layer_new.fields())
        #                 koppel_feat.setAttributes([koppel_item.data(GisItem.Name_Role), None])
        #                 koppel_feat.setGeometry(QgsGeometry.fromWkt(
        #                     to_shape(koppel_item.data(GisItem.Geometry_Role)).wkt))
        #                 (result, added_kop_feat) = self.koppel_dp_new.addFeatures([koppel_feat])
        #                 koppel_item.setData(added_kop_feat[0], GisItem.Feature_Role)
        #                 print(f'***')

        self.koppel_layer_new.setName(f'Koppeln neu ' + self.uicKkJahrCombo.currentText())

    def setJahrCombo(self, session):

        with session:

            jahre_query = session.execute(select(BKomplexVersion.jahr)
                                          .join(BKomplexVersion.rel_komplex)
                                          .where(
                BKomplex.akt_id == self.data_instance.id)
                                          .group_by(BKomplexVersion.jahr)).all()

            jahre_list = [i[0] for i in jahre_query]

            for jahr in sorted(jahre_list, reverse=True):
                self.uicKkJahrCombo.addItem(str(jahr))

    def loadGisLayer(self):
        """hole die infos der zu ladenden gis-layer aus der datenbank und
        übergebe sie dem main_gis widget"""

        """setzte den base_id für das main_gis widget"""
        self.guiMainGis.base_id = self.entity_id
        """"""

        """hole die daten für die gis-layer aus der datenbank"""
        with db_session_cm() as session:
            session.expire_on_commit = False

            akt_gis_scope_layer = session.query(BGisScopeLayer)\
                .join(BGisStyle) \
                .outerjoin(BGisStyleLayerVar) \
                .filter(BGisScopeLayer.gis_scope_id == self.guiMainGis.scope_id)\
                .order_by(desc(BGisScopeLayer.order))\
                .all()
        """"""

        """lade die gis-layer"""
        self.guiMainGis.loadLayer(akt_gis_scope_layer)

    def submitEntity(self):

        self.data_instance.alias = self.alias
        self.data_instance.alm_bnr = self.alm_bnr
        self.data_instance.anm = self.anm
        self.data_instance.bearbeitungsstatus_id = self.status

        super().submitEntity()

    def post_data_set(self):
        super().post_data_set()

        self.uiGisDock.setWindowTitle(
            f'Kartenansicht {self.name} (AZ {str(self.az)})')

        self.tool_menu = QMenu(self)
        self.uicEntityTools.setMenu(self.tool_menu)

        self.menu_prints = QMenu('Ausdrucke')
        self.tool_menu.addMenu(self.menu_prints)

        self.actionPrintAWB = QAction('NÖ Alm- und Weidebuch Auszug')
        self.menu_prints.addAction(self.actionPrintAWB)

        self.actionPrintAktInfo = QAction('allgemeine Akteninformation')
        self.menu_prints.addAction(self.actionPrintAktInfo)
        self.actionPrintAktInfo.setEnabled(False)

        self.actionPrintGstList = QAction('Grundstücksliste')
        self.menu_prints.addAction(self.actionPrintGstList)
        self.actionPrintGstList.setEnabled(False)

    def insertEntityHeader(self):
        super().insertEntityHeader()

        self.uicAzLbl = QLabel(self)
        az_label_font = QFont("Verdana", 10, QFont.Bold)
        self.uicAzLbl.setStyleSheet(self.header_label_style)
        self.uicAzLbl.setFont(az_label_font)
        spacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Minimum)
        self.uiHeaderHlay.addItem(spacer)
        self.uiHeaderHlay.insertWidget(2, self.uicAzLbl)

        self.uicEntityTools = QToolButton(self)
        self.uicEntityTools.setIcon(
            QIcon(':/svg/resources/icons/hamburger.svg'))
        self.uicEntityTools.setIconSize(QSize(30, 30))
        self.uicEntityTools.setFocusPolicy(Qt.NoFocus)
        self.uicEntityTools.setPopupMode(QToolButton.InstantPopup)
        self.uiHeaderMainHlay.insertWidget(1, self.uicEntityTools)

    def setStatusComboData(self):
        """
        hole die daten für die status-combobox aus der datenbank und füge sie in
        die combobox ein
        """

        with db_session_cm() as session:
            status_items = session.query(BBearbeitungsstatus).\
                order_by(BBearbeitungsstatus.sort).\
                all()

        for item in status_items:
            self.uiStatusCombo.addItem(item.name, item.id)

    def signals(self):
        super().signals()

        self.uiGisDock.topLevelChanged.connect(self.changedGisDockLevel)
        self.actionPrintAWB.triggered.connect(self.createAwbPrint)

        self.uicKkJahrCombo.currentIndexChanged.connect(self.loadKKTree)

        # self.komplexe_view.clicked.connect(self.clickedTreeElement)
        self.tree_selection_model.selectionChanged.connect(self.treeselectionChanged)

        self.uicCollapsNodesPbtn.clicked.connect(self.collapsKKTree)
        self.uicExpandNodesPbtn.clicked.connect(self.expandKKTree)

        # self.kk_selection_model.selectionChanged.connect(
        #     self.selectionChangedTreeNew)

        self.uicKkJahrComboNew.currentIndexChanged.connect(self.changedYear)

        self.uiVersionTv.selectionModel().selectionChanged.connect(
            self.selectedVersionChanged)

    def collapsKKTree(self):

        self.komplexe_view_new.collapseAll()

    def expandKKTree(self):

        self.komplexe_view_new.expandAll()

    def selectedVersionChanged(self, selected):

        self._selected_version_index = selected[0].indexes()[0]
        self._selected_version_item = self.uiVersionTv.model()\
            .itemFromIndex(self._selected_version_index)

        # self.uiVersionNrLbl.setText(
        #     self._selected_version_item.data(TreeItem.Code_Role))

        self.setKKTv(self._selected_version_index)

    def setKKTv(self, index):

        self.uiKKTv.setModel(self.komplex_model)
        self.uiKKTv.expandAll()
        # self.uiKKTv.setColumnWidth(0, 200)

        self.uiKKTv.setRootIndex(index)

    def selectionChangedTreeNew(self, tree_selection):

        print(f'kk selection changed!!')
        print(f'index: {tree_selection}')

        # for idx in tree_selection.indexes():
        #
        #     item = self.komplex_model.itemFromIndex(idx)
        #
        #     print(f'{item.data(GisItem.Name_Role)}')

        feature_id_list = []
        sel_item = []

        for idx in self.kk_selection_model.selectedIndexes():
            if idx.column() == 0:  # wähle nur indexe der ersten spalte!

                item = self.komplex_model.itemFromIndex(idx)
                sel_item.append(item)
                feature_id_list.append(item.data(GisItem.Feature_Role).id())

                # print(f':: {item.data(GisItem.Name_Role)}')
            # self.komplex_model.itemFromIndex(
            #     self.kk_selection_model.selectedIndexes()[0]).data(
            #     GisItem.Feature_Role).id()

        print(f'feature_ids:')
        for ii in sel_item:
            print(f'name: {ii.data(GisItem.Name_Role)}  id: {ii.data(GisItem.Feature_Role)}')
        print(f'fffffffffffffffffffffff')

        self.guiMainGis.layer_tree_view.setCurrentLayer(self.koppel_layer_new)
        self.selectFeaturesNew([s.data(GisItem.Feature_Role).id() for s in sel_item])

    def treeselectionChanged(self, tree_selection):

        print(f'index: {tree_selection}')

        sel_ids = []

        for s in self.tree_selection_model.selectedIndexes():
            if s.column() == 0:
                kop_id = self.komplexe_view.model().getItem(s).data_instance.id
                print(f'koppel: {kop_id}')
                sel_ids.append(kop_id)

        self.guiMainGis.layer_tree_view.setCurrentLayer(self.koppel_layer)
        self.setSelectFeature(sel_ids)

    # def selectLayer(self, layer_id, feature_ids):
    #
    #     for layer in self.project_instance.mapLayers().values():
    #
    #         if layer_id == layer.style_id:
    #             self.layer_tree_view.setCurrentLayer(layer)
    #             self.setSelectFeature(feature_ids)
    #
    def selectFeaturesNew(self, feat_id_list):

        self.guiMainGis.removeSelectedAll()
        curr_layer = self.guiMainGis.layer_tree_view.currentLayer()

        # curr_layer.select(feat_id_list.id())
        # curr_layer.select([f.id() for f in curr_layer.getFeatures() if
        #                    f['id'] in feat_id_list])
        curr_layer.select([f.id() for f in curr_layer.getFeatures() if f.id()
                           in feat_id_list])

    def setSelectFeature(self, feature_ids):
        """
        select features
        :param feature_ids:
        :return:
        """

        self.guiMainGis.removeSelectedAll()

        print(f'tuple(feature_ids): {tuple(feature_ids)}')

        # self.guiMainGis.layer_tree_view.currentLayer().select([1])
        # self.guiMainGis.layer_tree_view.currentLayer().selectByExpression(f'"id" in {tuple(feature_ids)}')
        # self.guiMainGis.layer_tree_view.currentLayer().selectByExpression(f'"id" in (492)')

        curr_layer = self.guiMainGis.layer_tree_view.currentLayer()
        curr_layer.select([f.id() for f in curr_layer.getFeatures() if f['id'] in feature_ids])

        # for i in tree_selection:
        #     print(f'i: {i}')
        #     kop_id = self.komplexe_view.model().getItem(i.indexes()[0]).data_instance
        #     print(f'koppel: {kop_id}')


        # print(f'index: {self.komplexe_view.model().getItem(index).data_instance}')
        #
        # kop_id = self.komplexe_view.model().getItem(index).data_instance.id
        #
        # self.gst_layer.select([kop_id])
        # self.gst_layer.selectByExpression(f'"id"={str(kop_id)}')


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

    def createAwbPrint(self):
        """
        erzeuge einen ausdruck mit den grundstücken dieses aktes die im
        alm- und weidebuch eingetragen sind inkl. einer karte dieser
        grundstücke
        """


        awb_auszug = AwbAuszug(akt_instance=self.data_instance)
        print(f'create AWB')

        """erzeuge eine pdf-Datei"""
        exporter = QgsLayoutExporter(awb_auszug)
        pdf_settings = exporter.PdfExportSettings()
        pdf_file = str(Path().absolute().joinpath('data', '__AWB-Auszug.pdf'))
        exporter.exportToPdf(pdf_file, pdf_settings)
        """"""

        """öffne die pdf datei"""
        os.startfile(pdf_file)
        """"""

    def onGisEdit(self):
        """
        führe diese methode aus, wenn ein feature hinzugefügt oder verändert
        wird
        """

        # self.komplex_table.updateMaintable()
        self.gst_table.updateMaintable()

    def updateAkt(self):

        """führe den verschnitt komplexe und gst-version durch"""
        cut_koppel_gstversion()
        """"""

        """update canvas"""
        self.guiMainGis.uiCanvas.update()
        self.guiMainGis.uiCanvas.refresh()
        """"""

        """aktualisiere die tabellen"""
        # self.komplex_table.updateMaintable()
        self.gst_table.updateMaintable()
        """"""


class GisDock(QDockWidget):
    """
    baseclass für das GisDock in der klasse 'Akt'
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.setWindowTitle('Kartenansicht')


class KomplexModel(QStandardItemModel):

    def __init__(self, parent=None) -> None:
        super(KomplexModel, self).__init__(parent)

        self.parent = parent

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['Komplex/Koppel', '2', '3', 'Fläche'])
        # self.setItemPrototype(KomplexItem())

    def data(self, index: QModelIndex, role: int = ...):

        item = self.itemFromIndex(index)

        """get the item of the first column if you are in an other"""
        if index.column() != 0:
            first_index = index.sibling(index.row(), 0)
            first_item = self.itemFromIndex(first_index)
        """"""

        # if role == TreeItem.Name_Role:
        #     print(f'--->  name')

        if not index.isValid():
            return None

        if index.column() == 0:

            # if role == Qt.DecorationRole:
            #     return item.data(TreeItem.Color_Role)

            # if type(item) == TreeItemCollection:

            # if role == Qt.EditRole:
            #     return item.data(TreeItem.Name_Role)

            if role == Qt.DisplayRole:

                if type(item) == QStandardItem:
                    return item.data(Qt.DisplayRole)
                else:
                    return item.data(GisItem.Name_Role)

            if role == Qt.DecorationRole:
                return item.data(GisItem.Color_Role)

        if index.column() == 1:

            if role == Qt.DisplayRole:
                return first_item.data(GisItem.Nr_Role)
                # return 'gg'

        if index.column() == 2:
            pass

        if index.column() == 3:

            if role == Qt.DisplayRole:

                if type(first_item) == KoppelItem:
                    k_area = to_shape(first_item.data(GisItem.Instance_Role).geometry).area
                    k_area_rounded = '{:.4f}'.format(
                        round(float(k_area) / 10000, 4)).replace(".", ",")

                    return f'{str(k_area_rounded)} ha'

                if type(first_item) == KomplexItem:
                    komp_area = 0.00
                    for k in range(first_item.rowCount()):
                        kop_area = to_shape(first_item.child(k).data(GisItem.Instance_Role).geometry).area
                        komp_area = komp_area + kop_area

                    komp_area_rounded = '{:.4f}'.format(
                        round(float(komp_area) / 10000, 4)).replace(".", ",")

                    return f'{str(komp_area_rounded)} ha'

        return QStandardItemModel.data(self, index, role)


class KKTreeModel(QAbstractItemModel):

    def __init__(self, parent, komplex_instances) -> None:
        super(KKTreeModel, self).__init__(parent)

        self.rootItem = KKTreeItem()

        self.appendChildItems(self.rootItem, komplex_instances)

        # self.addElement(self.rootItem, instance_list)
    def appendChildItems(self, parent_item, komplexe):

        for komplex in komplexe:
            tree_item = KKTreeItem(data=komplex)
            parent_item.appendRow(tree_item)

            if komplex.rel_komplex_version != []:

                # for komplex_v in komplex.rel_komplex_version:
                #     kv = KKTreeItem(data=komplex_v)
                #     tree_item.appendRow(kv)

                if komplex.rel_komplex_version[0].rel_koppel != []:

                    for koppel in komplex.rel_komplex_version[0].rel_koppel:
                        kop = KKTreeItem(data=koppel)
                        tree_item.appendRow(kop)

            # if instance.children != []:
            #     self.appendChildItems(tree_item, instance.children)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 6

    def rowCount(self, parent: QModelIndex = ...) -> int:

        parent_item = self.getItem(parent)
        return parent_item.rowCount()


    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        item = self.getItem(index)

        if not index.isValid():
            return None

        if role == Qt.DisplayRole and index.column() == 0:
            print('..')
            if type(item.data_instance) == BKomplex:
                return item.data_instance.name
            # if type(item.data_instance) == BKomplexVersion:
            #     return item.data_instance.jahr
            if type(item.data_instance) == BKoppel:
                if item.data_instance.nr:
                    nr = str(item.data_instance.nr)
                else:
                    nr = '-'
                if item.data_instance.name:
                    name = item.data_instance.name
                else:
                    name = '---'
                return nr + ' ' + name

        if role == Qt.DisplayRole and index.column() == 1:
            if type(item.data_instance) == BKoppel:
                return item.data_instance.nr

        if role == Qt.DisplayRole and index.column() == 2:
            if type(item.data_instance) == BKoppel:
                if item.data_instance.bearbeiter == '':
                    return 'n.b.'
                else:
                    return item.data_instance.bearbeiter

        if role == Qt.DisplayRole and index.column() == 5:
            if type(item.data_instance) == BKoppel:
                k_area = to_shape(item.data_instance.geometry).area
                k_area_rounded = '{:.4f}'.format(
                            round(float(k_area) / 10000, 4)).replace(".", ",")

                return f'{str(k_area_rounded)} ha'
                # return '1,23'

        if role == Qt.TextAlignmentRole and index.column() == 5:
            return Qt.AlignRight | Qt.AlignVCenter

        # try:
        # if role == Qt.DisplayRole:
        #     print('...')
        #     if index.column() == 0:
        #         return item.name + '---'
        #     else:
        #         return item.data(index.column())

        if role == Qt.DecorationRole:

            if index.column() == 0:

                if type(item.data_instance) == BKomplex:
                    return QColor(210, 95, 70)  # rot
                if type(item.data_instance) == BKoppel:
                    return QColor(245, 215, 20)  # gelb

        # if role == Qt.DecorationRole:
        #     if not item.hasChildren():
        #         return QColor(245, 210, 45)  # yellow
        #     elif item.hasChildren():
        #         itemlist = ''
        #         for r in range(item.rowCount()):
        #             if item.child(r).hasChildren():
        #                 itemlist += 'g'
        #             if not item.child(r).hasChildren():
        #                 itemlist += 'i'
        #
        #         if 'g' in itemlist and 'i' in itemlist:
        #                 return QColor(210, 95, 70)  # red
        #         else:
        #             return QColor(110, 160, 10)  # green
        #     return QColor(130, 185, 230)  # blue
        #
        # if role == Qt.ForegroundRole:
        #     return item.color
        # if role == Qt.FontRole:
        #     return item.fnt

        if role == KKTreeItem.INSTANCE_ROLE:
            return item.data_instance

        if role == KKTreeItem.ITEM_ROLE:
            return item
        # except:
        #     pass

        return None

    def setData(self, index, value, role=Qt.EditRole):
        """
        :param index: QModelIndex
        :param value: QVariant
        :param role: int (flag)
        :return: bool
        """
        if index.isValid():
            # if role == Qt.DecorationRole:
            #     self.dataChanged.emit(index, index)  # <---
            #     return True
            if role == Qt.EditRole:
                # item = index.internalPointer()
                item = self.data(index, KKTreeItem.ITEM_ROLE)
                item.name = value
                self.dataChanged.emit(index, index)  # <---
                return True

        return False

    def index(self, row, column, parent=QModelIndex()):

        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def getItem(self, index):
        """
        get the instance of the item of the given index (e.g. the instance of
        the class 'KKTreeItem')
        :param index:
        :return: instance of the item
        """
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def flags(self, index):

        item = self.getItem(index)

        """Komplexe sollen nicht ausgewählt werden können"""
        if type(item.data_instance) == BKomplex:
            return Qt.ItemIsEnabled
        """"""

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        # return self.createIndex(parentItem.childNumber(), 0, parentItem)
        return self.createIndex(parentItem.row(), 0, parentItem)

    def insertRowsAdd(self, row: int, count: int,
                   parent: QModelIndex = ...) -> bool:

        self.beginInsertRows(parent, row, count)

        new_inst = BFarmitem()
        new_inst.name = 'fff'

        new_item = KKTreeItem(new_inst.name, instance=new_inst)

        parent_item = self.data(parent, KKTreeItem.ITEM_ROLE)  # parent is the selected index

        parent_item.appendRow([new_item])

        self.endInsertRows()

        return True

    def insertRowsInclude(self, row: int, count: int,
                   parent: QModelIndex = ...) -> bool:

        self.beginInsertRows(parent, row, count)

        new_inst = BFarmitem()
        new_inst.name = 'zzzz'

        new_item = KKTreeItem(new_inst.name, instance=new_inst)

        parent_item = self.data(parent, KKTreeItem.ITEM_ROLE)  # parent is the selected index

        if parent_item.hasChildren():
            print(f'has children!!!')
            for cld in range(parent_item.rowCount()):
                old_chld = parent_item.takeChild(cld, 0)
                new_item.insertRow(0, old_chld)

        parent_item.appendRow([new_item])

        self.endInsertRows()

        self.layoutChanged.emit()

        return True


class KKTreeItem(QStandardItem):

    ITEM_ROLE = Qt.UserRole + 1
    INSTANCE_ROLE = Qt.UserRole + 2

    def __init__(self, name='', font_size=10, set_bold=False,
                 color=QColor(0, 0, 0), data=None):
        super().__init__()

        self.name = name
        self.data_instance = data
        self.color = color
        self.set_bold = set_bold

        self.fnt = QFont('Open Sans', font_size)
        self.fnt.setBold(set_bold)

        # self.setEditable(False)
        # self.setForeground(color)
        # self.setFont(fnt)
        # self.setText(txt)
        # self.setData(data, self.INSTANCE_ROLE)

    def childCount(self):
        return self.rowCount()
