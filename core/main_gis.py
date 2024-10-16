import os
import sys
from pathlib import Path

from qgis.PyQt.QtCore import Qt, QSize, QEvent
from qgis.PyQt.QtGui import QIcon, QStandardItemModel, QStandardItem, QColor
from qgis.PyQt.QtWidgets import QWidget, QMenu, QAction, QToolButton, \
    QFileDialog, QMessageBox, QDockWidget, QMainWindow, QSizePolicy, \
    QHBoxLayout, QToolBar, QDialog, QApplication
from qgis.PyQt.QtXml import QDomDocument

from core import main_gis_UI, db_session_cm, config, color

from qgis.core import QgsCoordinateReferenceSystem, QgsProject, QgsLayerTreeModel,\
    QgsLayerTreeLayer, QgsExpressionContextUtils, QgsLayout, QgsVectorLayer, \
    QgsReadWriteContext, QgsLayoutItemPage, QgsLayoutExporter, QgsVectorFileWriter

from qgis.gui import QgsLayerTreeView, QgsLayerTreeMapCanvasBridge, QgsMapToolPan, \
    QgsMapToolZoom, QgsMapToolIdentifyFeature, QgsMapToolIdentify, QgsMessageBar, \
    QgsAdvancedDigitizingDockWidget, QgsMapToolDigitizeFeature, QgsMapToolCapture, \
    QgsMapCanvas

from core.data_model import BGisStyle, BGisLayerMenu
from core.gis_layer import getGisLayer, setLayerStyle
from core.main_dialog import MainDialog
from core.print_content_widget import PrintContentWidget

from core.gis_tools import cut_koppel_gstversion


class MainGis(QMainWindow, main_gis_UI.Ui_MainGis):

    _background_instance = None
    _base_layer = None
    _layers = []
    _current_layer = None

    _base_id = None

    scope_id = None

    """eine klasse mit der z.b. ein gis-layer mit einer tabelle verknüpft
    werden kann"""
    gis_control_widget = None
    """"""

    @property  # getter
    def background_instance(self):

        return self._background_instance

    @background_instance.setter
    def background_instance(self, value):
        """
        setter für den hintergrundlayer
        """

        """entferne den bisherigen hintergrundlayer, wenn einer da ist"""
        for lay in self.project_instance.mapLayers().values():
            if hasattr(lay, 'back'):
                if lay.back:
                    self.project_instance.removeMapLayer(lay.id())
        """"""

        """lade den neuen hintergrundlayer und füge ihn in die projekt-instanz
        ein"""
        b_layer = getGisLayer(layer_instance=value)
        b_layer.back = True
        self.addLayer(b_layer)

        """"""

        self._background_instance = value

    @property  # getter
    def base_layer(self):
        return self._base_layer

    @base_layer.setter
    def base_layer(self, value):
        self._base_layer = value

    @property  # getter
    def base_id(self):
        return self._base_id

    @base_id.setter
    def base_id(self, value):
        self._base_id = value

    @property  # getter
    def layers(self):

        return self._layers

    @layers.setter
    def layers(self, value):

        self._layers = value

    @property  # getter
    def current_layer(self):

        return self._current_layer

    @current_layer.setter
    def current_layer(self, value):
        """
        setter für den aktuellen layer
        """

        """aktiviere den 'actionAddFeature' button, wenn die eigenschaft
        'add' in der tabelle 'a_gis_scope_layer' auf True gesetzt ist
        funktioniert derzeit nur mit dem 'komplexe' layer (v.a. das umschalten
        im 'Akt' auf die entsprechende tabelle
        """
        if hasattr(value, 'add'):
            if value.add:
                self.actionAddFeature.setEnabled(True)
                try:
                    self.parent.parent().tabAkt.setCurrentIndex(3)
                except:
                    print(f"Error: {sys.exc_info()}")
            else:
                self.actionAddFeature.setEnabled(False)
        """"""
        self._current_layer = value

    def __init__(self, parent=None, gis_control=None, base_id=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent
        self.maingis_session = None
        self.gis_control_widget = gis_control
        self.base_id = base_id

        """erzeuge ein QgsLayerTreeView"""
        self.layer_tree_view = QgsLayerTreeView(self)
        """"""

        """richte das canvas ein; das darauf passierende widget 'QgsMapCanvas'
        ist im ui-file mit dem qt-designer als centralWidget bereits eingefügt
        geworden"""
        self.uiCanvas.setCanvasColor(Qt.white)
        crs = QgsCoordinateReferenceSystem("EPSG:31259")
        self.uiCanvas.setDestinationCrs(crs)
        """"""

        """setzte die selektions-farbe"""
        self.uiCanvas.setSelectionColor(color.canvas_selection)

        """erzeuge eine projekt-instanz"""
        self.project_instance = QgsProject()
        """"""

        """erzeuge einige tools, damit z.b. eine legende dargestellt werden
        kann"""
        self.layer_tree_root = self.project_instance.layerTreeRoot()

        self.bridge = QgsLayerTreeMapCanvasBridge(self.layer_tree_root, self.uiCanvas)
        self.layertree_root_group = self.bridge.rootGroup()

        self.layer_tree_model = QgsLayerTreeModel(self.layer_tree_root)
        self.layer_tree_model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.layer_tree_model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.layer_tree_model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.layer_tree_model.setFlag(QgsLayerTreeModel.ShowLegend)

        self.layer_tree_view.setModel(self.layer_tree_model)
        """"""

        """"erzeuge eine QgsMessageBar"""
        self.messagebar = MessageBar(self.uiCanvas)
        """"""

        """erzeuge eine legende und füge sie auf der rechten seite ein"""
        self.legend_dock = LegendDock(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.legend_dock)

        """entferne die 'angreifer' im eck rechts unten die die größenänderung
        des widgets sichtbar machen"""
        self.statusBar().setSizeGripEnabled(False)
        """"""

        """erzeuge ein 'AdvancedDigitizingDockWidget'"""
        self.digi_dock = QgsAdvancedDigitizingDockWidget(self.uiCanvas)
        """"""

        self.actionAddFeature.setEnabled(False)
        self.setToolbarBasic()

        """activiere pan standardmässig"""
        self.pan()
        """"""
        self.signals()

        self.setMinimumWidth(900)

    def currentLayerChanged(self):
        """
        wird ausgeführt wenn die auswahl eines layers im layer_tree_view
        geändert wird
        :return:
        """

        """wenn das 'SelectFeature' aktiv ist dann entferne die bisherige
        auswahl und aktiviere das tool wieder"""
        if self.actionSelectFeature.isChecked():
            self.removeSelectedAll()
            self.activateSelectFeature()
        """"""

        """setze die eigenschaft 'current_layer' """
        self.current_layer = self.layer_tree_view.currentLayer()
        """"""

    def setToolbarBasic(self):
        """
        passe die toolbar 'uiBasicToolbar' an
        """

        """füge einen platzhalter ein"""
        emty_wid_01 = QWidget(self)
        emty_wid_01.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Preferred)
        self.uiBasicToolbar.addWidget(emty_wid_01)
        """"""

        """füge einen button zum einfügen von internen layer ein"""
        self.add_alm_layer = QToolButton(self)
        self.add_alm_layer.setIcon(QIcon(":/svg/resources/icons/mActionAdd_2.svg"))
        self.add_alm_layer.setToolTip('füge einen Layer aus dem Datenbestand<br>'
                                      'des <b>NÖ Alminspektorates</b> ein')
        self.add_alm_layer.setIconSize(QSize(25, 25))
        self.add_alm_layer.setPopupMode(QToolButton.InstantPopup)
        self.uiBasicToolbar.addWidget(self.add_alm_layer)
        """"""

        """lade den menübaum zum einfügen interner layer"""
        menu_abb = self.getLayerMenu(2)
        self.add_alm_layer.setMenu(menu_abb)
        """"""

        """füge einen button zum einfügen von externer layer ein"""
        self.add_layer_tbtn = QToolButton(self)
        self.add_layer_tbtn.setIcon(QIcon(":/svg/resources/icons/mActionAdd.svg"))
        self.add_layer_tbtn.setToolTip('füge einen <b>externen</b> Layer ein')
        self.add_layer_tbtn.setIconSize(QSize(25, 25))
        self.add_layer_tbtn.setPopupMode(QToolButton.InstantPopup)
        self.uiBasicToolbar.addWidget(self.add_layer_tbtn)
        """"""

        """lade den menübaum zum einfügen externer layer"""
        menu = self.getLayerMenu(1)
        self.add_layer_tbtn.setMenu(menu)
        """"""

        """füge einen button zum einfügen von hintergrund-layer ein"""
        self.add_back_layer = QToolButton(self)
        self.add_back_layer.setIcon(QIcon(":/svg/resources/icons/mActionAdd_3.svg"))
        self.add_back_layer.setToolTip('füge einen <b>Hintergrundlayer</b> ein')
        self.add_back_layer.setIconSize(QSize(25, 25))
        self.add_back_layer.setPopupMode(QToolButton.InstantPopup)
        self.uiBasicToolbar.addWidget(self.add_back_layer)
        """"""

        """lade den menübaum zum einfügen von hintergrund-layer"""
        self.setBackgroundComboData()
        """"""

        """füge einen platzhalter ein"""
        emty_wid_02 = QWidget(self)
        emty_wid_02.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Preferred)
        self.uiBasicToolbar.addWidget(emty_wid_02)
        """"""

        """füge einen button ein um ein losgelöstes GisDock zum ursprüglichen
        platz zurück zu bewegen"""
        self.uiUnfoatDock = QAction(QIcon(":/svg/resources/icons/unfloat_dock.svg"),
                                    'platziere die Kartenansicht am ursprünglichen Platz')
        self.uiUnfoatDock.setVisible(False)
        self.uiBasicToolbar.addAction(self.uiUnfoatDock)
        """"""

        """füge einen button für das hauptmenü ein"""
        self.uiMainMenuTbtn = QToolButton(self)
        self.uiMainMenuTbtn.setIcon(QIcon(":/svg/resources/icons/hamburger.svg"))
        self.uiMainMenuTbtn.setIconSize(QSize(25, 25))
        self.uiMainMenuTbtn.setPopupMode(QToolButton.InstantPopup)
        self.setMainMenu()
        self.uiBasicToolbar.addWidget(self.uiMainMenuTbtn)
        """"""

    def getLayerMenu(self, menu_id):
        """
        erzeuge einen menü-baum mit layern die den übergebenen menu_id haben;
        die daten werden aus dem daten-model 'BGisLayerMenu' geholt

        :return: QMenu
        """

        with db_session_cm() as session:

            menu_query = session.query(BGisLayerMenu)\
                .filter(BGisLayerMenu.menu_id == menu_id)\
                .all()

            """erzeuge ein menu"""
            menu = QMenu(self)
            """"""

            """erzeuge ein QStandardItemModel in dem die menü-einträge zwischen 
            eingelesen werden"""
            self.menu_tree = QStandardItemModel(self)
            self.menu_tree.setColumnCount(2)
            """"""

            """definiere das unsichtbare root-element des menu_tree_models"""
            self.root_item = self.menu_tree.invisibleRootItem()
            """"""

            self.createMenuTree(menu_query)  # ein menu-tree von QStandardItem's

            # """zeige für tests den menu-tree als QTreeView"""
            # self.test_view = QTreeView()
            # self.test_view.setModel(self.menu_tree)
            # self.test_view.expandAll()
            # self.test_view.resizeColumnToContents(0)
            # self.test_view.show()
            # """"""

            """erstelle den menu-tree"""
            self.addMenuItem(menu, self.root_item)
            """"""

        return menu

    def createMenuTree(self, element_list):
        """erzeuge die menü-baum struktur in einem QStandardItemModel;
        dazu wird die liste mit den menü-elementen solange durchlaufen,
        bis alle child-elemente einem parent-element zugeordnet sind"""

        """add the elements to the item-tree and make list of the added
        elements"""
        remove_elements = []  # liste mit bereits eingefügten elementen
        for element in element_list:
            node = QStandardItem(str(element.id))

            node.name = element.name
            node.instance = element
            node.parent_id = element.parent_id
            sort = QStandardItem(str(element.sort))

            if element.parent_id == 0:
                self.root_item.appendRow([node, sort])
                remove_elements.append(element)
            else:
                items = self.menu_tree.findItems(str(element.parent_id),
                                                 Qt.MatchRecursive, 0)
                if items != []:
                    for k in range(len(items)):
                        items[k].appendRow([node, sort])
                        remove_elements.append(element)
        """"""

        """kontrolliere ob es elemente gibt, die nicht eingefügt wurden"""
        left_elements_list = []  # liste mit übrigen elementen
        for z in element_list:
            if z not in remove_elements:
                left_elements_list.append(z)
        """"""

        """wiederhole diese methode solange bis alle elemente im menü-baum 
        eingefügt wurden"""
        if not left_elements_list:
            return
        else:
            self.createMenuTree(left_elements_list)
        """"""

    def addMenuItem(self, parent_menu, menu_item):
        """
        erstelle das Menu mit Menu-Elementen und Aktionen;
        füge dieses menu an das gegebene parent_menu an;
        menu_item ist das root_Standarditem des menu_tree's

        :param: paent_menu = QMenu
        :param: menu_item = QStandardItem
        """

        if menu_item.hasChildren():  # einträge die einen menü-punkt darstellen
            menu_item.sortChildren(1)  # sortiere die children nach der spalte 1
            if menu_item == self.root_item:  # erstelle die 1. menü-ebene
                for r in range(menu_item.rowCount()):
                    self.addMenuItem(parent_menu, menu_item.child(r))
            else:  # erstelle die weiteren menü-einträge
                men = parent_menu.addMenu(menu_item.instance.name)
                for m in range(menu_item.rowCount()):
                    self.addMenuItem(men, menu_item.child(m))
        else:
            try:
                """die 'top-level-items' werden eingefügt"""
                action = QAction(self)
                action.setText(menu_item.instance.name)
                parent_menu.addAction(action)

                action.triggered.connect(
                    lambda x, style_inst=menu_item.instance.rel_gis_style:
                    self.loadLayerByStyle(style_instance=style_inst)
                )
                """"""
            except:
                print(f"Error: {sys.exc_info()}")

    def loadLayerByStyle(self, style_instance):
        """
        lade einen gis-layer mit einer layer_style instanz
        """
        layer = getGisLayer(style_instance)

        if style_instance.qml_file:
            setLayerStyle(layer, style_instance.qml_file)

        self.addLayer(layer)

    def setBackgroundComboData(self):
        """
        erstelle das menu zu laden der hintergrundlayer
        """

        back_menu = QMenu()

        with db_session_cm() as session:
            session.expire_on_commit = False

            lay = session.query(BGisStyle)\
                .filter(BGisStyle.background == 1)\
                .all()

        for item in lay:
            background_item = QAction(self)
            background_item.setText(item.rel_gis_layer.name + ' (' + item.name + ')')
            background_item.triggered.connect(
                lambda x, inst=item: self.setBackground(inst))

            back_menu.addAction(background_item)

        self.add_back_layer.setMenu(back_menu)

    def setBackground(self, layer_instance):

        self.background_instance = layer_instance

    def signals(self):

        self.actionSelectFeature.triggered.connect(self.activateSelectFeature)
        self.actionFeatureInfo.triggered.connect(self.displayFeatureInfo)

        self.actionPan.triggered.connect(self.pan)
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionZoomBase.triggered.connect(self.pan_baselayer)
        self.actionZoomToLayer.triggered.connect(self.zoomToLayer)
        self.actionZoomToSelected.triggered.connect(self.zoomToSelected)
        self.actionDelSelection.triggered.connect(self.removeSelectedAll)

        self.uiUnfoatDock.triggered.connect(self.unfloatDock)

        self.actionAddFeature.triggered.connect(self.addGisFeature)

        self.layer_tree_view.currentLayerChanged.connect(
            self.currentLayerChanged)

        self.print_manager.triggered.connect(self.printCanvasToPdf)

    def unfloatDock(self):
        """
        beende den float-modus des docks und bewege es zurück zur letzten Position
        """
        self.parent.setFloating(False)

    def setMainMenu(self):
        """
        füge einträge im hauptmenü ein
        """

        self.main_menu = QMenu(self)

        self.load_project = QAction(QIcon(":/svg/resources/icons/mActionFileOpen.svg"),
                                    'öffne Projekt')
        self.load_project.triggered.connect(self.openProject)
        self.main_menu.addAction(self.load_project)

        self.save_project = QAction(QIcon(":/svg/resources/icons/mActionFileSaveAs.svg"),
                                    'speichere als Projekt')
        self.save_project.triggered.connect(self.saveProject)
        self.main_menu.addAction(self.save_project)

        self.load_layer = QAction(QIcon(":/svg/resources/icons/mActionDataSourceManager.svg"),
                                  'beliebigen Layer hinzufügen')
        self.load_layer.triggered.connect(self.addCustomLayer)
        self.main_menu.addAction(self.load_layer)

        self.export = QMenu('Export')
        self.main_menu.addMenu(self.export)

        self.save_layer = QAction(QIcon(":/svg/resources/icons/export_layer.svg"),
                                  'Layer speichern als ...')
        self.save_layer.triggered.connect(self.exportLayer)
        self.export.addAction(self.save_layer)

        self.main_menu.addSeparator()

        self.print_manager = QAction(QIcon(":/svg/resources/icons/mActionFilePrint.svg"),
                                     'Kartenansicht drucken')
        self.main_menu.addAction(self.print_manager)

        self.uiMainMenuTbtn.setMenu(self.main_menu)

    def exportLayer(self):
        """
        exportiere den ausgewählten Layer
        :return:
        """



        if self.current_layer:
            QgsVectorFileWriter.writeAsVectorFormat(layer=self.current_layer,
                                                    fileName='C:/work/gst.gpkg',
                                                    fileEncoding='utf-8',
                                                    destCRS=self.current_layer.crs(),
                                                    driverName='GPKG')

        print(self.current_layer)

    def loadLayer(self, layer_instance_list):
        """
        lade gis-layer mithilfe der übergebenen 'layer_instance_list';
        diese liste enthält instanzen des daten-models 'BGisScopeLayer';
        mit der base_id kann ein filter auf features durchgeführt werden

        :param layer_instance_list:
        :return:
        """
        for scope_layer_instance in layer_instance_list:

            layer_style_inst = scope_layer_instance.rel_gis_style

            """wenn ein 'id_value' eingetragen ist, dann filtere die objekte
            darauf in der ebenfalls eingetragenen spalte 'id_column' """
            if scope_layer_instance.base_id_column or scope_layer_instance.feat_filt_expr:

                gis_layer = getGisLayer(
                    layer_instance=layer_style_inst,
                    base_id_column=scope_layer_instance.base_id_column,
                    id_val=self.base_id,
                    feat_filt_expr=scope_layer_instance.feat_filt_expr)
            else:
                gis_layer = getGisLayer(layer_instance=layer_style_inst)

            """setze instanz-eigenschaften, die für die weitere verwendung
            notwendig sind"""
            gis_layer.style_id = layer_style_inst.id
            gis_layer.dataform_modul = layer_style_inst.dataform_modul
            gis_layer.dataform_class = layer_style_inst.dataform_class

            gis_layer.base = scope_layer_instance.baselayer
            gis_layer.back = scope_layer_instance.background
            gis_layer.add = scope_layer_instance.add
            """"""

            """lade das style-file"""
            if layer_style_inst.qml_file:
                setLayerStyle(gis_layer, layer_style_inst.qml_file)
            """"""

            """setzte die layer_variablen, falls für diesen layer_style welche
            gesetzt sind (im daten-model 'BGisStyleLayerVar') """
            if layer_style_inst.rel_gis_style_layer_var:

                for layer_var in layer_style_inst.rel_gis_style_layer_var:

                    if layer_var.code_value == True:
                        var_value = getattr(self, layer_var.value)
                    else:
                        var_value = layer_var.value

                var_name = layer_var.name

                QgsExpressionContextUtils.setLayerVariable(gis_layer,
                                                           var_name,
                                                           var_value)
            """"""

            # """setzte die layer_variablen, falls für diesen layer_style welche
            # gesetzt sind (im daten-model 'BGisStyleLayerVar') """
            # if layer_style_inst.rel_gis_style_layer_var:
            #
            #     for layer_var in layer_style_inst.rel_gis_style_layer_var:
            #
            #         if layer_var.code_value == True:
            #             var_value = getattr(self, layer_var.value)
            #             expression1 = f'jahr={var_value}'
            #
            #             expression2 = '"akt_id"=54'
            #             expression = expression1 + ' and ' + expression2
            #
            #             # test_obj = eval('self.parent.parent()')
            #             # test_val = getattr(test_obj, 'komplex_jahr')
            #
            #             gis_layer.setSubsetString(expression)
            #         else:
            #             var_value = layer_var.value
            #
            #     var_name = layer_var.name
            #
            #     QgsExpressionContextUtils.setLayerVariable(gis_layer,
            #                                                var_name,
            #                                                var_value)
            # """"""

            """modifiziere die namen die im layer_tree_view angezeigt
            werden"""
            if scope_layer_instance.baselayer:
                name = gis_layer.name()
                gis_layer.setName(name + ' (Basislayer)')
            if scope_layer_instance.background:
                name = gis_layer.name()
                gis_layer.setName(name + ' (Hintergrund)')
            """"""

            self.addLayer(gis_layer)

    def addLayer(self, layer, group=None, treeview_only=False):
        """
        füge den layer ins projekt ein;
        Wenn 'treeview_only' True ist, wird der Layer nur im Layer-Tree-View
        und nicht in die Projekt-Instance eingefügt. Der Layer muss in diesem
        Fall selbstständig vorher (!!) in die Projekt-Instance eingefügt
        werden (mit self.project_instance.addMapLayer(...))!!!

        :param layer:
        :param group:
        :param treeview_only: bool
        :return:
        """

        """falsch der layer ungültig ist, dann zeige eine wahrnung;
        an"""
        if not layer.isValid():
            self.messagebar.pushMessage(
                "Achtung",
                f"Der Layer '{layer.name()}' kann nicht geladen werden",
                level=1,
                duration=15)
        else:
            """setze die eigenschaft 'base_layer' wenn er einer ist"""
            if hasattr(layer, 'base'):
                if layer.base:
                    self.base_layer = layer
            """"""

            """füge den Layer in das Projekt ein (aber nicht sichtbar!)"""
            if not treeview_only:
                self.project_instance.addMapLayer(layer, False)
            """"""

            """positioniere den Layer entsprechend der Vorgaben im Layertree"""
            if layer.back:
                self.layertree_root_group.insertChildNode(
                    -1, QgsLayerTreeLayer(layer))
            else:
                if group is not None:
                    group.addLayer(layer)
                else:
                    self.layertree_root_group.insertChildNode(
                        -1,
                        QgsLayerTreeLayer(layer))
            """"""

            """falls ein base-layer eingefügt wird, dann verschiebe den 
            kartenausschnitt auf diesen"""
            if layer.base:
                extent = layer.extent()
                self.uiCanvas.setExtent(extent)

            self.uiCanvas.refresh()

    def removeLayer(self):

        sel_layer = self.layer_tree_view.selectedLayers()

        for layer in sel_layer:

            # if hasattr(layer, 'back'):
            #     if layer.back:
            #         self.BackgroundCombo.setCurrentIndex(0)

            if hasattr(layer, 'base'):
                if layer.base:
                    self.msgRemoveBaselayer()
                else:
                    self.project_instance.removeMapLayer(layer.id())
            else:
                self.project_instance.removeMapLayer(layer.id())

        self.uiCanvas.refresh()

    def removeLayersAll(self):
        """
        remove all layers from the current project
        :return:
        """
        layers = self.project_instance.mapLayers().values()

        for layer in layers:
            self.project_instance.removeMapLayer(layer)

    def openProject(self):

        o_fd = QFileDialog()
        o_fd.setFileMode(QFileDialog.ExistingFiles)

        project_file = o_fd.getOpenFileName(self, "wähle Projekt", "",
                                                       "*.qgz")

        if project_file[0]:
            self.removeLayersAll()
            self.project_instance.read(project_file[0])
            self.uiCanvas.refresh()

    def saveProject(self):

        s_fd = QFileDialog()

        save_project_file = s_fd.getSaveFileName(self, 'speichere als externes Projekt',
                                               'C:/work/Projekte/AlmGIS_uni/data',
                                               "Qgis-Projekt (*.qgz)")

        if save_project_file[0]:
            self.project_instance.write(save_project_file[0])

    def addCustomLayer(self):
        """
        füge einen beliebigen geopackage- oder shp-layer in das projekt ein
        """

        fd = QFileDialog()

        layer_file = fd.getOpenFileName(self, "wähle Layer", "", "*.gpkg;;*.shp")

        if layer_file[0]:

            layer_name = Path(layer_file[0]).name
            vlayer = QgsVectorLayer(layer_file[0], layer_name, "ogr")

            if not vlayer.isValid():
                self.messagebar.pushMessage(
                    "Achtung",
                    f"Der Layer '{layer_name}' kann nicht geladen werden",
                    level=1,
                    duration=15)
            else:
                self.project_instance.addMapLayer(vlayer)
                self.uiCanvas.refresh()

    def msgRemoveBaselayer(self):
        """
        nachricht falls ein base-layer entfernt werden soll
        """

        msg = QMessageBox()
        msg.setText("Der Basislayer dieser Kartenansicht kann nicht "
                    "gelöscht werden. Er kann nur unsichtbar gemacht werden.")
        msg.exec_()

    def printCanvasToPdf(self):
        """
        erzeuge eine pdf-Datei aus einer Druckvorlage
        :return:
        """
        self.print_widget = PrintContentWidget(self)

        self.print_dialog = MainDialog(self)
        self.print_dialog.enableApply = True
        self.print_dialog.set_apply_button_text('&Drucken')
        self.print_dialog.insertWidget(self.print_widget)

        result = self.print_dialog.exec()

        if result:
            """hole die druckvorlage"""
            template = Path(str(config.print_template_path.absolute() / "A3quer.qpt"))

            with open(template, 'r') as file:
                page = file.read()

            """erzeuge ein layout"""
            doc = QDomDocument()
            doc.setContent(page)

            project = self.project_instance
            layout = QgsLayout(project)
            layout.initializeDefaults()
            layout.loadFromTemplate(doc, QgsReadWriteContext(), False)
            """"""

            """setzte das format der karte"""
            pc = layout.pageCollection()
            pc.page(0).setPageSize('A3', QgsLayoutItemPage.Orientation.Landscape)
            """"""

            """hole mit den element-id's widgets die in der druckvorlage
            definiert sind"""
            map_item = layout.itemById('Karte1')
            akt_name = layout.itemById('akt_name')
            az = layout.itemById('az')
            abb_logo = layout.itemById('abb_logo')
            north_arrow = layout.itemById('north_arrow')
            content = layout.itemById('content')
            remark = layout.itemById('remark')
            user = layout.itemById('user')
            """"""

            """setze werte für die vordefinierten widgets"""
            akt_name.setText(self.parent.parent()._entity_mci.name)
            az.setText(str(self.parent.parent()._entity_mci.az))
            abb_logo.setPicturePath(
                ':/logo/resources/icons/abb_logo_ohne_schrift.svg')
            north_arrow.setPicturePath(':/logo/resources/icons/nordpfeil01.png')
            content.setText(self.print_widget.content)
            remark.setText(self.print_widget.remark)
            user.setText(self.print_widget.user)
            """"""

            """übernehme die Ausdehnung der Kartenansicht"""
            new_extent = self.uiCanvas.mapSettings().visibleExtent()
            """"""

            """setze die layout-karten-ausdehnung auf die ausdehnung der
            kartenansicht"""
            map_item.zoomToExtent(new_extent)
            """"""

            """erstelle und öffne die karte als pdf"""
            exporter = QgsLayoutExporter(layout)
            print_pdf = str(Path().absolute().joinpath('data', '__gis_ausdruck.pdf'))
            exporter.exportToPdf(
                print_pdf, QgsLayoutExporter.PdfExportSettings())
            os.startfile(print_pdf)
            """"""

    def msg_select_layer(self):
        """
        nachricht, dass ein layer ausgewählt werden soll
        """
        msg = QMessageBox()
        msg.setText("Bitte einen Layer auswählen!")
        msg.exec_()

    def displayFeatureInfo(self):

        self.setToolButtonsCheckstate(self.actionFeatureInfo)

        current_layer = self.layer_tree_view.currentLayer()

        if not current_layer:
            msg = QMessageBox()
            msg.setText("Bitte einen Layer auswählen!")
            msg.exec_()
        elif current_layer.type() != current_layer.VectorLayer:
            msg2 = QMessageBox()
            msg2.setText("Dieser Layer kann nicht abgefragt werden!")
            msg2.exec_()
            self.pan()
        else:
            self.feature_info_tool = FeatureInfoTool(self, self.uiCanvas, current_layer)
            self.uiCanvas.setMapTool(self.feature_info_tool)

    def selectLayer(self, layer_id, feature_ids):

        for layer in self.project_instance.mapLayers().values():

            if layer_id == layer.style_id:
                self.layer_tree_view.setCurrentLayer(layer)
                self.setSelectFeature(feature_ids)

    def setMaingisSession(self, session):

        self.maingis_session = session

    def setSelectFeature(self, feature_ids):
        """
        select features
        :param feature_ids:
        :return:
        """

        self.removeSelectedAll()

        self.layer_tree_view.currentLayer().select(feature_ids)

    def activateSelectFeature(self):
        """
        aktiviere die das 'SelectTool'
        """

        self.setToolButtonsCheckstate(self.actionSelectFeature)

        current_layer = self.layer_tree_view.currentLayer()

        if not current_layer:
            msg = QMessageBox()
            msg.setText("Bitte einen Layer auswählen!")
            msg.exec_()
        elif current_layer.type() != current_layer.VectorLayer:
            msg2 = QMessageBox()
            msg2.setText("Auf diesem Layer können keine Objekte ausgewählt werden!")
            msg2.exec_()
            self.pan()
        else:
            self.select_tool = SelectTool(self, self.uiCanvas, current_layer)
            self.uiCanvas.setMapTool(self.select_tool)

    def setToolButtonsCheckstate(self, checked_button=None):
        """
        uncheck all listed buttons expect the given 'checked_button'
        :param checked_button:
        :return:
        """

        self.actionPan.setChecked(False)
        self.actionZoomIn.setChecked(False)
        self.actionZoomOut.setChecked(False)
        self.actionSelectFeature.setChecked(False)
        self.actionFeatureInfo.setChecked(False)

        if checked_button:
            checked_button.setChecked(True)

    def addGisFeature(self):

        # """display a cadDockWidget if needed"""
        # self.addDockWidget(Qt.LeftDockWidgetArea, self.digi_dock)
        # """"""

        current_layer = self.layer_tree_view.currentLayer()

        if current_layer:

            self.digi_tool = DigiTool(self,
                                      self.uiCanvas,
                                      self.digi_dock,
                                      QgsMapToolCapture.CapturePolygon,
                                      layer=current_layer)
            self.uiCanvas.setMapTool(self.digi_tool)
        else:
            self.msg_select_layer()

    def pan(self):

        self.setToolButtonsCheckstate(self.actionPan)

        self.toolPan = QgsMapToolPan(self.uiCanvas)
        self.uiCanvas.setMapTool(self.toolPan)

    def pan_baselayer(self):

        for lay in self.project_instance.mapLayers().values():
            if hasattr(lay, 'base'):
                if lay.base:
                    self.uiCanvas.setExtent(lay.extent())
                    self.uiCanvas.refresh()

    def pan_last(self):
        """zoome zum vorherigen Ausschnitt"""

        self.uiCanvas.zoomToPreviousExtent()

    def zoomIn(self):
        """
        aktiviere das tool zoomIn
        """

        self.setToolButtonsCheckstate(self.actionZoomIn)

        self.toolZoomIn = QgsMapToolZoom(self.uiCanvas, False)  # false = in
        self.uiCanvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        """
        aktiviere das tool zoomOut
        """

        self.setToolButtonsCheckstate(self.actionZoomOut)

        self.toolZoomOut = QgsMapToolZoom(self.uiCanvas, True)  # true = out
        self.uiCanvas.setMapTool(self.toolZoomOut)

    def zoomToSelected(self):
        """
        zoome zum selectierten feature
        """
        current_layer = self.layer_tree_view.currentLayer()
        self.uiCanvas.zoomToSelected(current_layer)

    def zoomToLayer(self):
        """
        zoome auf den aktuellen layer
        :return:
        """
        current_layer = self.layer_tree_view.currentLayer()
        if current_layer:
            self.uiCanvas.setExtent(current_layer.extent())
            self.uiCanvas.refresh()

    def removeSelectedAll(self):
        """
        entferne selectionen von allen layern
        """

        for layer in self.project_instance.mapLayers().values():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()


class FeatureInfoTool(QgsMapToolIdentifyFeature):
    """
    tool zum abfragen von feature attrubuten

    ist noch nicht ganz fertig; das ergebnis wird in der konsole ausgegeben
    """

    def __init__(self, parent, canvas, select_layer):
        self.parent = parent
        self.canvas = canvas
        self.layer = select_layer
        QgsMapToolIdentifyFeature.__init__(self, self.canvas, self.layer)
        self.canvas.currentLayerChanged.connect(self.active_changed)

    def active_changed(self, layer):
        self.layer.removeSelection()
        if isinstance(layer, QgsVectorLayer) and layer.isSpatial():
            self.layer = layer
            self.setLayer(self.layer)

    def canvasReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            found_features = self.identify(
                event.x(),
                event.y(),
                [self.parent.current_layer],
                QgsMapToolIdentify.ActiveLayer
            )

            if found_features:
                for feat in found_features:

                    dv = self.parent.current_layer.data_view

                    feat_mci = feat.mFeature['mci'][0]

                    wid = dv.entity_widget_class(dv)
                    dlg = dv.entity_dialog_class(dv)

                    wid.setEntitySession(self.parent.maingis_session)
                    wid.editEntity(entity_mci=feat_mci)
                    wid.entity_feature = feat.mFeature

                    # """open the entity_widget_class in a dialog"""
                    # self.openDialog(wid)
                    # """"""

                    wid.entity_dialog = dlg
                    dlg.insertWidget(wid)
                    # self.dlg.resize(self.minimumSizeHint())

                    dlg.show()

        elif event.button() == Qt.RightButton:
            self.parent.pan()


    def displayGisWidget(self, widget):

        self.gis_dialog = FeatureAttributeDialog(self.parent)
        self.gis_dialog.insertWidget(widget)

        if self.gis_dialog.exec():
            self.deactivate()


class SelectTool(QgsMapToolIdentifyFeature):
    """
    markiere ein oder mehrere features von einem layer
    """

    selected_features_id: list = []

    def __init__(self, parent, canvas, select_layer):
        self.parent = parent
        self.canvas = canvas
        self.layer = select_layer
        QgsMapToolIdentifyFeature.__init__(self, self.canvas, self.layer)

    def canvasReleaseEvent(self, event):

        if event.button() == Qt.RightButton:
            self.parent.pan()

    def canvasPressEvent(self, event):

        found_features = self.identify(event.x(),
                                       event.y(),
                                       [self.layer],
                                       QgsMapToolIdentify.TopDownAll)

        """erzeuge eine liste mit den gewählten feature-id's abhängig von der 
        auswahlmethode (single- or multi-select)"""
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:  # multiselect mit 'Strg'
            self.layer.selectByIds([f.mFeature.id() for f in found_features],
                                   QgsVectorLayer.AddToSelection)
        else:  # wähle single feature und entferne eine bisherige auswahl
            self.layer.selectByIds([f.mFeature.id() for f in found_features],
                                   QgsVectorLayer.SetSelection)
            self.selected_features_id = []

        for feat in [f.mFeature.id() for f in found_features]:
            self.selected_features_id.append(feat)
        """"""

        # """wenn das main_gis-widget teil eines komplexen entity-widget ist (z.b. Akt)
        # dann wähle ausßerdem die zeilen von verknüpften tabellen
        # """
        # if self.parent.gis_control_widget:
        #     self.parent.gis_control_widget.selectRows(self.layer.style_id,
        #                                               self.selected_features_id)
        # """"""


class DigiTool(QgsMapToolDigitizeFeature):
    """
    digitaliesiere ein neues feature und öffne ein widget um die attribute zu
    erfassen
    """
    def __init__(self, parent, canvas, cad_dock_widget, capture_mode, layer=None):
        super(DigiTool, self).__init__(canvas,
                                       cad_dock_widget,
                                       capture_mode)

        self.parent = parent
        self.layer_name = layer  # layer der bearbeitet wird
        self.canvas = canvas

        self.setLayer(self.layer_name)

        self.layer_name.startEditing()

        self.digitizingCompleted.connect(self.addNewFeature)

    def addNewFeature(self, feature):
        """
        wenn fertig digitalisiert ist, dann gebe die attribute ein
        """

        """hole die modul und widget-class"""
        form_module = __import__(self.parent.current_layer.dataform_modul,
                                 fromlist=[self.parent.current_layer.dataform_class])
        form_wid = getattr(form_module, self.parent.current_layer.dataform_class)
        self.attribute_widget = form_wid()
        """"""

        """erzeuge einen dialog, füge das attribut-widget ein und zeige den dialog"""
        self.att_dialog = FeatureAttributeDialog(self.parent)
        self.att_dialog.insertWidget(self.attribute_widget)
        result = self.att_dialog.exec()
        """"""

        """wenn der attribut-dialog mit 'accept' geschlossen wird, dann werden
        das feature und die attribute gespeichert und die darstellung aktualisiert"""
        if result:
            attr_list = self.attribute_widget.feature_attribute_list()
            attr_list.insert(0, self.parent.parent.parent().entity_id)
            attr_list.insert(0, None)
            feature.setAttributes(attr_list)

            self.layer_name.addFeature(feature)

            """schreibe in db und beende den editing-mode"""
            self.layer_name.commitChanges(stopEditing=True)
            """"""
            self.canvas.update()
            self.canvas.refresh()

            cut_koppel_gstversion()
            self.parent.parent.parent().onGisEdit()

        else:
            print(f"Error in '{self.__class__.__name__}':", sys.exc_info())
            msg = QMessageBox()
            msg.setText("Digitalisierung abgebrochen.")
            msg.exec_()
        """"""

        # """remove the digi_dock if there is one"""
        # self.parent.removeDockWidget(self.parent.digi_dock)
        # """"""

        """set a map_tool after finish digitalizing"""
        self.parent.pan()
        """"""

class LegendDock(QDockWidget):
    """
    baseclass für ein QDockWidget für die legende
    """

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.parent = parent

        self.tool_bar = QToolBar(self)

        self.setTitleBarWidget(self.tool_bar)

        dock_title_lay = QHBoxLayout(self)
        dock_title_lay.setContentsMargins(2, 2, 2, 2)

        """füge einen patzhalter ein"""
        self.emty_wid_01 = QWidget(self)
        self.emty_wid_01.setSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Preferred)
        self.tool_bar.addWidget(self.emty_wid_01)
        """"""

        self.remove_layer = QAction(
            QIcon(":/svg/resources/icons/mActionRemoveLayer.svg"),
            '<b>entferne</b> den ausgewählten Layer')
        self.remove_layer.triggered.connect(self.parent.removeLayer)
        self.tool_bar.addAction(self.remove_layer)

        self.setObjectName("layers")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(self.parent.layer_tree_view)
        self.setContentsMargins(2, 2, 2, 2)

class FeatureAttributeDialog(MainDialog):
    """
    dialog um nach dem einfügen eines neuen features die attribute des feature
    erfassen zu können
    """

    def __init__(self, parent=None):
        super(FeatureAttributeDialog, self).__init__(parent)

        self.parent = parent
        self.enableApply = True
        self.set_apply_button_text('&Speichern und Schließen')

    def accept(self):

        QDialog.accept(self)

    def reject(self):

        QDialog.reject(self)


class MessageBar(QgsMessageBar):
    """
    baseclass für eine QgsMessageBar im main_gis
    """
    def __init__(self, parent=None):
        super(MessageBar, self).__init__(parent)
        self.parent().installEventFilter(self)

    def showEvent(self, event):

        """positioniere die messagebar und passe die größe bei veränderung an"""
        self.resize(QSize(self.parent().geometry().size().width(), self.height()))
        # self.move(0, self.parent().geometry().size().height() - self.height())
        self.raise_()
        """"""

    def eventFilter(self, object, event):
        if event.type() == QEvent.Resize:
            self.showEvent(None)

        return super(MessageBar, self).eventFilter(object, event)
