import csv

import sys
from datetime import datetime

from geoalchemy2 import WKTElement
from sqlalchemy import desc, text

from core.data_model import BGst, BGstEz, BGstEigentuemer, BGstNutzung, \
    BGstVersion, BSys, BKatGem, BGstZuordnung, BGstZuordnungMain, \
    BGisScopeLayer
from core.gis_control import GisControl
from core.main_gis import MainGis
from core.main_table import MainTable, MaintableColumn, MainTableModel, \
    MainTableView

import zipfile
from io import TextIOWrapper
from os import listdir
from os.path import isfile, join

from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QMainWindow, QComboBox, QHeaderView, \
    QDockWidget
from qgis.core import QgsVectorLayer, QgsProject, \
    QgsCoordinateReferenceSystem, QgsCoordinateTransform

from core import DbSession, config, main_dialog
from core.scopes.gst import gst_zuordnung_UI
from core.scopes.gst.gst_gemeinsame_werte import GstGemeinsameWerte


class GstZuordnung(gst_zuordnung_UI.Ui_GstZuordnung, QMainWindow, GisControl):
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

        self.guiGisDock = GisDock(self)
        self.guiMainGis = MainGis(self.guiGisDock, self, akt_id)
        self.guiMainGis.scope_id = 2

        self.addDockWidget(Qt.RightDockWidgetArea, self.guiGisDock)
        self.guiGisDock.setWidget(self.guiMainGis)

        self.guiGstTable = GstTable(self)
        self.uiTableVlay.addWidget(self.guiGstTable)

    def initWidget(self):

        self.getZugeordneteGst()

        """initialisiere die grundstückstabelle"""
        with DbSession.session_scope() as session:
            self.guiGstTable.initMaintable(session)
        """"""

        self.setLoadTimeLabel()

        self.loadGisLayer()

        self.signals()

        self.linked_gis_widgets[108] = self.guiGstTable
        self.activateGisControl()
        self.dialog_widget._guiApplyDbtn.setEnabled(False)

    def signals(self):

        self.uiLoadGdbPbtn.clicked.connect(self.loadGdbDaten)

    def loadGisLayer(self):

        with DbSession.session_scope() as session:
            session.expire_on_commit = False

            scope_layer_inst = session.query(BGisScopeLayer)\
                .filter(BGisScopeLayer.gis_scope_id == 2)\
                .order_by(desc(BGisScopeLayer.order))\
                .all()

        self.guiMainGis.loadLayer(scope_layer_inst)


    def setLoadTime(self, time):
        """
        trage die Zeit für den gdb-import in der datenbank ein
        """

        with DbSession.session_scope() as session:
            time_sys_query = session.query(BSys).filter(BSys.key == 'last_gdb_import').first()
            time_sys_query.value = str(time)

            session.commit()

    def getLoadTime(self):
        """
        erhalte die Zeit des letzten gdb-importes aus der alm_sys tabelle
        """
        with DbSession.session_scope() as session:
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

        with DbSession.session_scope() as session:

            zuord_query = session.query(BGst.id)\
                .join(BGstZuordnung) \
                .filter(BGstZuordnung.akt_id == self.akt_id)\
                .all()
        """erzeuge eine liste mit den id's aus dem query (=list in list)"""
        self.akt_zugeordnete_gst = [r[0] for r in zuord_query]
        """"""

    def loadGdbDaten(self):
        """
        lösche zuerst alle ungenutzten Gst-Daten;
        lade dann alle Gst-Daten die sich im GDB-Importverzeichnis befinden;
        :return:
        """
        self.deleteUnusedGst()

        self.loading_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        """erstelle eine Liste mit den dateien im importverzeichnis:"""
        gdb_files = [f for f in listdir(config.gdb_import_path) if isfile(join(config.gdb_import_path, f))]
        """"""

        self.gst_geometries = {}  # dict für die geomentrien

        self.ez_import_path = []  # liste der ez's im import-pfad (ez als base-class)

        with DbSession.session_scope() as session:
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
                    zip_file = zipfile.ZipFile(str(config.gdb_import_path.absolute() / file), 'r')
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

        """lade die Gst-Tabelle:"""
        self.guiGstTable.updateMaintable()
        """"""

        """aktualisiere main_gis"""
        self.guiMainGis.uiCanvas.update()
        self.guiMainGis.uiCanvas.refresh()
        """"""

    def importGdbDaten(self):
        """
        importiere die Gdb-Daten, die in die Liste self.ez_import_path geladen wurden
        """
        with DbSession.session_scope() as session:

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
                                    new_nutz = BGstNutzung(ba_id=nutz.ba_id,
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
                                    new_nutz = BGstNutzung(ba_id=nutz.ba_id,
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
                                    new_nutz = BGstNutzung(ba_id=nutz.ba_id,
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

                ba_id = gst_row[3]
                nu_id = gst_row[4]
                flaeche = gst_row[7]

                kg_gst = str(kgnr) + str(gst)

                """pro csv-zeile wird auf jeden fall eine ba-instanz erzeugt"""
                nutzung_instance = BGstNutzung(ba_id=ba_id,
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
            # headers = next(read_eig_csv, None)  # erhalte eine liste mit den Spaltennamen

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

            accept_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            """übernehme die markierten Gst in die GDB-Tabelle (inkl. EZ, Eigentuemer u. Nutzungen)"""
            with DbSession.session_scope() as session:
                session.expire_on_commit = False
                for gst_instance in self.checked_gst_instances:

                    gst_zuordnung = BGstZuordnung(akt_id=self.parent.parent.entity_id,
                                                  gst_id=gst_instance.id,
                                                  awb_status_id=awb_status,
                                                  rechtsgrundlage_id=rechtsgrundlage,
                                                  anmerkung=anm,
                                                  probleme=problem,
                                                  time=accept_time)
                    session.add(gst_zuordnung)

            session.commit()
            """"""

            """update den akt"""
            self.parent.parent.updateAkt()
            """"""

    def deleteUnusedGst(self):
        """
        lösche Gst-Daten aus der db die nicht genutzt werden
        (keinem akt zugewiesen sind);

        mache die aus performace-gründen direkt in der db
        """

        with DbSession.session_scope() as session:

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

class GstTable(MainTable):
    """
    tabelle mit den grundstücken die zugeordnet werden können bzw. bereits
    zugeordnet sind
    """

    gis_relation = {"gis_id_column": 0,
                    "gis_layer_style_id": 108,
                    "gis_layer_id_column": 'id'}

    _data_view = MainTableView

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.available_filters = 'gs'

        self.maintable_text = ["Grundstück", "Grundstücke", "kein Grundstück"]

    def initUi(self):
        super().initUi()

        self.uiAddDataTbtn.setVisible(False)
        self.uiEditDataTbtn.setVisible(False)
        self.uiDeleteDataTbtn.setVisible(False)

        self.guiGstChecked = QLabel()
        self.uiFooterSubVlay.addWidget(self.guiGstChecked)

    def finalInit(self):
        super().finalInit()

        # """setzt bestimmte spaltenbreiten"""
        # self.guiMainTableTvw.setColumnWidth(4, 200)
        # self.guiMainTableTvw.setColumnWidth(6, 200)
        # self.guiMainTableTvw.setColumnWidth(7, 130)
        # """"""
        """passe die Zeilenhöhen an den Inhalt an"""
        self.maintable_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        """"""

    def setMaintableColumns(self):
        super().setMaintableColumns()

        self.maintable_columns[0] = MaintableColumn(column_type='int',
                                                    visible=False)
        self.maintable_columns[1] = MaintableColumn(column_type='str',
                                                    visible=False)
        self.maintable_columns[2] = MaintableColumn(column_type='str',
                                                    heading='Gst')
        self.maintable_columns[3] = MaintableColumn(heading='KG-Nr',
                                                    column_type='int')
        self.maintable_columns[4] = MaintableColumn(heading='KG-Name',
                                                    column_type='str')
        self.maintable_columns[5] = MaintableColumn(heading='EZ',
                                                    column_type='int')
        self.maintable_columns[6] = MaintableColumn(heading="bereits zugeordnet zu",
                                                    column_type='str')
        self.maintable_columns[7] = MaintableColumn(heading='Datenstand',
                                                    column_type='str')
        self.maintable_columns[8] = MaintableColumn(heading='Importzeit',
                                                    column_type='str')
        self.maintable_columns[9] = MaintableColumn(column_type='str',
                                                    visible=False)

    def getMainQuery(self, session=None):
        super().getMainQuery(session)

        query = session.query(BGstZuordnungMain.id,
                              BGstZuordnungMain.kg_gst,
                              BGstZuordnungMain.gst,
                              BGstZuordnungMain.kgnr,
                              BGstZuordnungMain.kg_name,
                              BGstZuordnungMain.ez,
                              BGstZuordnungMain.zu_aw,
                              BGstZuordnungMain.datenstand,
                              BGstZuordnungMain.import_time,
                              BGstZuordnungMain)

        return query

    def setMainTableModel(self):
        super().setMainTableModel()

        return GstMainModel(parent=self, data_array=self.maintable_dataarray)

    def setFilterScopeUI(self):
        super().setFilterScopeUI()

        """filter ez"""
        self.guiFilterEzLbl = QLabel("Ez:")
        self.guiFilterEzCombo = QComboBox(self)

        self.uiTableFilterHLay.insertWidget(2, self.guiFilterEzLbl)
        self.uiTableFilterHLay.insertWidget(3, self.guiFilterEzCombo)
        """"""

        """filter kg name"""
        self.guiFilterKgNameLbl = QLabel("Kg-Name:")
        self.guiFilterKgNameCombo = QComboBox(self)

        self.uiTableFilterHLay.insertWidget(2, self.guiFilterKgNameLbl)
        self.uiTableFilterHLay.insertWidget(3, self.guiFilterKgNameCombo)
        """"""

        """filter kgnr"""
        self.guiFilterKgLbl = QLabel("Kg-Nr:")
        self.guiFilterKgCombo = QComboBox(self)

        # self.uiFilterScopeHLay.insertWidget(0, self.guiFiltRechtsverhLbl)
        self.uiTableFilterHLay.insertWidget(2, self.guiFilterKgLbl)
        self.uiTableFilterHLay.insertWidget(3, self.guiFilterKgCombo)
        """"""

    def setFilterScope(self):
        super().setFilterScope()

        self.setFilterKgnr()
        self.setFilterKgName()
        self.setFilterEz()

    def setFilterKgnr(self):

        with DbSession.session_scope() as session:
            item_query = session.query(BGstEz.kgnr).distinct()

        try:
            self.guiFilterKgCombo.currentTextChanged.disconnect(
                self.filterMaintable)
        except:
            pass
        finally:
            prev_typ = self.guiFilterKgCombo.currentText()
            self.guiFilterKgCombo.clear()

            self.guiFilterKgCombo.addItem('- Alle -')
            for item in sorted(item_query):
                self.guiFilterKgCombo.addItem(str(item[0]))

            self.guiFilterKgCombo.setCurrentText(prev_typ)

            self.guiFilterKgCombo.currentTextChanged.connect(
                self.applyFilter)

    def setFilterKgName(self):

        with DbSession.session_scope() as session:
            item_query = session.query(BKatGem.kgname).join(BGstEz).distinct()

        try:
            self.guiFilterKgNameCombo.currentTextChanged.disconnect(
                self.filterMaintable)
        except:
            pass
        finally:
            prev_typ = self.guiFilterKgNameCombo.currentText()
            self.guiFilterKgNameCombo.clear()

            self.guiFilterKgNameCombo.addItem('- Alle -')
            for item in sorted(item_query):
                self.guiFilterKgNameCombo.addItem(str(item[0]))

            self.guiFilterKgNameCombo.setCurrentText(prev_typ)

            self.guiFilterKgNameCombo.currentTextChanged.connect(
                self.applyFilter)

    def setFilterEz(self):

        with DbSession.session_scope() as session:
            item_query = session.query(BGstEz.ez).distinct()

        try:
            self.guiFilterEzCombo.currentTextChanged.disconnect(
                self.filterMaintable)
        except:
            pass
        finally:
            prev_typ = self.guiFilterEzCombo.currentText()
            self.guiFilterEzCombo.clear()

            self.guiFilterEzCombo.addItem('- Alle -')
            for item in sorted(item_query):
                self.guiFilterEzCombo.addItem(str(item[0]))

            self.guiFilterEzCombo.setCurrentText(prev_typ)

            self.guiFilterEzCombo.currentTextChanged.connect(
                self.applyFilter)

    def useFilterScope(self, source_row, source_parent):
        super().useFilterScope(source_row, source_parent)

        try:
            """filter KgNr"""
            table_value = self.filter_proxy.sourceModel() \
                .data(self.filter_proxy.sourceModel().index(source_row, 3),
            Qt.DisplayRole)
            if self.guiFilterKgCombo.currentText() != "- Alle -":
                if str(table_value) != self.guiFilterKgCombo.currentText():
                    return False
            """"""

            """filter KgName"""
            table_value = self.filter_proxy.sourceModel() \
                .data(self.filter_proxy.sourceModel().index(source_row, 4),
            Qt.DisplayRole)
            if self.guiFilterKgNameCombo.currentText() != "- Alle -":
                if str(table_value) != self.guiFilterKgNameCombo.currentText():
                    return False
            """"""

            """filter Ez"""
            table_value = self.filter_proxy.sourceModel() \
                .data(self.filter_proxy.sourceModel().index(source_row, 5),
            Qt.DisplayRole)
            if self.guiFilterEzCombo.currentText() != "- Alle -":
                if str(table_value) != self.guiFilterEzCombo.currentText():
                    return False
            """"""
        except:
            print("Filter Error:", sys.exc_info())

class GstMainModel(MainTableModel):

    col_with_kg_gst_value = 0
    col_with_checkbox = 2

    def __init__(self, parent, data_array=None):
        super(__class__, self).__init__(parent, data_array)

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

        """setze den check-status"""
        if role == Qt.CheckStateRole:
            if index.column() == 2:
                return self.checkState(QModelIndex(index))
        """"""

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

        if role == Qt.CheckStateRole:

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

            """zeige die anzahl der neu zugeordneten gst:"""
            self.setCheckedGstLabel()
            """"""
            return True
        return False

    def setCheckedGstLabel(self):
        """
        setze den wert für die anzahl der markierte grundstücke und passe
        die dialog-buttons an die aktuelle situation an
        """

        while self.parent.parent.uiVorgemerkteGstVlay.count():
            child = self.parent.parent.uiVorgemerkteGstVlay.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if len(self.parent.parent.checked_gst_instances) > 0:
            vorgemerkt_text = QLabel()
            vorgemerkt_text.setText(str(len(self.parent.parent.checked_gst_instances))+ ' Grundstücke vorgemerkt:')
            self.parent.parent.uiVorgemerkteGstVlay.addWidget(vorgemerkt_text)
            self.parent.parent.uiVorgemerkteGstVlay.addWidget(QLabel())

            for gst in self.parent.parent.checked_gst_instances:
                gst_label = QLabel()
                gst_label.setText(gst.gst)
                self.parent.parent.uiVorgemerkteGstVlay.addWidget(gst_label)

            self.parent.parent.dialog_widget._guiApplyDbtn.setEnabled(True)
            self.parent.parent.dialog_widget.set_reject_button_text('&Abbrechen')
        else:
            self.parent.parent.dialog_widget._guiApplyDbtn.setEnabled(False)
            self.parent.parent.dialog_widget.set_reject_button_text('&Schließen')

    def flags(self, index):

        if not index.isValid():
            return None

        if index.column() == self.col_with_checkbox:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable


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