import csv, sys, webbrowser, os
from _operator import attrgetter

from datetime import datetime
from pathlib import Path

from geoalchemy2 import WKTElement
from sqlalchemy import desc, text, select
from sqlalchemy.orm import joinedload

from geoalchemy2.shape import to_shape

from core.data_model import BGst, BGstEz, BGstEigentuemer, BGstNutzung, \
    BGstVersion, BSys, BKatGem, BGstZuordnung, BGstZuordnungMain, \
    BGisScopeLayer
# from core.gis_control import GisControl
from core.gis_layer import GstAllLayer, Feature, GstPreSelLayer
from core.main_gis import MainGis
from core.data_view import DataView, TableModel, TableView, \
    SortFilterProxyModel, GisTableModel

import zipfile
from io import TextIOWrapper
from os import listdir
from os.path import isfile, join

from qgis.PyQt.QtCore import (QModelIndex, Qt, QAbstractTableModel,
                          QSortFilterProxyModel, QItemSelectionModel, QSize,
                              QVariant)
from qgis.PyQt.QtGui import QColor, QIcon
from qgis.PyQt.QtWidgets import (QLabel, QMainWindow, QComboBox, QHeaderView, \
    QDockWidget, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QTableView,
                             QSplitter, QVBoxLayout, QWidget, QLineEdit)
from qgis.core import QgsVectorLayer, QgsProject, \
    QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsField, QgsGeometry, \
    edit

from core import db_session_cm, config, main_dialog, settings
from core.scopes.gst import gst_zuordnung_UI
from core.scopes.gst.gst_gemeinsame_werte import GstGemeinsameWerte


class GstZuordnung(gst_zuordnung_UI.Ui_GstZuordnung, QMainWindow):
    """
    mit diesem Formular können ein oder mehrere Gst zugeordnet werden
    """

    dialog_widget = None

    def __init__(self, parent=None, akt_id=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        self.parent = parent
        self.akt_id = akt_id

        self.checked_gst_instances = []  # liste mit den vorgemerkten gst-instanzen
        self.preselcted_gst_mci = []  # list der vorgemerkten gst-mci'S

        self.guiGisDock = GisDock(self)
        self.guiMainGis = MainGis(self.guiGisDock, self, akt_id)
        self.guiMainGis.scope_id = 2

        self.addDockWidget(Qt.RightDockWidgetArea, self.guiGisDock)
        self.guiGisDock.setWidget(self.guiMainGis)

        self.loadSupWidgets()

        self.initUi()

        self.setLoadTimeLabel()

        self.signals()

        # self.presel_proxy_model = GstPreSelFilter(self)

        # self.getZugeordneteGst()
        #
        # """initialisiere die grundstückstabelle"""
        # with db_session_cm() as session:
        #     self.guiGstTable.initDataView(session)
        # """"""
        #
        # """setzte das model für die vorgemerkte Tabelle"""
        # presel_model = self.guiGstTable.data_view_model
        # """"""
        # """filtere die Ansicht in diesem View auf die angehackten Grundstücke;
        # das wird in der Klasse 'GstPreSelFilter' erledigt """
        # self.presel_proxy_model.setSourceModel(presel_model)
        # """"""
        #
        # """da in diesem Maintabel die 'initDataView' Methode nicht verwendet
        # wird muss neben dem data_view_model auch dem view direkt das
        # model mit den daten übergeben werden"""
        # self.guiGstPreSelTview.data_view.setModel(self.presel_proxy_model)
        # self.guiGstPreSelTview.data_view_model = self.presel_proxy_model
        # """"""

        # """richte self.guiGstPreSelTview ein"""
        # self.guiGstPreSelTview.initUi()
        # self.guiGstPreSelTview.finalInit()
        # self.guiGstPreSelTview.updateMaintableNew()
        # self.guiGstPreSelTview.data_view.selectionModel().selectionChanged.connect(self.selPreChanged)
        # """"""

        # self.presel_wid = QWidget(self)
        # self.guiMatchPreSelGstPbtn = QPushButton(self)
        # self.guiMatchPreSelGstPbtn.setText('Grundstücke zuordnen')
        # self.guiMatchPreSelGstPbtn.setIcon(QIcon(":/svg/resources/icons/tick_green.svg"))
        # self.guiMatchPreSelGstPbtn.setToolTip('übernehme die <p>vorgemerkten</p> Grundstücke<br>'
        #                                       'in den aktuellen Akt')
        # self.guiMatchPreSelGstPbtn.setIconSize(QSize(30, 30))
        # self.guiMatchPreSelGstPbtn.setEnabled(False)
        #
        # self.presel_layout = QHBoxLayout(self)
        # self.presel_layout.setContentsMargins(0, 0, 0, 0)
        # self.presel_wid.setLayout(self.presel_layout)
        #
        # self.presel_layout.insertWidget(0, self.guiGstPreSelTview)
        # self.presel_layout.insertWidget(1, self.guiMatchPreSelGstPbtn)
        #
        # self.table_splitter = QSplitter()
        # self.table_splitter.setOrientation(Qt.Vertical)
        # self.table_splitter.setStyleSheet('QSplitter::handle {background: grey; }')
        # self.table_splitter.addWidget(self.guiGstTable)
        # self.table_splitter.addWidget(self.presel_wid)
        #
        # self.uiCentralLayout.addWidget(self.table_splitter)


        # self.setLoadTimeLabel()
        #
        # self.loadGisLayer()
        #
        # self.signals()
        #
        # self.linked_gis_widgets[108] = self.guiGstTable
        # self.activateGisControl()

    def loadData(self):

        pass

        # self.getZugeordneteGst()
        #
        # """initialisiere die grundstückstabelle"""
        # with db_session_cm() as session:
        #     self.guiGstTable.initDataView(session)
        # """"""
        #
        # self.setPreSelModel()
        #
        # """da in diesem Maintabel die 'initDataView' Methode nicht verwendet
        # wird muss neben dem data_view_model auch dem view direkt das
        # model mit den daten übergeben werden"""
        # self.guiGstPreSelTview.data_view.setModel(self.presel_proxy_model)
        # self.guiGstPreSelTview.data_view_model = self.presel_proxy_model
        # """"""

    def setPreSelModel(self):
        """
        setzte das model für die vorgemerkte Tabelle
        :return:
        """
        presel_model = self.guiGstTable.data_view_model

        """filtere die Ansicht im View 'self.guiGstPreSelTview' auf die 
        angehackten Grundstücke;
        das wird in 'self.presel_proxy_model' erledigt """
        self.presel_proxy_model.setSourceModel(presel_model)
        """"""

    def initUi(self):

        self.presel_wid = QWidget(self)
        self.guiMatchPreSelGstPbtn = QPushButton(self)
        self.guiMatchPreSelGstPbtn.setText('Grundstücke zuordnen')
        self.guiMatchPreSelGstPbtn.setIcon(QIcon(":/svg/resources/icons/tick_green.svg"))
        self.guiMatchPreSelGstPbtn.setToolTip('übernehme die <p>vorgemerkten</p> Grundstücke<br>'
                                              'in den aktuellen Akt')
        self.guiMatchPreSelGstPbtn.setIconSize(QSize(30, 30))
        self.guiMatchPreSelGstPbtn.setEnabled(False)

        self.presel_layout = QHBoxLayout(self)
        self.presel_layout.setContentsMargins(0, 0, 0, 0)
        self.presel_wid.setLayout(self.presel_layout)

        self.presel_layout.insertWidget(0, self.guiGstPreSelTview)
        self.presel_layout.insertWidget(1, self.guiMatchPreSelGstPbtn)

        self.table_splitter = QSplitter()
        self.table_splitter.setOrientation(Qt.Vertical)
        self.table_splitter.setStyleSheet('QSplitter::handle {background: grey; }')
        self.table_splitter.addWidget(self.guiGstTable)
        self.table_splitter.addWidget(self.presel_wid)

        self.uiCentralLayout.addWidget(self.table_splitter)

        """richte self.guiGstPreSelTview ein"""
        # self.guiGstPreSelTview.initUi()
        # self.guiGstPreSelTview.finalInit()
        # self.guiGstPreSelTview.updateMaintableNew()
        # self.guiGstPreSelTview.data_view.selectionModel().selectionChanged.connect(self.selPreChanged)
        """"""

    def initWidget(self):

        self.loadData()

        self.setLoadTimeLabel()

        self.loadGisLayer()

        self.initUi()

        # self.linked_gis_widgets[108] = self.guiGstTable
        # self.activateGisControl()

        # self.linked_gis_widgets[108] = self.guiGstTable
        # self.activateGisControl()
        self.dialog_widget._guiApplyDbtn.setEnabled(False)

        self.signals()

        self.guiGstTable.updateMaintableNew()

    def selPreChanged(self):
        """wenn die Auswahl im presel_view geändert wird"""

        """entferne die gesamte Auswahl im gst_view"""
        self.guiGstTable.data_view.clearSelection()
        """"""

        """wähle die Reihen aus"""
        for ind in self.guiGstPreSelTview.data_view.selectionModel().selectedIndexes():
            """wandle den gewählten proxy-index in den index für das 
            basis-model um"""
            basis_index = self.presel_proxy_model.mapToSource(ind)
            """"""
            self.guiGstTable.data_view.selectionModel().select(
                basis_index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
        """"""

        """wichtig um die anzahl der ausgewählten Zeilen im Footer anzuzeigen"""
        self.guiGstPreSelTview.updateMaintableNew()
        """"""

    def signals(self):

        # if self._gis_layer is not None:
        #     self._gis_layer.selectionChanged.connect(self.selectedRowsChanged)

        self.uiLoadGdbPbtn.clicked.connect(self.loadGdbDaten)
        self.guiGstTable.guiPreSelectPbtn.clicked.connect(self.reserveSelectedGst)

        self.guiMatchPreSelGstPbtn.clicked.connect(self.matchGstMultiple)

        self.uiOpenImpPathPbtn.clicked.connect(self.openImpPath)

    def loadSupWidgets(self):

        self.guiGstTable = GstTable(self)
        self.guiGstPreSelTview = GstPreSelTable(self)

        self.guiMainGis.project_instance.addMapLayer(self.guiGstTable._gis_layer)

        self.guiGstTable._gis_layer.updateExtents()

        extent = self.guiGstTable._gis_layer.extent()
        self.guiMainGis.uiCanvas.setExtent(extent)


    def loadGisLayer(self):

        with db_session_cm() as session:
            session.expire_on_commit = False

            scope_layer_inst = session.query(BGisScopeLayer) \
                .filter(BGisScopeLayer.gis_scope_id == 2) \
                .order_by(desc(BGisScopeLayer.order)) \
                .all()

        self.guiMainGis.loadLayer(scope_layer_inst)


    def setLoadTime(self, time):
        """
        trage die Zeit für den gdb-import in der datenbank ein
        """

        with db_session_cm() as session:
            time_sys_query = session.query(BSys).filter(BSys.key == 'last_gdb_import').first()
            time_sys_query.value = str(time)

            session.commit()

    def getLoadTime(self):
        """
        erhalte die Zeit des letzten gdb-importes aus der alm_sys tabelle
        """
        with db_session_cm() as session:
            time_sys_query = session.query(BSys).filter(BSys.key == 'last_gdb_import').first()
            return time_sys_query.value

    def setLoadTimeLabel(self):
        """
        setze die import-zeit im zuordnungsformular
        """

        self.uiGdbDataTimeLbl.setText(self.getLoadTime())

    def getZugeordneteGst(self):
        """
        erstelle eine liste mit den Gst, die bereits diesem Akt zugeordnet sind;
        --> bereits zugeordnete Gst können dann farblich gekennzeichnet werden
        --> es kann verhindert werden, das eine Zuordnung an dieser Stelle entfernt wird
        """

        self.akt_id = self.parent.parent.entity_id

        with db_session_cm() as session:

            zuord_query = session.query(BGst.id) \
                .join(BGstZuordnung) \
                .filter(BGstZuordnung.akt_id == self.akt_id) \
                .all()
        """erzeuge eine liste mit den id's aus dem query (=list in list)"""
        self.akt_zugeordnete_gst = [r[0] for r in zuord_query]
        """"""

    def reserveSelectedGst(self):
        """übernehme ausgewählte Grundstücke der Gst-Tabelle in die Tabelle mit
        den vorgemerkten Grundstücke"""

        if self.guiGstTable._gis_layer.selectedFeatures() != []:

            self.guiGstTable._gis_layer.startEditing()

            for feat in self.guiGstTable._gis_layer.selectedFeatures():

                if feat.attribute('zugeordnet') != 'X':

                    print(f'füge feature -- {feat.id()} -- ein!')
                    feat.setAttribute(5, 'neu')
                    self.guiGstTable._gis_layer.updateFeature(feat)

                    gst_feature_id = feat.id()
                    if gst_feature_id not in [g[0] for g in self.preselcted_gst_mci]:

                        self.preselcted_gst_mci.append([
                            gst_feature_id,
                            feat.attribute('gst_id'),
                            feat.attribute('gst'),
                            feat.attribute('ez'),
                            feat.attribute('kgnr'),
                            feat.attribute('kgname')
                            ])

                    print(f'vorgemerkte gst: {self.preselcted_gst_mci}')

            self.updatePreSelTable(self.preselcted_gst_mci)

            self.preselcted_gst_mci.clear()

            self.guiGstTable._gis_layer.commitChanges()

            self.guiGstTable._gis_layer.data_provider.dataChanged.emit()

    def updatePreSelTable(self, gst_list):
        """
        lade die features in der tabelle mit den vorgemerkten gst neu
        :param gst_list:
        :return:
        """
        self.guiGstPreSelTview._gis_layer.startEditing()

        # self.guiGstPreSelTview._gis_layer.data_provider.truncate()

        self.guiGstPreSelTview.addFeaturesFromMciList(gst_list)

        self.guiGstPreSelTview._gis_layer.commitChanges()

        self.guiGstPreSelTview._gis_layer.data_provider.dataChanged.emit()

        self.guiGstPreSelTview.updateFooter()

    def loadGdbDaten(self):
        """
        lösche zuerst alle ungenutzten Gst-Daten;
        lade dann alle Gst-Daten die sich im GDB-Importverzeichnis befinden;
        :return:
        """

        """entferne alle vorgemerkten Grundstücke"""
        self.guiGstPreSelTview.undoPreSelGst()
        """"""

        self.deleteUnusedGst()

        self.loading_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        """erstelle eine Liste mit den dateien im importverzeichnis:"""
        bev_import_path = settings.getSettingValue("bev_imp_path")
        gdb_files = [f for f in listdir(bev_import_path) if isfile(join(bev_import_path, f))]
        """"""

        self.gst_geometries = {}  # dict für die geomentrien

        self.ez_import_path = []  # liste der ez's im import-pfad (ez als base-class)

        with db_session_cm() as session:
            session.expire_on_commit = False

            """hole alle Gst die aktuell einem Akt zugeordnet sind"""
            alle_zugeordnete_gst = session.query(BGst.kg_gst).join(BGstZuordnung).all()
            self.alle_zugeordnete_gst = [r[0] for r in alle_zugeordnete_gst]
            """"""

            """durchsuche die dateien aus dem gdb-importverzeichnis"""
            for file in gdb_files:
                point_pos = file.index('.')  #: suche die Position des Punktes
                file_endung = file[point_pos+1:]  #: erhalte die Dateiendung
                if file_endung == 'zip':
                    """definiere das zip-file"""
                    path_to_zip_file = settings.getSettingValue("bev_imp_path")
                    zip_file = zipfile.ZipFile(str(Path(path_to_zip_file) / file), 'r')
                    """durchsuche die zip-datei nach dateien:
                    Wichtig: führe zuerst den loop auf dem shp-Layer durch und
                    erst dann den loop in der Grundstücks-csv"""
                    for file_in_zip_file in zip_file.namelist():

                        if 'dkmGST_V2.shp' in file_in_zip_file:
                            self.loadGstShpLayer(zip_file, file_in_zip_file)

                    for file_in_zip_file in zip_file.namelist():

                        if 'Grundstuecke_V2.csv' in file_in_zip_file:  #: file_in_zip_file ist die gst-csv
                            self.loadGstCsv(zip_file, file_in_zip_file)
            """"""

        """importiere die gdb-daten"""
        self.importGdbDaten()
        """"""

        self.setLoadTime(self.loading_time)

        """aktualisiere die Anzeige für die Import-Zeit"""
        self.setLoadTimeLabel()
        """"""

        self.guiGstTable.loadData()  # lade die Daten in der Gst-Tabelle neu
        """setzte das model für den Filter erneut, damit dieser korrekt 
        funktioniert"""
        self.setPreSelModel()
        """"""
        self.guiGstTable.updateMaintableNew()

        """aktualisiere main_gis"""
        self.guiMainGis.uiCanvas.update()
        self.guiMainGis.uiCanvas.refresh()
        """"""

    def importGdbDaten(self):
        """
        importiere die Gdb-Daten, die in die Liste self.ez_import_path geladen wurden
        """
        with db_session_cm() as session:

            """erstelle ein dict mit allen kg_gst aus der tabelle a_alm_gst mit der klasse BGst als value"""
            self.vorhandene_kg_gst = {}
            vorhandene_kg_gst_query = session.query(BGst).all()
            for gst_inst in vorhandene_kg_gst_query:
                self.vorhandene_kg_gst[gst_inst.kg_gst] = gst_inst
            """"""

            """erstelle ein dict mit den vorhandenen ez's mit der ez base-class als value"""
            self.vorhandene_ez_02 = {}
            vorhandene_ez_query = session.query(BGstEz).all()
            for ez in vorhandene_ez_query:
                self.vorhandene_ez_02[ez.kg_ez] = ez
            """"""

            for ez in self.ez_import_path:
                n = 1

                if ez.kg_ez not in self.vorhandene_ez_02:
                    """lade die komplette ez in die db da sie noch nicht existiert"""
                    session.add(ez)
                    """"""
                elif ez.kg_ez in self.vorhandene_ez_02:
                    """wandle den 'datenstand'-string in ein datetime-objekt um, um sie zu vergleichen"""
                    datenstand_vorhandene_ez = datetime.strptime(self.vorhandene_ez_02[ez.kg_ez].datenstand, '%Y-%m-%d %H:%M:%S')
                    datenstand_import_ez = datetime.strptime(ez.datenstand, '%Y-%m-%d %H:%M:%S')
                    """"""
                    if datenstand_import_ez > datenstand_vorhandene_ez:
                        """die zu importierende ez ist jünger, lese daher die gesamte ez ein;
                        die gst dürfen aber nicht neu angelegt werden, sondern nur die in dieser 
                        ez vorhandenen gst als gst_version an die bestehenden gst zugewiesen werden"""

                        new_ez = BGstEz(kgnr=ez.kgnr,
                                        ez=ez.ez,
                                        kg_ez=ez.kg_ez,
                                        datenstand=ez.datenstand,
                                        import_time=ez.import_time)
                        """hole die eingelesenen eigentuemer und weise sie der ez zu"""
                        for eig in ez.rel_alm_gst_eigentuemer:
                            new_eig = BGstEigentuemer(kg_ez=eig.kg_ez,
                                                      anteil=eig.anteil,
                                                      anteil_von=eig.anteil_von,
                                                      name=eig.name,
                                                      geb_dat=eig.geb_dat,
                                                      adresse=eig.adresse)
                            new_ez.rel_alm_gst_eigentuemer.append(new_eig)
                        """"""

                        for gst_version in ez.rel_alm_gst_version:
                            if gst_version.rel_alm_gst.kg_gst in self.vorhandene_kg_gst:
                                """das zu importierende gst ist bereits in der alm_db vorhanden"""
                                new_gst_version = BGstVersion(gst_id=self.vorhandene_kg_gst[gst_version.rel_alm_gst.kg_gst].id,
                                                              gk=gst_version.gk,
                                                              source_id=gst_version.source_id,
                                                              import_time=gst_version.import_time,
                                                              geometry=gst_version.geometry)
                                """hole die bisher eingelesenen nutzungen und weise sie der neuen gst_version zu"""
                                for nutz in gst_version.rel_alm_gst_nutzung:
                                    new_nutz = BGstNutzung(banu_id=nutz.banu_id,
                                                           ba_id=nutz.ba_id,
                                                           nu_id=nutz.nu_id,
                                                           area=nutz.area)
                                    new_gst_version.rel_alm_gst_nutzung.append(new_nutz)
                                """"""
                            else:
                                """das zu importierende gst ist noch nicht vorhanden, 
                                lege daher auch eine neue BGst-Instanz an"""
                                new_gst = BGst(kg_gst=gst_version.rel_alm_gst.kg_gst,
                                               kgnr=gst_version.rel_alm_gst.kgnr,
                                               gst=gst_version.rel_alm_gst.gst)
                                new_gst_version = BGstVersion(gk=gst_version.gk,
                                                              source_id=gst_version.source_id,
                                                              import_time=gst_version.import_time,
                                                              geometry=gst_version.geometry)
                                """hole die bisher eingelesenen nutzungen und weise sie der neuen gst_version zu"""
                                for nutz in gst_version.rel_alm_gst_nutzung:
                                    new_nutz = BGstNutzung(banu_id=nutz.banu_id,
                                                           ba_id=nutz.ba_id,
                                                           nu_id=nutz.nu_id,
                                                           area=nutz.area)
                                    new_gst_version.rel_alm_gst_nutzung.append(new_nutz)
                                """"""
                                new_gst.rel_alm_gst_version.append(new_gst_version)
                            """weise die neue gst_version der ez zu"""
                            new_ez.rel_alm_gst_version.append(new_gst_version)
                            """"""


                        session.add(new_ez)
                    else:
                        """die zu importierende ez ist gleich alt oder älter;
                        lade nur die gst die noch nicht vorhanden sind"""
                        for gst_version in ez.rel_alm_gst_version:
                            if gst_version.rel_alm_gst.kg_gst not in self.vorhandene_kg_gst:
                                """gst_version.rel_alm_gst entspricht der klasse BGst"""

                                new_gst = BGst(kg_gst=gst_version.rel_alm_gst.kg_gst,
                                               kgnr=gst_version.rel_alm_gst.kgnr,
                                               gst=gst_version.rel_alm_gst.gst)

                                new_gst_version = BGstVersion(ez_id=self.vorhandene_ez_02[ez.kg_ez].id,
                                                              gk=gst_version.gk,
                                                              source_id=gst_version.source_id,
                                                              import_time=gst_version.import_time,
                                                              geometry=gst_version.geometry)

                                """weise dem neuen gst die neue gst_version zu"""
                                new_gst.rel_alm_gst_version.append(new_gst_version)
                                """"""

                                """hole die bisher eingelesenen nutzungen und weise sie der neuen gst_version zu"""
                                for nutz in gst_version.rel_alm_gst_nutzung:
                                    new_nutz = BGstNutzung(banu_id=nutz.banu_id,
                                                           ba_id=nutz.ba_id,
                                                           nu_id=nutz.nu_id,
                                                           area=nutz.area)
                                    new_gst_version.rel_alm_gst_nutzung.append(new_nutz)
                                """"""

                                """weise die neue gst_version der vorhandenen ez zu"""
                                self.vorhandene_ez_02[ez.kg_ez].rel_alm_gst_version.append(new_gst_version)
                                """"""
                                n += 1

            session.commit()

    def loadGstShpLayer(self, zip_file, shp_file):
        """
        lade die daten der shp-datei und füge die features in das dict 'self.gst_geometries' ein; aus diesem
        dict werden später in der funktion 'loadGstCsv' die Gst-Geometrien übernommen
        """

        shp_path = "/vsizip/" + zip_file.filename + '/' + shp_file

        shp_layer = QgsVectorLayer(shp_path, "Gst", "ogr")
        if shp_layer.isValid():

            shp_features = shp_layer.getFeatures()
            feature_list = []

            """lese die crs des quell-layers aus und erzeuge damit eine transformation von dieser crs in das
            crs 'EPSG:31259' (=BMN M34)"""
            crsSrc = shp_layer.sourceCrs()
            crsDest = QgsCoordinateReferenceSystem("EPSG:31259")   # BMN M34
            transformContext = QgsProject.instance()
            xform = QgsCoordinateTransform(crsSrc, crsDest, transformContext)
            """"""

            for feat in shp_features:
                feature_list.append(feat)
                kg = feat['KG']
                gst = feat['GNR']
                kg_gst = str(kg) + str(gst)
                geom = feat.geometry()
                """transformiere die geometrie vom quell-crs zu BMN M34"""
                geom.transform(xform)
                """"""
                # todo: speichere hier die geometrie als WKB um beim abfragen
                #  aus der db ebenfalls mit WKB arbeiten zu können
                self.gst_geometries[kg_gst] = geom.asWkt()

    def loadGstCsv(self, zip_file, gst_csv):
        """
        lese die übergebene csv datei aus dem gdb-import-pfad ein und hänge diese daten als base_instanz
        der liste 'self.ez_import_path' an; diese liste wird für den import der daten in die datenbank
        verwendet;
        die instanzen werden unabhängig davon ob die daten bereits importiert wurden angelegt, beim importvorgang
        wird dann überprüft, ob die daten bereist importiert bzw. die gst einem akt zugeordnet wurden
        """

        """lese die grundstuecke-csv-datei"""
        with zip_file.open(gst_csv) as gst_csvfile:
            read_csv = csv.reader(TextIOWrapper(gst_csvfile, 'utf-8'), delimiter=';')
            headers = next(read_csv, None)  # erhalte eine liste mit den Spaltennamen

            """hole den datenstand aus der ez spalte in der spaltenüberschrifts-zeile"""
            datenstand_tag = headers[12][4:6]
            datenstand_monat = headers[12][7:9]
            datenstand_jahr = headers[12][10:14]
            datenstand_h = headers[12][15:17]
            datenstand_min = headers[12][18:20]
            datenstand_str = datenstand_jahr + '-' + datenstand_monat + '-' + datenstand_tag + ' ' + \
                             datenstand_h + ':' + datenstand_min + ':00'
            """"""

            """hole die ez daten von der ersten Daten-Zeile in der csv-datei"""
            first_row = next(read_csv, None)
            csv_kg = str(first_row[0])
            csv_ez = str(first_row[12])
            csv_kg_ez = csv_kg + csv_ez
            """"""

            """ereuge eine instanz für die ez"""
            ez_instance = BGstEz(kgnr=csv_kg,
                                 ez=csv_ez,
                                 kg_ez=csv_kg_ez,
                                 datenstand=datenstand_str,
                                 import_time=self.loading_time)
            """"""

            """lade die eigentuemer-csv für diese ez; diese muss sich im gleichen verzeichnis befinden"""
            for eigentuemer_file in zip_file.namelist():
                if 'Eigentuemer.csv' in eigentuemer_file:
                    self.loadEigentuemerCsv(zip_file, eigentuemer_file, ez_instance)
            """"""

            """lade die grundstuecke dieser csv-datei:
            pro zeile in der csv-datei sind die nutzungs-daten vorhanden, zusätlich die gst-daten. d.h., dass
            die eigentlichen gst-daten bei mehreren nutzungsarten's mehrfach vorkommen

            für den check, ob das gst bereits eingelesen wurde
            (da für jede nutzungsart eine zeile in der csv ist)"""
            gst_pro_ez = {}
            """"""

            for gst_row in read_csv:

                kgnr = gst_row[0]
                gst = gst_row[1]
                gk = gst_row[2]

                banu_id = int(str(gst_row[3]) + gst_row[4])
                ba_id = gst_row[3]
                nu_id = gst_row[4]
                flaeche = gst_row[7]

                kg_gst = str(kgnr) + str(gst)

                """pro csv-zeile wird auf jeden fall eine ba-instanz erzeugt"""
                nutzung_instance = BGstNutzung(banu_id=banu_id,
                                               ba_id=ba_id,
                                               nu_id=nu_id,
                                               area=flaeche)

                """kontrolliere, ob dieses gst bereits als solches erfasst wurde;
                wenn nicht, dann erzeuge eine gst-instanz und gst_version-instanz, weise sie einander zu
                und füge die gst-instanz in das dict 'gst_pro_ez' ein"""
                if kg_gst not in gst_pro_ez:

                    """gst bisher noch nicht eingelesen"""
                    gst_instance = BGst(kg_gst=str(kgnr)+str(gst),
                                        kgnr=kgnr,
                                        gst=gst)

                    gst_version_instance = BGstVersion(gk=gk,
                                                       source_id=1,
                                                       import_time=self.loading_time,
                                                       geometry=WKTElement(self.gst_geometries[kg_gst], srid=31259))
                    """"""

                    """weise die nutzung_instance der eben erstellten gst_version-instance zu"""
                    gst_version_instance.rel_alm_gst_nutzung.append(nutzung_instance)
                    """"""
                    """weise die gst_version-instanz der gst-instanz zu"""
                    gst_instance.rel_alm_gst_version.append(gst_version_instance)
                    """"""

                    """weise die eben erstellte gst_version-instance der oben erstellten ez_instance zu
                    (da die ez auf der ebene der gst_version mit dem gst in beziehung steht!)"""
                    ez_instance.rel_alm_gst_version.append(gst_version_instance)
                    """"""

                    gst_pro_ez[kg_gst] = gst_instance

                elif kg_gst in gst_pro_ez:

                    """gst bereits eingelsen; d.h. die nutzungsart-instanz wird nur dem bereits eingelesenen
                    gst (eben der gst_version) zugewiesen"""
                    gst_pro_ez[kg_gst].rel_alm_gst_version[0].rel_alm_gst_nutzung.append(nutzung_instance)

            self.ez_import_path.append(ez_instance)

    def loadEigentuemerCsv(self, zip_file, eigentuemer_csv, related_ez_instance):
        """
        lese die eigentümer aus der übergebenen csv datei ein;
        für jeden eigentümer wird eine instanz erzeugt, die der übergeben ez-instanz zugewiesen wird
        """

        """lese die eigentuemer-csv-datei"""
        with zip_file.open(eigentuemer_csv) as eigentuemer_csvfile:
            read_eig_csv = csv.reader(TextIOWrapper(eigentuemer_csvfile, 'utf-8'), delimiter=';')
            """überspringe die erste Zeile mit den Spaltenüberschriften"""
            headers = next(read_eig_csv, None)  # erhalte eine liste mit den Spaltennamen
            """"""

            for eig_row in read_eig_csv:
                row_name = eig_row[7] + ' ' + eig_row[8] + ' ' + eig_row[13]

                eig_instance = BGstEigentuemer(kg_ez=str(eig_row[0]) + str(eig_row[2]),
                                               anteil=eig_row[4],
                                               anteil_von=eig_row[5],
                                               name=row_name.strip(),
                                               geb_dat=eig_row[10],
                                               adresse=eig_row[16])

                related_ez_instance.rel_alm_gst_eigentuemer.append(eig_instance)
        """"""

    def matchGstMultiple(self):
        """
        führe die zuordnung von mehreren grundstücken durch
        """

        """öffne den dialog 'GemeinsameWerte' und ordne die gst dem akt zu
        wenn 'accept' geklickt wird"""
        gemeinsame_werte = GstGemeinsameWerte(self)
        gem_dialog = GstGemWerteMainDialog(self)
        gem_dialog.initDialog(gemeinsame_werte, center_in=self)
        result = gem_dialog.exec()
        """"""

        if result:

            awb_status = gemeinsame_werte.awb_status_model.data(gemeinsame_werte.awb_status_model.index(
                gemeinsame_werte.uiAwbStatusCombo.currentIndex(),0), Qt.EditRole)

            rechtsgrundlage = gemeinsame_werte.rechtsgrundlage_model.data(gemeinsame_werte.rechtsgrundlage_model.index(
                gemeinsame_werte.uiRechtsformCombo.currentIndex(),0), Qt.EditRole)

            anm = gemeinsame_werte.uiAnmerkungTedit.toPlainText()
            problem = gemeinsame_werte.uiProblemTedit.toPlainText()

            # accept_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            """übernehme die markierten Gst in die GDB-Tabelle (inkl. EZ, Eigentuemer u. Nutzungen)"""
            with db_session_cm() as session:
                session.expire_on_commit = False
                for gst_instance in self.checked_gst_instances:

                    gst_zuordnung = BGstZuordnung(akt_id=self.parent.parent.entity_id,
                                                  gst_id=gst_instance.id,
                                                  awb_status_id=awb_status,
                                                  rechtsgrundlage_id=rechtsgrundlage,
                                                  anmerkung=anm,
                                                  probleme=problem)
                    session.add(gst_zuordnung)

            session.commit()
            """"""

            """update den akt"""
            self.parent.parent.updateAkt()
            """"""

            self.dialog_widget.reject()  # schliesse  zuordungs-dialog

    def openImpPath(self):
        """
        öffne das BEV-Import-Verzeichnis

        :return:
        """

        path = settings.getSettingValue("bev_imp_path")

        webbrowser.open(os.path.realpath(path))

    def deleteUnusedGst(self):
        """
        lösche Gst-Daten aus der db die nicht genutzt werden
        (keinem akt zugewiesen sind);

        mache die aus performace-gründen direkt in der db
        """

        with db_session_cm() as session:

            """aktiviere foreign_key-Support in der alm-datenbank"""
            session.execute(text('pragma foreign_keys=ON'))
            """"""

            del_gst = "DELETE FROM a_alm_gst WHERE " \
                      "id NOT IN (SELECT gst_id FROM a_alm_gst_zuordnung);"

            del_gst_version = "DELETE FROM a_alm_gst_version WHERE " \
                              "gst_id NOT IN (SELECT id FROM a_alm_gst);"

            del_ez = "DELETE FROM a_alm_gst_ez WHERE id NOT IN " \
                     "(SELECT ez_id FROM a_alm_gst_version);"

            del_eig = "DELETE FROM a_alm_gst_eigentuemer WHERE" \
                      " ez_id NOT IN (SELECT id FROM a_alm_gst_ez);"

            del_nutz = "DELETE FROM a_alm_gst_nutzung WHERE gst_version_id " \
                       "NOT IN (SELECT id FROM a_alm_gst_version);"

            session.execute(text(del_gst))
            session.execute(text(del_gst_version))
            session.execute(text(del_ez))
            session.execute(text(del_eig))
            session.execute(text(del_nutz))


class GstModel(TableModel):

    col_with_kg_gst_value = 0
    col_with_checkbox = 2

    def __init__(self, parent, data_array=None):
        super(__class__, self).__init__(parent)

        self.parent = parent
        self.data_array = None

        if data_array:
            self.data_array = data_array

    def data(self, index: QModelIndex, role: int = ...):

        if not index.isValid():
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.data_array[index.row()][index.column()]

        """setze eine Schriftfarbe, wenn das gst diesem Akt bereits zugeordnet ist"""
        if role == Qt.ForegroundRole:
            if index.column() == self.col_with_checkbox:
                if self.data(self.index(index.row(), 0),
                             Qt.DisplayRole) in self.parent.parent.akt_zugeordnete_gst:
                    return QColor(15, 153, 222)
        """"""

        """setze den check-status auf spalte 2"""
        if role == Qt.CheckStateRole:
            if index.column() == 2:
                return self.checkState(QModelIndex(index))
        """"""

        return super().data(index, role)

    def checkState(self, index):
        """markiere wenn das gst in der liste checked_gst ist"""
        if self.data(self.index(index.row(), 0), Qt.DisplayRole) \
                in [gst.id for gst in self.parent.parent.checked_gst_instances]:
            return Qt.Checked
        """"""

        """markiere wenn das gst bereits zugeordnet ist"""
        if self.data(self.index(index.row(), 0), Qt.DisplayRole) \
                in self.parent.parent.akt_zugeordnete_gst:
            return Qt.Checked
        else:
            return Qt.Unchecked
        """"""

    def setData(self, index, value, role=Qt.EditRole):

        if not index.isValid():
            return False

        if role == Qt.CheckStateRole and index.column() == 2:
            """durch das setzten eines Hakens wird die Liste 
            'checked_gst_instances' modifiziert, auf dieser basierend wird
            der Haken mit der Methode 'checkState' gesetzt. """

            """entferne die kg_gst wenn sie sich in der liste der marktierten gst befindet:"""
            if self.data(self.index(index.row(), 0), Qt.DisplayRole) \
                    in [gst.id for gst in self.parent.parent.checked_gst_instances]:
                self.parent.parent.checked_gst_instances.remove(
                     self.data(self.index(index.row(), 9), Qt.DisplayRole))
                """"""

                """wenn die kg_gst nicht bereits dem akt zugeordnet ist, dann füge sie der liste der markierten gst hinzu:"""
            elif self.data(self.index(index.row(), 0), Qt.DisplayRole)  not in self.parent.parent.akt_zugeordnete_gst:

                self.parent.parent.checked_gst_instances.append(
                    self.data(self.index(index.row(), 9), Qt.DisplayRole))
                """"""

            """aktualisiere das model am entsprechenden index
            (siehe: https://stackoverflow.com/questions/65386552/update-object-when-checkbox-clicked-in-qtableview"""
            self.dataChanged.emit(index, index)
            """"""
            """nachdem (!) das model aktualisiert wurde, aktualisiere das
            view"""
            self.parent.parent.guiGstPreSelTview.updateMaintableNew()
            """"""

            """aktiviere oder deaktiviere den Button zum zuordnen vorgemerkter
            Grundstücke"""
            if self.parent.parent.checked_gst_instances:
                self.parent.parent.guiMatchPreSelGstPbtn.setEnabled(True)
            else:
                self.parent.parent.guiMatchPreSelGstPbtn.setEnabled(False)
            """"""

            return True
        return False

    def flags(self, index):

        if not index.isValid():
            return None

        if index.column() == self.col_with_checkbox:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable


class GstTableModel(GisTableModel):

    def __init__(self, layerCache, parent=None):
        super(GisTableModel, self).__init__(layerCache, parent)

    def data(self, index: QModelIndex, role: int = ...):

        # feat = self.feature(index)

        if role == Qt.TextAlignmentRole:

            if index.column() in [3]:

                return Qt.AlignRight | Qt.AlignVCenter

            if index.column() in [1, 2, 5]:

                return Qt.AlignHCenter | Qt.AlignVCenter

        if index.column() == 3:

            if role == Qt.DisplayRole:

                return str(self.feature(index).attribute('kgnr'))

        # if index.column() == 9:  # gis_area
        #
        #     if role == Qt.DisplayRole:
        #
        #         area = self.feature(index).attribute('gis_area')
        #         area_r = '{:.4f}'.format(round(float(area) / 10000, 4)
        #                                  ).replace(".", ",")
        #         return area_r + ' ha'
        #
        #     # if role == Qt.EditRole:
        #     #     return area
        #
        # if index.column() == 10:  # gb_area
        #
        #     if role == Qt.DisplayRole:
        #
        #         area = self.feature(index).attribute('gb_area')
        #         area_r = '{:.4f}'.format(round(float(area) / 10000, 4)
        #                                  ).replace(".", ",")
        #         return area_r + ' ha'

        return super().data(index, role)

    # def flags(self, index):
    #
    #     # if not index.isValid():
    #     #     return None
    #
    #     if index.column() == 5:
    #         return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    #     else:
    #         return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable


class GstTable(DataView):
    """
    tabelle mit den grundstücken die zugeordnet werden können bzw. bereits
    zugeordnet sind
    """

    # gis_relation = {"gis_id_column": 0,
    #                 "gis_layer_style_id": 108,
    #                 "gis_layer_id_column": 'id'}

    # _data_view = TableView
    # _model_class = GstModel

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self._gis_table_model_class = GstTableModel

        self.uiTitleLbl.setText('Grundstücke die zugeordnet werden können:')
        self.maintable_text = ["Grundstück", "Grundstücke", "kein Grundstück"]

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


    def setFeatureFields(self):

        gst_id_fld = QgsField("gst_id", QVariant.Int)

        gst_fld = QgsField("gst", QVariant.String)
        gst_fld.setAlias('Gst')

        ez_fld = QgsField("ez", QVariant.Int)
        ez_fld.setAlias('EZ')

        kgnr_fld = QgsField("kgnr", QVariant.Int)
        kgnr_fld.setAlias('KG-Nr')

        kgname_fld = QgsField("kgname", QVariant.String)
        kgname_fld.setAlias('KG-Name')

        zugeordnet_fld = QgsField("zugeordnet", QVariant.String)
        zugeordnet_fld.setAlias('zugeordnet')

        zugeordnet_zu_fld = QgsField("zugeordnet_zu", QVariant.String)
        zugeordnet_zu_fld.setAlias('zugeordnet zu')

        datenstand_fld = QgsField("datenstand", QVariant.String)
        datenstand_fld.setAlias('Datenstand')

        importzeit_fld = QgsField("importzeit", QVariant.String)
        importzeit_fld.setAlias('Importzeit')

        self.feature_fields.append(gst_id_fld)
        self.feature_fields.append(gst_fld)
        self.feature_fields.append(ez_fld)
        self.feature_fields.append(kgnr_fld)
        self.feature_fields.append(kgname_fld)
        self.feature_fields.append(zugeordnet_fld)
        self.feature_fields.append(zugeordnet_zu_fld)
        self.feature_fields.append(datenstand_fld)
        self.feature_fields.append(importzeit_fld)

    def setFeaturesFromMci(self):
        super().setFeaturesFromMci()

        for gst in self._mci_list:

            feat = Feature(self._gis_layer.fields(), self)

            self.setFeatureAttributes(feat, gst)

            """last_gst"""
            gst_versionen_list = gst.rel_alm_gst_version
            last_gst = max(gst_versionen_list,
                           key=attrgetter('rel_alm_gst_ez.datenstand'))
            """"""

            geom_wkt = to_shape(last_gst.geometry).wkt
            geom_new = QgsGeometry()
            geom = geom_new.fromWkt(geom_wkt)

            feat.setGeometry(geom)

            self._gis_layer.data_provider.addFeatures([feat])

    def setFeatureAttributes(self, feature, mci):

        """last_gst"""
        gst_versionen_list = mci.rel_alm_gst_version
        last_gst = max(gst_versionen_list,
                       key=attrgetter('rel_alm_gst_ez.datenstand'))
        """"""

        zugeordnet = '--'

        zugeordnet_list = []
        if mci.rel_gst_zuordnung != []:
            for gst_zuord in mci.rel_gst_zuordnung:
                zugeordnet_list.append(gst_zuord.rel_akt.name)

                if gst_zuord.rel_akt.id == self.parent.akt_id:
                    zugeordnet = 'X'


            zugeordnet_zu = ", ".join(str(z) for z in zugeordnet_list)
        else:
            zugeordnet_zu = '---'

        feature['gst_id'] = mci.id
        feature['gst'] = mci.gst
        feature['ez'] = last_gst.rel_alm_gst_ez.ez
        feature['kgnr'] = mci.kgnr
        feature['kgname'] = mci.rel_kat_gem.kgname
        feature['zugeordnet'] = zugeordnet
        feature['zugeordnet_zu'] = zugeordnet_zu
        feature['datenstand'] = last_gst.rel_alm_gst_ez.datenstand
        feature['importzeit'] = last_gst.rel_alm_gst_ez.import_time

    def setLayer(self):

        layer = GstAllLayer(
            "Polygon?crs=epsg:31259",
            "GstAllLay",
            "memory",
            feature_fields=self.feature_fields
        )
        return layer

    def initUi(self):
        super().initUi()

        self.uiAddDataTbtn.setVisible(False)
        self.uiEditDataTbtn.setVisible(False)
        self.uiDeleteDataTbtn.setVisible(False)

        self.guiPreSelectPbtn = QPushButton()
        self.guiPreSelectPbtn.setText('Auswahl übernehmen')
        self.guiPreSelectPbtn.setIcon(QIcon(":/svg/resources/icons/arrow_down_blue.svg"))
        self.guiPreSelectPbtn.setToolTip('merke die ausgewählten Grundstücke vor')
        self.guiPreSelectPbtn.setIconSize(QSize(30, 30))
        self.guiPreSelectPbtn.setEnabled(False)

        self.uiFooterHlay.addWidget(self.guiPreSelectPbtn)

        self.guiGstChecked = QLabel()
        self.uiFooterSubVlay.addWidget(self.guiGstChecked)

    def getMciList(self, session):

        stmt = (select(BGst)
        .options(
            joinedload(BGst.rel_alm_gst_version)
            .joinedload(BGstVersion.rel_alm_gst_ez)
        )
        .options(
            joinedload(BGst.rel_alm_gst_version)
            .joinedload(BGstVersion.rel_alm_gst_nutzung)
        )
        .options(
            joinedload(BGst.rel_kat_gem)
        )
        .options(
            joinedload(BGst.rel_gst_zuordnung)
            .joinedload(BGstZuordnung.rel_akt)
        )
        )

        mci = session.scalars(stmt).unique().all()

        return mci

    def finalInit(self):
        super().finalInit()

        self.setStretchMethod(2)

        self.view.setColumnHidden(0, True)

        """setzt bestimmte spaltenbreiten"""
        self.view.setColumnWidth(1, 60)
        self.view.setColumnWidth(2, 50)
        self.view.setColumnWidth(3, 60)
        self.view.setColumnWidth(4, 150)
        self.view.setColumnWidth(5, 80)
        self.view.setColumnWidth(6, 100)
        """"""

    # def setMaintableColumns(self):
    #     super().setMaintableColumns()
    #
    #     self.maintable_columns[0] = MaintableColumn(column_type='int',
    #                                                 visible=False)
    #     self.maintable_columns[1] = MaintableColumn(column_type='str',
    #                                                 visible=False)
    #     self.maintable_columns[2] = MaintableColumn(column_type='str',
    #                                                 heading='Gst',
    #                                                 alignment='l')
    #     self.maintable_columns[3] = MaintableColumn(heading='KG-Nr',
    #                                                 column_type='int',
    #                                                 alignment='r')
    #     self.maintable_columns[4] = MaintableColumn(heading='KG-Name',
    #                                                 column_type='str',
    #                                                 alignment='l')
    #     self.maintable_columns[5] = MaintableColumn(heading='EZ',
    #                                                 column_type='int',
    #                                                 alignment='c')
    #     self.maintable_columns[6] = MaintableColumn(heading="zugeordnet zu",
    #                                                 column_type='str',
    #                                                 alignment='l')
    #     self.maintable_columns[7] = MaintableColumn(heading='Datenstand',
    #                                                 column_type='str')
    #     self.maintable_columns[8] = MaintableColumn(heading='Importzeit',
    #                                                 column_type='str')
    #     self.maintable_columns[9] = MaintableColumn(column_type='str',
    #                                                 visible=False)
    #
    # def getMainQuery(self, session=None):
    #     super().getMainQuery(session)
    #
    #     query = session.query(BGstZuordnungMain.id,
    #                           BGstZuordnungMain.kg_gst,
    #                           BGstZuordnungMain.gst,
    #                           BGstZuordnungMain.kgnr,
    #                           BGstZuordnungMain.kg_name,
    #                           BGstZuordnungMain.ez,
    #                           BGstZuordnungMain.zu_aw,
    #                           BGstZuordnungMain.datenstand,
    #                           BGstZuordnungMain.import_time,
    #                           BGstZuordnungMain)
    #
    #     return query

    # def setMainTableModel(self):
    #     super().setMainTableModel()
    #
    #     return GstModel(parent=self, data_array=self.maintable_dataarray)

    # def setFilterScopeUI(self):
    #     super().setFilterScopeUI()
    #
    #     """filter ez"""
    #     self.guiFilterEzLbl = QLabel("Ez:")
    #     self.guiFilterEzCombo = QComboBox(self)
    #
    #     self.uiTableFilterHLay.insertWidget(2, self.guiFilterEzLbl)
    #     self.uiTableFilterHLay.insertWidget(3, self.guiFilterEzCombo)
    #     """"""
    #
    #     """filter kg name"""
    #     self.guiFilterKgNameLbl = QLabel("Kg-Name:")
    #     self.guiFilterKgNameCombo = QComboBox(self)
    #
    #     self.uiTableFilterHLay.insertWidget(2, self.guiFilterKgNameLbl)
    #     self.uiTableFilterHLay.insertWidget(3, self.guiFilterKgNameCombo)
    #     """"""
    #
    #     """filter kgnr"""
    #     self.guiFilterKgLbl = QLabel("Kg-Nr:")
    #     self.guiFilterKgCombo = QComboBox(self)
    #
    #     # self.uiFilterScopeHLay.insertWidget(0, self.guiFiltRechtsverhLbl)
    #     self.uiTableFilterHLay.insertWidget(2, self.guiFilterKgLbl)
    #     self.uiTableFilterHLay.insertWidget(3, self.guiFilterKgCombo)
    #     """"""

    # def setFilterScope(self):
    #     super().setFilterScope()
    #
    #     self.setFilterKgnr()
    #     self.setFilterKgName()
    #     self.setFilterEz()

    # def setFilterKgnr(self):
    #
    #     with db_session_cm() as session:
    #         item_query = session.query(BGstEz.kgnr).distinct()
    #
    #     try:
    #         self.guiFilterKgCombo.currentTextChanged.disconnect(
    #             self.filterMaintable)
    #     except:
    #         pass
    #     finally:
    #         prev_typ = self.guiFilterKgCombo.currentText()
    #         self.guiFilterKgCombo.clear()
    #
    #         self.guiFilterKgCombo.addItem('- Alle -')
    #         for item in sorted(item_query):
    #             self.guiFilterKgCombo.addItem(str(item[0]))
    #
    #         self.guiFilterKgCombo.setCurrentText(prev_typ)
    #
    #         self.guiFilterKgCombo.currentTextChanged.connect(
    #             self.applyFilter)

    # def setFilterKgName(self):
    #
    #     with db_session_cm() as session:
    #         item_query = session.query(BKatGem.kgname).join(BGstEz).distinct()
    #
    #     try:
    #         self.guiFilterKgNameCombo.currentTextChanged.disconnect(
    #             self.filterMaintable)
    #     except:
    #         pass
    #     finally:
    #         prev_typ = self.guiFilterKgNameCombo.currentText()
    #         self.guiFilterKgNameCombo.clear()
    #
    #         self.guiFilterKgNameCombo.addItem('- Alle -')
    #         for item in sorted(item_query):
    #             self.guiFilterKgNameCombo.addItem(str(item[0]))
    #
    #         self.guiFilterKgNameCombo.setCurrentText(prev_typ)
    #
    #         self.guiFilterKgNameCombo.currentTextChanged.connect(
    #             self.applyFilter)

    # def setFilterEz(self):
    #
    #     with db_session_cm() as session:
    #         item_query = session.query(BGstEz.ez).distinct()
    #
    #     try:
    #         self.guiFilterEzCombo.currentTextChanged.disconnect(
    #             self.filterMaintable)
    #     except:
    #         pass
    #     finally:
    #         prev_typ = self.guiFilterEzCombo.currentText()
    #         self.guiFilterEzCombo.clear()
    #
    #         self.guiFilterEzCombo.addItem('- Alle -')
    #         for item in sorted(item_query):
    #             self.guiFilterEzCombo.addItem(str(item[0]))
    #
    #         self.guiFilterEzCombo.setCurrentText(prev_typ)
    #
    #         self.guiFilterEzCombo.currentTextChanged.connect(
    #             self.applyFilter)

    # def useFilterScope(self, source_row, source_parent):
    #     super().useFilterScope(source_row, source_parent)
    #
    #     try:
    #         """filter KgNr"""
    #         table_value = self.filter_proxy.sourceModel() \
    #             .data(self.filter_proxy.sourceModel().index(source_row, 3),
    #         Qt.DisplayRole)
    #         if self.guiFilterKgCombo.currentText() != "- Alle -":
    #             if str(table_value) != self.guiFilterKgCombo.currentText():
    #                 return False
    #         """"""
    #
    #         """filter KgName"""
    #         table_value = self.filter_proxy.sourceModel() \
    #             .data(self.filter_proxy.sourceModel().index(source_row, 4),
    #         Qt.DisplayRole)
    #         if self.guiFilterKgNameCombo.currentText() != "- Alle -":
    #             if str(table_value) != self.guiFilterKgNameCombo.currentText():
    #                 return False
    #         """"""
    #
    #         """filter Ez"""
    #         table_value = self.filter_proxy.sourceModel() \
    #             .data(self.filter_proxy.sourceModel().index(source_row, 5),
    #         Qt.DisplayRole)
    #         if self.guiFilterEzCombo.currentText() != "- Alle -":
    #             if str(table_value) != self.guiFilterEzCombo.currentText():
    #                 return False
    #         """"""
    #     except:
    #         print("Filter Error:", sys.exc_info())

    def selectedRowsChanged(self):
        super().selectedRowsChanged()

        """aktiviere oder deaktiviere den Button zum zuordnen vorgemerkter
        Grundstücke"""

        if self._gis_layer.selectedFeatureIds() != []:
            self.guiPreSelectPbtn.setEnabled(True)
        else:
            self.guiPreSelectPbtn.setEnabled(False)

        # if self.view.selectionModel().selectedRows():
        #     self.guiPreSelectPbtn.setEnabled(True)
        # else:
        #     self.guiPreSelectPbtn.setEnabled(False)
        """"""

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
        """"""

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        filter_lay.addItem(spacerItem)

        self.uiHeaderHley.insertLayout(1, filter_lay)

    def useFilter(self):

        gst_text = self.filter_gst_input_wdg.text()
        ez_text = self.filter_ez_input_wdg.text()
        kgnr_text = self.filter_kgnr_input_wdg.text()
        kgname_text = self.filter_kgname_input_wdg.text()

        gst_expr = f"lower(\"gst\") LIKE '%{gst_text}%'"
        ez_expr = f"to_string(\"ez\") LIKE '%{ez_text}%'"
        kgnr_expr = f"to_string(\"kgnr\") LIKE '%{kgnr_text}%'"
        kgname_expr = f"lower(\"kgname\") LIKE '%{kgname_text}%'"

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

        if expr_list == []:
            self._gis_layer.setSubsetString('')
        else:

            expr_string = " and ".join(expr for expr in expr_list)
            print(f'expression string: {expr_string}')
            self._gis_layer.setSubsetString(expr_string)

        self.updateFooter()


class GstPreSelTable(DataView):

    _data_view = TableView

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent

        # self.available_filters = ''
        self.title = 'vorgemerkte Grundstücke:'

        self.maintable_text = ["vorgemerktesGrundstück",
                               "vorgemerkte Grundstücke",
                               "kein vorgemerktes Grundstück"]

        self.guiUndoPreSelPbtn = QPushButton(self)
        self.guiUndoPreSelPbtn.setIcon(
            QIcon(":/svg/resources/icons/arrow_up_blue.svg"))
        self.guiUndoPreSelPbtn.setIconSize(QSize(25, 25))
        self.guiUndoPreSelPbtn.setFixedSize(32, 31)
        self.guiUndoPreSelPbtn.setFlat(True)
        self.guiUndoPreSelPbtn.setToolTip('entferne alle vorgemerkten Grundstücke')
        self.uiHeaderHley.insertWidget(1, self.guiUndoPreSelPbtn)

        self.guiUndoPreSelPbtn.clicked.connect(self.undoPreSelGst)

        """"""
        self.setFeatureFields()
        # self.setFilterUI()
        # self.setCanvas(self.parent.guiMainGis.uiCanvas)

        self._gis_layer = self.setLayer()

        self.loadData()
        self.setFeaturesFromMci()
        self.setTableView()

        self.finalInit()

        self.updateFooter()

        self.signals()
        """"""

    def loadData(self):

        self._mci_list = self.parent.preselcted_gst_mci
        # self._mci_list = [[1, '314/3', 136, 19321, 'Mitterbachseerotte'],
        #                   [2, '314/4', 136, 19321, 'Mitterbachseerotte']]

    def setFeatureFields(self):

        feat_id_fld = QgsField("feat_id", QVariant.Int)

        gst_id_fld = QgsField("gst_id", QVariant.Int)

        gst_fld = QgsField("gst", QVariant.String)
        gst_fld.setAlias('Gst')

        ez_fld = QgsField("ez", QVariant.Int)
        ez_fld.setAlias('EZ')

        kgnr_fld = QgsField("kgnr", QVariant.Int)
        kgnr_fld.setAlias('KG-Nr')

        kgname_fld = QgsField("kgname", QVariant.String)
        kgname_fld.setAlias('KG-Name')

        self.feature_fields.append(feat_id_fld)
        self.feature_fields.append(gst_id_fld)
        self.feature_fields.append(gst_fld)
        self.feature_fields.append(ez_fld)
        self.feature_fields.append(kgnr_fld)
        self.feature_fields.append(kgname_fld)

    def setFeaturesFromMci(self):
        super().setFeaturesFromMci()

        for gst in self._mci_list:

            feat = Feature(self._gis_layer.fields(), self)

            self.setFeatureAttributes(feat, gst)

            # """last_gst"""
            # gst_versionen_list = gst.rel_alm_gst_version
            # last_gst = max(gst_versionen_list,
            #                key=attrgetter('rel_alm_gst_ez.datenstand'))
            # """"""

            # geom_wkt = to_shape(last_gst.geometry).wkt
            # geom_new = QgsGeometry()
            # geom = geom_new.fromWkt(geom_wkt)
            #
            # feat.setGeometry(geom)

            self._gis_layer.data_provider.addFeatures([feat])

    def setFeatureAttributes(self, feature, mci):

        # """last_gst"""
        # gst_versionen_list = mci.rel_alm_gst_version
        # last_gst = max(gst_versionen_list,
        #                key=attrgetter('rel_alm_gst_ez.datenstand'))
        # """"""
        #
        # zugeordnet = '--'
        #
        # zugeordnet_list = []
        # if mci.rel_gst_zuordnung != []:
        #     for gst_zuord in mci.rel_gst_zuordnung:
        #         zugeordnet_list.append(gst_zuord.rel_akt.name)
        #
        #         if gst_zuord.rel_akt.id == self.parent.akt_id:
        #             zugeordnet = 'X'
        #
        #
        #     zugeordnet_zu = ", ".join(str(z) for z in zugeordnet_list)
        # else:
        #     zugeordnet_zu = '---'

        feature['feat_id'] = mci[0]
        feature['gst_id'] = mci[1]
        feature['gst'] = mci[2]
        feature['ez'] = mci[3]
        feature['kgnr'] = mci[4]
        feature['kgname'] = mci[5]

    def setLayer(self):

        layer = GstPreSelLayer(
            "None",
            "GstPreSelLay",
            "memory",
            feature_fields=self.feature_fields
        )
        return layer

    def undoPreSelGst(self):
        """
        entferne alle selektierten vorgemerkten Grundstücke
        :return:
        """

        self._gis_layer.data_provider.deleteFeatures(
            self._gis_layer.selectedFeatureIds())

        self._gis_layer.data_provider.dataChanged.emit()

        self.updateFooter()

    def initUi(self):
        super().initUi()

        self.uiAddDataTbtn.setVisible(False)
        self.uiEditDataTbtn.setVisible(False)
        self.uiDeleteDataTbtn.setVisible(False)
        self.uiToolsTbtn.setVisible(False)

        # """blende unnötige Spalten aus"""
        # self.view.setColumnHidden(0, True)
        # self.view.setColumnHidden(1, True)
        # self.view.setColumnHidden(6, True)
        # self.view.setColumnHidden(7, True)
        # self.view.setColumnHidden(8, True)
        # self.view.setColumnHidden(9, True)
        # """"""

    def finalInit(self):
        super().finalInit()

        # """setzt bestimmte spaltenbreiten"""
        # self.view.setColumnWidth(2, 80)
        # self.view.setColumnWidth(3, 45)
        # self.view.setColumnWidth(4, 150)
        # self.view.setColumnWidth(5, 40)
        # """"""

        self.setMaximumWidth(450)

        self.signals()

    def signals(self):
        # super().signals()

        self._gis_layer.data_provider.dataChanged.connect(self.preselChangend)

        # self.uiDeleteDataTbtn.clicked.disconnect()
        #
        # self.uiDeleteDataTbtn.clicked.connect(self.removeReservedGst)
        #
        # self.uiClearSelectionPbtn.clicked.connect(self.clearSelectedRows)

    def preselChangend(self):

        if self.view.model().rowCount() > 0:
            self.parent.guiMatchPreSelGstPbtn.setEnabled(True)
        else:
            self.parent.guiMatchPreSelGstPbtn.setEnabled(False)

    # def clearSelectedRows(self):
    #     # super().clearSelectedRows()
    #
    #     self.data_view.selectionModel().clear()

class GstPreSelFilter(QSortFilterProxyModel):

    def __init__(self, parent):
        QSortFilterProxyModel.__init__(self, parent)

        self.parent = parent

    def filterAcceptsRow(self, pos, index):

        model = self.sourceModel()
        """zeige nur Zeilen die angehakt sind und deren kg_gst-key sich aber 
        nicht in der Liste 'akt_zugeordnete_gst' befindet"""
        if (model.data(model.index(pos, 2), Qt.CheckStateRole) == Qt.Checked and
                model.data(model.index(pos, 0), Qt.DisplayRole) not in self.parent.akt_zugeordnete_gst):
            return True
        """"""
        return False


class GstGemWerteMainDialog(main_dialog.MainDialog):
    """
    dialog zum setzen gemeinsamer werte bei der grundstückszuordnung
    """

    def __init__(self, parent=None):
        super(GstGemWerteMainDialog, self).__init__(parent)

        self.parent = parent

        self.enableApply = True

        self.dialog_window_title = 'Werte setzen'
        self.set_apply_button_text('&Werte setzen und zuordnen')


class GisDock(QDockWidget):

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.setWindowTitle('Kartenansicht')
