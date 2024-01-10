import os
from pathlib import Path

from qgis.PyQt.QtGui import (QFont, QIntValidator, QIcon, QStandardItem, QColor,
                             QStandardItemModel)
from qgis.PyQt.QtWidgets import (QLabel, QSpacerItem, QDockWidget, QToolButton, \
    QMenu, QAction, QTreeView, QHBoxLayout, QComboBox, QAbstractItemView,
                                 QPushButton)
from qgis.PyQt.QtCore import Qt, QSize, QAbstractItemModel, QModelIndex
from geoalchemy2.shape import to_shape
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsLayoutExporter, QgsFeature, QgsVectorLayer, \
    QgsGeometry, edit, QgsField
from sqlalchemy import desc, select, text
from sqlalchemy.orm import joinedload

from core import entity, db_session_cm
from core.data_model import BAkt, BBearbeitungsstatus, BGisStyle, \
    BGisScopeLayer, BGisStyleLayerVar, BAbgrenzung, BKomplex, BKoppel
from core.gis_control import GisControl
from core.gis_item import GisItem
from core.gis_layer import setLayerStyle, KoppelLayer, KomplexLayer
from core.gis_tools import cut_koppel_gstversion
from core.main_gis import MainGis
from core.print_layouts.awb_auszug import AwbAuszug
from core.scopes.akte import akt_UI
from core.scopes.akte.akt_gst_main import GstMaintable
from core.scopes.komplex.komplex_item import KomplexItem, AbgrenzungItem
from core.scopes.koppel.koppel_item import KoppelItem

import resources_rc

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
        """"""

        self.komplex_model = KomplexModel()
        self.komplex_root_item = self.komplex_model.invisibleRootItem()

        # """erzeuge einen Layer für die Koppeln und füge ihn ins canvas ein"""
        # self.koppel_layer_new = KoppelLayer("Polygon?crs=epsg:31259",
        #                                     "Koppeln new1",
        #                                     "memory"
        #                                     )
        # self.guiMainGis.addLayer(self.koppel_layer_new)
        # """"""

        self.title_lbl = QLabel()
        self.title_lbl.setText('ttttttttttttttttt')

        self.uiTitleToolBar.addWidget(self.title_lbl)

    def initUi(self):
        super().initUi()

    def finalInit(self):
        super().finalInit()

        """stetze eine minimum widget-größe"""
        self.setMinimumWidth(1800)
        self.setMinimumHeight(900)
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

    def loadSubWidgets(self):
        super().loadSubWidgets()

        self.initGis()

        self.gst_table.initMaintable(self.session)

        self.loadKKTreeNew()

        self.loadGisLayer()  # lade layer die in der db definiert sind

    def initGis(self):

        self.kk_gis_group = self.guiMainGis.layer_tree_root.addGroup(
            'sonstige Komplexe und Koppeln')
        self.kk_gis_group.setItemVisibilityChecked(False)

    def updateKomplexe(self):
        """
        temporäre und nur einmal verwendete funktion für zum aktualisieren
        der neuen Tabellenstruktur
        :return:
        """
        alm_new = []

        with db_session_cm() as session:

            akt_instances = session.scalars(select(BAkt)
                                            .options(joinedload(BAkt.rel_abgrenzung)
                                                     .joinedload(BAbgrenzung.rel_komplex)
                                                     .joinedload(BKomplex.rel_koppel))
                                            ).unique().all()

            for akt in akt_instances:
                akt_new = BAkt(name=akt.name,
                               alias=akt.alias,
                               az=akt.az,
                               bearbeitungsstatus_id=akt.bearbeitungsstatus_id,
                               alm_bnr=akt.alm_bnr,
                               anm=akt.anm,
                               stz=akt.stz)
                alm_new.append(akt_new)
                akt_abgrenzungen_new = {}
                for abgrenzung in akt.rel_abgrenzung:

                    abgr_key = str(abgrenzung.jahr) + abgrenzung.bearbeiter + str(abgrenzung.erfassungsart_id)

                    if abgr_key in akt_abgrenzungen_new:
                        abgr_new = akt_abgrenzungen_new[abgr_key]
                    else:
                        abgr_new = BAbgrenzung(akt_id=abgrenzung.akt_id,
                                               jahr=abgrenzung.jahr,
                                               bearbeiter=abgrenzung.bearbeiter,
                                               erfassungsart_id=abgrenzung.erfassungsart_id,
                                               status_id=abgrenzung.status_id,
                                               anmerkung=abgrenzung.anmerkung,
                                               inaktiv=abgrenzung.inaktiv)
                        akt_abgrenzungen_new[abgr_key] = abgr_new
                        akt_new.rel_abgrenzung.append(abgr_new)

                    for komplex in abgrenzung.rel_komplex:
                        komplex_new = BKomplex(abgrenzung_id=komplex.abgrenzung_id,
                                               komplex_name_id=komplex.komplex_name_id)
                        abgr_new.rel_komplex.append(komplex_new)

                        for koppel in komplex.rel_koppel:
                            koppel_new =BKoppel(komplex_id=koppel.komplex_id,
                                                nr=koppel.nr,
                                                name=koppel.name,
                                                nicht_weide=koppel.nicht_weide,
                                                bearbeiter=koppel.bearbeiter,
                                                seehoehe=koppel.seehoehe,
                                                domes_id=koppel.domes_id,
                                                heuertrag_ha=koppel.heuertrag_ha,
                                                anmerkung=koppel.anmerkung,
                                                geometry=koppel.geometry)
                            komplex_new.rel_koppel.append(koppel_new)

                session.add(akt_new)

            """aktiviere foreign_key-Support in der datenbank"""
            session.execute(text('pragma foreign_keys=ON'))
            """"""

            """delete the farmitem (version) witch will be submitted (including deleting all
            children by using the cascaded 'delete' in the datamodel)"""
            for akt_inst in akt_instances:
                session.delete(akt_inst)
            """"""

            """remove the sequence of the row-id's to begin at 1 on setting
            the new row-id """
            session.execute(text("""delete from sqlite_sequence where name='a_alm_akt';"""))
            """"""

            session.commit()

        print(f'...')

    def loadKKTreeNew(self):

        def addKoppelFeature(koppel_item, koppel_layer):

            koppel_feat = QgsFeature(koppel_layer.fields())
            koppel_feat.setAttributes(
                [koppel_item.data(GisItem.Instance_Role).id,
                 koppel_item.data(GisItem.Name_Role),
                 None,
                 None,
                 None,
                 '0,123'])
            koppel_feat.setGeometry(QgsGeometry.fromWkt(
                to_shape(
                    koppel_item.data(GisItem.Geometry_Role)).wkt)
            )
            (result,
             added_kop_feat) = koppel_layer.data_provider.addFeatures(
                [koppel_feat])

            return added_kop_feat

        with db_session_cm() as session:

            abgrenzungs_instances = session.scalars(select(BAbgrenzung)
                                    .where(BAbgrenzung.akt_id == self.data_instance.id)
                                    .order_by(desc(BAbgrenzung.jahr))
                                                    ).unique().all()

            """finde alle abgrenzungen mit dem status 0 und danach 
            das jüngste Jahr"""
            ist_versions = [i for i in abgrenzungs_instances if
                            i.status_id == 0]
            max_version_year = max([y.jahr for y in ist_versions])
            """"""

            for abgrenzung in abgrenzungs_instances:

                abgrenzung_item = AbgrenzungItem(abgrenzung)
                self.komplex_root_item.appendRow(abgrenzung_item)

                """erzeuge Layer für die Komplexe und Koppeln"""
                koppel_layer = KoppelLayer(
                    "Polygon?crs=epsg:31259",
                    "Koppeln " + str(abgrenzung.jahr),
                    "memory"
                )
                komplex_layer = KomplexLayer(
                    "Polygon?crs=epsg:31259",
                    "Komplexe " + str(abgrenzung.jahr),
                    "memory"
                )
                """"""

                """finde und markiere die aktuelle Abgrenzung"""
                if abgrenzung.jahr == max_version_year and abgrenzung.status_id == 0:
                    """diese version ist die aktuelle"""
                    abgrenzung_item.setData(1, GisItem.Current_Role)
                    version_icon = QIcon(
                        ":/svg/resources/icons/triangle_right_green.svg")
                    """"""
                    komplex_layer.base = True
                    self.guiMainGis.addLayer(komplex_layer)
                    self.guiMainGis.addLayer(koppel_layer)
                else:
                    """diese version nicht die aktuelle version"""
                    abgrenzung_item.setData(0, GisItem.Current_Role)
                    version_icon = QIcon(
                        ":/svg/resources/icons/_leeres_icon.svg")
                    """"""
                    self.guiMainGis.addLayer(komplex_layer, self.kk_gis_group)
                    self.guiMainGis.addLayer(koppel_layer, self.kk_gis_group)

                abgrenzung_item.setIcon(version_icon)
                """"""

                for komplex in abgrenzung.rel_komplex:

                    komplex_geom = None

                    komplex_item = KomplexItem(komplex)
                    abgrenzung_item.appendRow(komplex_item)

                    for koppel in komplex.rel_koppel:

                        koppel_item = KoppelItem(koppel)
                        komplex_item.appendRow(koppel_item)
                        new_koppel_feat = addKoppelFeature(koppel_item, koppel_layer)

                        koppel_item.setData(new_koppel_feat[0], GisItem.Feature_Role)
                        koppel_item.setData(koppel_layer, GisItem.Layer_Role)

                        if komplex_geom == None:
                            komplex_geom = new_koppel_feat[0].geometry()
                        else:
                            komplex_geom = komplex_geom.combine(new_koppel_feat[0].geometry())

                    komplex_feat = QgsFeature(komplex_layer.fields())
                    komplex_feat.setAttributes([
                        komplex_item.data(GisItem.Instance_Role).id,
                        1,
                        komplex_item.data(GisItem.Name_Role)
                    ])
                    komplex_feat.setGeometry(komplex_geom)
                    (result,
                     added_komp_feat) = komplex_layer.data_provider.addFeatures(
                        [komplex_feat])

                    komplex_item.setData(added_komp_feat[0],
                                        GisItem.Feature_Role)
                    komplex_item.setData(komplex_layer, GisItem.Layer_Role)

            """wichig wenn neue features eingefügt werden, da die Änderung im
            provider nicht an den Layer übermittelt wird"""
            koppel_layer.updateExtents()
            """"""

            extent = koppel_layer.extent()
            self.guiMainGis.uiCanvas.setExtent(extent)

            self.uiVersionTv.setModel(self.komplex_model)

            if self.komplex_root_item.rowCount() > 0:

                self._selected_version_item = self.komplex_root_item.child(0)
                self.setKKTv(self._selected_version_item.index())
                self.uiVersionTv.selectRow(0)

        self.uiVersionTv.selectionModel().selectionChanged.connect(
            self.selectedVersionChanged)

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

        # self.uicKkJahrCombo.currentIndexChanged.connect(self.loadKKTree)
        # self.uicKkJahrComboNew.currentIndexChanged.connect(self.changedVersion)

        # self.komplexe_view.clicked.connect(self.clickedTreeElement)
        # self.kk_selection_model.selectionChanged.connect(self.treeselectionChanged)

        # self.uicCollapsNodesPbtn.clicked.connect(self.collapsKKTree)
        # self.uicExpandNodesPbtn.clicked.connect(self.expandKKTree)

        self.uiKKTv.selectionModel().selectionChanged.connect(
            self.selectionChangedTreeNew)


        # self.uiVersionTv.selectionModel().selectionChanged.connect(
        #     self.selectedVersionChanged)

    def selectedKKChanged(self, selected):

        pass
    def selectedVersionChanged(self, selected):

        self._selected_version_index = selected[0].indexes()[0]
        self._selected_version_item = self.uiVersionTv.model()\
            .itemFromIndex(self._selected_version_index)

        self.setKKTv(self._selected_version_index)

        # """lösche alle Features vom Layer Koppel"""
        # with edit(self.koppel_layer_new):
        #     listOfIds = [feat.id() for feat in self.koppel_layer_new.getFeatures()]
        #     self.koppel_layer_new.deleteFeatures(listOfIds)
        # """"""
        #
        # for kom in range(self._selected_version_item.rowCount()):
        #
        #     komplex = self._selected_version_item.child(kom)
        #     for ko in range(komplex.rowCount()):
        #         koppel = komplex.child(ko)
        #         koppel_feat = koppel.data(GisItem.Feature_Role)
        #         # (result, added_kop_feat) = self.koppel_dp_new.addFeatures(
        #         #     [koppel_feat])
        #         (result, added_kop_feat) = self.koppel_layer_new.data_provider.addFeatures(
        #             [koppel_feat])
        #         koppel.setData(added_kop_feat[0], GisItem.Feature_Role)
        #
        # self.koppel_layer_new.setName(f'Koppeln neu ')

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

        # feature_id_list = []
        sel_item = []

        for idx in self.uiKKTv.selectionModel().selectedIndexes():
            if idx.column() == 0:  # wähle nur indexe der ersten spalte!

                item = self.komplex_model.itemFromIndex(idx)
                print(f'item.data(GisItem.Feature_Role): {item.data(GisItem.Feature_Role)}')
                sel_item.append(item)
                # feature_id_list.append(item.data(GisItem.Feature_Role).id())

                # print(f':: {item.data(GisItem.Name_Role)}')
            # self.komplex_model.itemFromIndex(
            #     self.kk_selection_model.selectedIndexes()[0]).data(
            #     GisItem.Feature_Role).id()

        print(f'feature_ids:')
        for ii in sel_item:
            print(f'name: {ii.data(GisItem.Name_Role)}  id: {ii.data(GisItem.Feature_Role)}')
        print(f'fffffffffffffffffffffff')

        # self.guiMainGis.layer_tree_view.setCurrentLayer(self.koppel_layer_new)
        self.guiMainGis.layer_tree_view.setCurrentLayer(sel_item[0].data(GisItem.Layer_Role))
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

    def selectLayer(self, layer_id, feature_ids):

        for layer in self.project_instance.mapLayers().values():

            if layer_id == layer.style_id:
                self.layer_tree_view.setCurrentLayer(layer)
                self.setSelectFeature(feature_ids)

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

    def data(self, index: QModelIndex, role: int = ...):

        item = self.itemFromIndex(index)

        """get the item of the first column if you are in an other"""
        if index.column() != 0:
            first_index = index.sibling(index.row(), 0)
            first_item = self.itemFromIndex(first_index)
        """"""

        if not index.isValid():
            return None

        if index.column() == 0:

            if role == Qt.DisplayRole:
                return item.data(GisItem.Name_Role)

            if role == Qt.DecorationRole:

                if type(item) != AbgrenzungItem:

                    return item.data(GisItem.Color_Role)

        if index.column() == 1:

            if role == Qt.DisplayRole:
                return first_item.data(GisItem.Nr_Role)

        if index.column() == 2:
            pass

        # if index.column() == 3:
        #
        #     if role == Qt.DisplayRole:
        #
        #         if type(first_item) == KoppelItem:
        #             k_area = to_shape(first_item.data(GisItem.Instance_Role).geometry).area
        #             k_area_rounded = '{:.4f}'.format(
        #                 round(float(k_area) / 10000, 4)).replace(".", ",")
        #
        #             return f'{str(k_area_rounded)} ha'
        #
        #         if type(first_item) == KomplexItem:
        #             komp_area = 0.00
        #             for k in range(first_item.rowCount()):
        #                 kop_area = to_shape(first_item.child(k).data(GisItem.Instance_Role).geometry).area
        #                 komp_area = komp_area + kop_area
        #
        #             komp_area_rounded = '{:.4f}'.format(
        #                 round(float(komp_area) / 10000, 4)).replace(".", ",")
        #
        #             return f'{str(komp_area_rounded)} ha'

        return QStandardItemModel.data(self, index, role)
