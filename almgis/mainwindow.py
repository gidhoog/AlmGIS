from pathlib import Path

from PyQt5.QtCore import QSettings
from qgis.PyQt.QtGui import QAction

from qgis.PyQt.QtGui import QIcon

from almgis import DbSession, settings_user, settings_sys
from almgis.scopes.akte.akte_all_main import AkteAllMainWidget

from almgis.scopes.kontakt.kontakt_main import KontaktMainWidget

from qga.mainwindow import QgaMainWindow

from almgis.settings import AlmSettingsUser, AlmSettingsApp


# from almgis.scopes.akte import akte_all_main
# from almgis.scopes.gst import gst_all_main
# from almgis.scopes.kontakt import kontakt_main
# from qga.settings import SettingsDlg, SettingsWdg


# class AlmMainWindow(QgaMainWindow, mainwindow_UI.Ui_QgaMainWindow):
class AlmMainWindow(QgaMainWindow):

    def __init__(self, parent=None):
        super(AlmMainWindow, self).__init__(parent)
        # self.setupUi(self)

        self.setWindowTitle('AlmGIS')

    def declareActions(self):

        self.uiAktionOpenAkteMain = QAction()
        self.uiAktionOpenAkteMain.setText('Alle Akte')
        self.uiAktionOpenAkteMain.setIcon(
            QIcon(':/svg/resources/icons/akte.svg'))

        self.uiAktionOpenGstZuornungMain = QAction()
        self.uiAktionOpenGstZuornungMain.setText('zugeordnete Grundstücke')
        self.uiAktionOpenGstZuornungMain.setIcon(
            QIcon(':/svg/resources/icons/gst_all.svg'))

        self.uiAktionOpenKontakteMain = QAction()
        self.uiAktionOpenKontakteMain.setText('alle Kontakte')
        self.uiAktionOpenKontakteMain.setIcon(
            QIcon(':/svg/resources/icons/contacts.svg'))

        self.uiAktionCutAwbKomplex = QAction()
        self.uiAktionCutAwbKomplex.setText('Verschnitt: Gst und Komplexe')
        # self.uiAktionCutAwbKomplex.setIcon(
        #     QIcon(':/svg/resources/icons/contacts.svg'))

        self.uiAktionOpenSettings = QAction()
        self.uiAktionOpenSettings.setText('Einstellungen')
        # self.uiAktionOpenSettings.setIcon(
        #     QIcon(':/svg/resources/icons/contacts.svg'))

        self.uiAktionOpenGstImportPath = QAction()
        self.uiAktionOpenGstImportPath.setText('öffne Gst-Importverzeichnis')
        self.uiAktionOpenGstImportPath.setIcon(
            QIcon(':/svg/resources/icons/mActionFileOpen.svg'))

        self.uiAktionImportGst = QAction()
        self.uiAktionImportGst.setText('Gst-Importverzeichnis neu einlesen')
        self.uiAktionImportGst.setIcon(
            QIcon(':/svg/resources/icons/import.svg'))

        self.uiAktionOpenWiki = QAction()
        self.uiAktionOpenWiki.setText('öffne AlmGIS-Wiki')
        # self.uiAktionOpenSettings.setIcon(
        #     QIcon(':/svg/resources/icons/contacts.svg'))

        self.uiAktionOpenAbout = QAction()
        self.uiAktionOpenAbout.setText('über AlmGIS')
        # self.uiAktionOpenSettings.setIcon(
        #     QIcon(':/svg/resources/icons/contacts.svg'))

    def signalsAction(self):

        # self.uiAktionOpenAkteMain.triggered.connect(self.testAkte)
        self.uiAktionOpenAkteMain.triggered.connect(
            lambda x,
                   wid_cls=AkteAllMainWidget,
                   session=DbSession:
            self.openMainWidgetNew(wid_cls, session))

        self.uiAktionOpenKontakteMain.triggered.connect(
            lambda x,
                   wid_cls=KontaktMainWidget,
                   session=DbSession:
            self.openMainWidgetNew(wid_cls, session))

        # self.uiAktionOpenKontakteMain.triggered.connect(self.testKontakte)

    # def testAkte(self):
    #     # super().testAkte()
    #
    #     print('test Akte')
    #     # self.uiStatusProgressBar.setVisible(True)
    #     # self.uiStatusProgressLbl.setText('Akt öffnen')
    #     # widget = AkteAllMainWidget(self, DbSession())
    #     db_session_cls = DbSession
    #     widget_cls = AkteAllMainWidget
    #     widget_title = "AAkte"
    #
    #     # self.openMainWidget(widget_cls, widget_title, db_session_cls)
    #     self.openMainWidgetNew(widget_cls, widget_title, db_session_cls)

    # def testKontakte(self):
    #     super().testKontakte()
    #
    #     print('test Kontakte')
    #     # widget = KontaktMainWidget(self, self.main_session)
    #     widget = KontaktMainWidget(self, DbSession())
    #     widget_title = "KKontakte"
    #
    #     self.openMainWidget(widget, widget_title)
    #
    #     # widget.initMainWidget()
    #     #
    #     # self._addMaintable(widget, widget_title)
    #     #
    #     # widget.update_app.connect(self.update_application_in_mainwindow)

    def createMenuBar(self):
        super().createMenuBar()

        self.uiMenuAkte = self.menuBar().addMenu('Akte')
        self.uiMenuAkte.addAction(self.uiAktionOpenAkteMain)

        self.uiMenuGst = self.menuBar().addMenu('Grundstücke')
        self.uiMenuGst.addAction(self.uiAktionOpenGstZuornungMain)

        self.uiMenuKontakte = self.menuBar().addMenu('Kontakte')
        self.uiMenuKontakte.addAction(self.uiAktionOpenKontakteMain)

        self.uiMenuSonstiges = self.menuBar().addMenu('Sonstiges')
        self.uiMenuSonstiges.addAction(self.uiAktionCutAwbKomplex)
        self.uiMenuSonstiges.addAction(self.uiAktionOpenGstImportPath)
        self.uiMenuSonstiges.addAction(self.uiAktionImportGst)
        self.uiMenuSonstiges.addAction(self.uiAktionOpenSettings)

        self.uiMenuHilfe = self.menuBar().addMenu('Hilfe')
        self.uiMenuHilfe.addAction(self.uiAktionOpenWiki)
        self.uiMenuHilfe.addAction(self.uiAktionOpenAbout)

    def createToolBar(self):

        self.uiToolBar.addAction(self.uiAktionOpenAkteMain)
        self.uiToolBar.addAction(self.uiAktionOpenKontakteMain)
        self.uiToolBar.addAction(self.uiAktionOpenGstZuornungMain)

    def initStatusBar(self):
        super().initStatusBar()

        self.uiStatusBar.showMessage('AlmGIS geladen ...', 3000)

#     def setupMainWindow(self):
#
#         self.main_session = DbSession()
#
#     def signalsMenue(self):
#         """
#         menü signale
#         """
#
#         # Akte:
#         self.uiAkteAllAction.triggered.connect(
#             lambda: self._setMainWidget("akte_alle"))
#
#         # Kontakte:
#         self.uiKontakteAllAction.triggered.connect(
#             lambda: self._setMainWidget("kontakte_alle"))
#
#         # alle zugeordneten gst:
#         self.actionAllGst.triggered.connect(
#             lambda: self._setMainWidget("gst_all"))
#
#         # Verschnitte:
#         self.actionCutGstVersionKomplexe.triggered.connect(self.cutGstKoppel)
#
#         # Einstellungen:
#         self.actionSettings.triggered.connect(self.openSettings)
#
#     def cutGstKoppel(self):
#         """
#         verschneide alle aktuellen gst mit den koppeln die mit 'awb' markiert
#         sind
#         :return:
#         """
#         awb_koppeln = QgsVectorLayer(
#             str(data_db_path.absolute()) + '|layername=v_awb_koppeln',
#             'awb_koppeln',
#             'ogr'
#         )
#         cut_koppel_gstversion(awb_koppeln)
#
#     def openSettings(self):
#
#         settings_dlg = SettingsDlg(self)
#
#         settings_wdg = SettingsWdg(self)
#
#         settings_dlg.insertWidget(settings_wdg)
#         settings_dlg.setMinimumWidth(1000)
#         settings_dlg.setMinimumHeight(600)
#
#         settings_dlg.exec()
#
#     def _setMainWidget(self, scope):
#         """
#         methode die aufgrufen wird wenn ein widget als main_widget direkt in
#         die hauptansicht geladen wird (funktioniert derzeit nur mit einem
#         main_table)
#         """
#
#         widget = QWidget(self)
#         widget_title = 'tttt'
#
#         # if scope == "akte_alle":
#         #     # widget = akte_all_main.AkteAllMain(self)
#         #     widget = akte_all_main.AkteAllMainWidget(self,
#         #                                              self.main_session)
#         #     widget_title = "Akten"
#         #
#         # if scope == "kontakte_alle":
#         #     widget = kontakt_main.KontaktMainWidget(self,
#         #                                              self.main_session)
#         #     widget_title = "Kontakte"
#         #
#         # if scope == "gst_all":
#         #     widget = gst_all_main.GstAllMainWidget(self,
#         #                                              self.main_session)
#         #     widget_title = "Grundstücke"
#
#         widget.initMainWidget()
#
#         self._addMaintable(widget, widget_title)
#
#         widget.update_app.connect(self.update_application_in_mainwindow)
#
#     def initUi(self):
#         """
#         definiere die oberfläche
#         """
#         self._guiMainSplitter = QSplitter()
#         self.uiMainHLay.addWidget(self._guiMainSplitter)
#
#         """füge einen button ein um eine zusätzliche display_area einzufügen"""
#         self._guiAddMainAreaPbtn = QPushButton()
#         self._guiAddMainAreaPbtn.setFlat(True)
#         self._guiAddMainAreaPbtn.setMaximumWidth(30)
#         self._guiAddMainAreaPbtn.setIcon(
#             QIcon(':/svg/resources/icons/add_display_area_unchecked.svg'))
#         self._guiAddMainAreaPbtn.setIconSize(QSize(20, 20))
#         self._guiAddMainAreaPbtn.setCheckable(True)
#         self._guiAddMainAreaPbtn.setToolTip('neuer Darstellungsbereich')
#         self.menuBar.setCornerWidget(
#             self._guiAddMainAreaPbtn, Qt.TopRightCorner)
#         self._guiAddMainAreaPbtn.clicked.connect(
#             self.setAddDisplayAreaCheckStatus)
#         """"""
#
#         self.uicUserLbl = QLabel()
#         self.uicUserLbl.setText(f'Benutzer: {os.getlogin()}')
#         self.uiStatusBar.addPermanentWidget(self.uicUserLbl)
#
#         """set the uiStatusBar-frame invisible"""
#         self.setStyleSheet('QStatusBar::item{border:0px}')
#         """"""
#
#         """entferne die 'angreifer' im eck rechts unten die die größenänderung
#         des widgets sichtbar machen"""
#         self.uiStatusBar.setSizeGripEnabled(False)
#         """"""
#
#         horrSplitter = QSplitter()
#         horrSplitter.setOrientation(Qt.Horizontal)
#
#         self.uiStatusProgressBar = QProgressBar()
#         self.uiStatusProgressBar.setMinimum(0)
#         self.uiStatusProgressBar.setMaximum(0)
#         self.uiStatusProgressBar.setValue(-1)
#         self.uiStatusProgressLbl = QLabel()
#         self.uiStatusProgressLbl.setText('Prozess:')
#
#         # self.uiStatusBar.addWidget(self.uiStatusProgressLbl)
#         # self.uiStatusBar.addWidget(self.uiStatusProgressBar, 2)
#         # self.uiStatusBar.addWidget(horrSplitter)
#
#         self.uiStatusBar.showMessage('AlmGIS geladen ...', 5000)
#
#         # self.uiStatusBar.clearMessage()
#
#     def _addMaintable(self, table_widget, tab_title):
#         """
#         füge einen maintable_scope in ein TabWidget ein
#         """
#         wid = table_widget
#
#         """wenn der button für eine neue display_area gedrückt ist, dann erzeuge
#          eine; ansonst füge den main_table in das aktuelle TabWidget ein"""
#         if self._guiAddMainAreaPbtn.isChecked():
#             self._addMainArea()
#             self._guiAddMainAreaPbtn.setChecked(False)
#             self.setAddDisplayAreaCheckStatus()
#         else:
#             """neue main_area wenn noch keine vorhanden ist"""
#             if not self._selected_mainarea:
#                 self._addMainArea()
#             """"""
#
#         self._selected_mainarea.tab_widget.addTab(wid, tab_title)
#
#         self._selected_mainarea.tab_widget.setCurrentIndex(
#             self._selected_mainarea.tab_widget.count() - 1)
#
#         self._addWidgetToMainWidgetList(wid)
#         """"""
#
#     def selectMainArea(self):
#         """
#         wähle eine main_area aus
#         """
#
#         for area in self.mainarea_list:
#             area.setDeselected()
#         self._selected_mainarea.setSelected()
#
#     def setAddDisplayAreaCheckStatus(self):
#         """
#         mache den status_id zum hinzufügen einer neuen display_area am button sichtbar
#         """
#
#         if self._guiAddMainAreaPbtn.isChecked():
#             self._guiAddMainAreaPbtn.setIcon(
#                 QIcon(':/svg/resources/icons/add_display_area_checked.svg'))
#         else:
#             self._guiAddMainAreaPbtn.setIcon(
#                 QIcon(':/svg/resources/icons/add_display_area_unchecked.svg'))
#
#     def _addMainArea(self):
#         """
#         füge eine neue main_area ein
#         """
#
#         self.mainarea = DisplayAreaTab(self)
#         self.mainarea.installEventFilter(self)
#         self._guiMainSplitter.addWidget(self.mainarea)
#         self._selected_mainarea = self.mainarea
#         self.mainarea_list.append(self.mainarea)
#
#         self.selectMainArea()
#
#     def _addWidgetToMainWidgetList(self, widget):
#         """
#         füge das übergebene widget in die liste main_widget_list ein;
#         wird z.b. beim update aller offenen main_tables benötigt
#         """
#         self._main_widget_list.append(widget)
#
#     def update_application_in_mainwindow(self):
#         """
#         aktualisiere die ansicht aller angezeigten main_widgets
#         """
#
#         for main_widget in self._main_widget_list:
#             main_widget.updateMainWidget()
#
#     def eventFilter(self, obj, event):
#         """
#         event filter für dieses widget
#         """
#
#         """setze eine main_area aktiv wenn auf sie geklickt wird"""
#         if event.type() == QEvent.MouseButtonPress:
#             if type(obj) == DisplayAreaTab:
#                 self._selected_mainarea = obj
#                 self.selectMainArea()
#
#                 return True
#             else:
#                 return QMainWindow.eventFilter(self, obj, event)
#         else:
#             return QMainWindow.eventFilter(self, obj, event)
#         """"""
#
#
# class DisplayAreaTab(QWidget):
#     """
#     ein widget, das selbst in einer QScrollArea liegt und ein QTabWidget beinhaltet
#     a area that displays a QTabWidget with the detail-widgets;
#     """
#
#     def __init__(self, parent):
#         super(DisplayAreaTab, self).__init__(parent)
#
#         self.parent = parent
#
#         self.setContentsMargins(0, 0, 0, 0)
#
#         display_layout = QVBoxLayout(self)
#         display_layout.setContentsMargins(0, 0, 0, 0)
#         self.setLayout(display_layout)
#
#         self.gui_close_button = QPushButton(self)
#         self.gui_close_button.setIcon(
#             QIcon(':/svg/resources/icons/close_mainarea_inactive.svg'))
#         self.gui_close_button.setIconSize(QSize(16, 16))
#         self.gui_close_button.setFixedSize(20, 20)
#         self.gui_close_button.setFlat(True)
#         self.gui_close_button.setToolTip('schließe den Darstellungsbereich')
#
#         self.frame = DisplayAreaFrame(self)
#         frame_layout = QVBoxLayout()
#         frame_layout.setContentsMargins(3, 3, 3, 3)
#         self.frame.setLayout(frame_layout)
#
#         self.scrollarea = ScrollArea(self)
#
#         scroll_layout = QVBoxLayout(self)
#         scroll_layout.setContentsMargins(10, 10, 10, 10)
#         self.scrollarea.setLayout(scroll_layout)
#         self.tab_widget = TabWidget(self)
#
#         self.scrollarea.setWidget(self.tab_widget)
#         self.scrollarea.layout().setContentsMargins(10, 10, 10, 10)
#         self.layout().addWidget(self.frame)
#
#         frame_layout.addWidget(self.scrollarea)
#
#         self.gui_close_button.raise_()
#         self.gui_close_button.clicked.connect(self.closeMainArea)
#
#     def setSelected(self):
#
#         self.gui_close_button.setIcon(
#             QIcon(':/svg/resources/icons/close_mainarea_active.svg'))
#
#     def setDeselected(self):
#
#         self.gui_close_button.setIcon(
#             QIcon(':/svg/resources/icons/close_mainarea_inactive.svg'))
#
#     def addTabWidget(self, table_widget, tab_title):
#
#         self.tab_widget.addTab(table_widget, tab_title)
#
#     def resizeEvent(self, QResizeEvent):
#         super().resizeEvent(QResizeEvent)
#
#         """position den close-buttons"""
#         width = self.frameGeometry().width()
#         self.gui_close_button.move(width - 28, 5)
#         """"""
#
#     def closeMainArea(self):
#         """
#         entferne eine main_area und alle darin enthaltenen main_widgets
#         """
#
#         """entferne die tab_widgets dieser display_area aus der liste
#         'main_widget_list' """
#         number_tab_widgets = self.tab_widget.count()
#         for wid in range(number_tab_widgets):
#             del_wid = self.tab_widget.widget(wid)
#             if del_wid in self.parent._main_widget_list:
#                 self.parent._main_widget_list.remove(del_wid)
#         """"""
#
#         """entferne diese display_area von der mainarea_list"""
#         self.parent.mainarea_list.remove(self)
#         """"""
#
#         """wähle eine übrig bleibende main_area als aktiv"""
#         if self.parent.mainarea_list:
#             #: check if the removed area was the selected_area
#             if self == self.parent._selected_mainarea:
#                 self.parent._selected_mainarea = self.parent.mainarea_list[0]
#             self.parent.selectMainArea()
#         """"""
#
#         if not self.parent.mainarea_list:
#             self.parent._selected_mainarea = None
#
#         self.hide()
#         self.deleteLater()
#
#
# class DisplayAreaFrame(QFrame):
#     """
#     rahmen für eine display_area
#     """
#
#     def __init__(self, parent=None):
#         super(DisplayAreaFrame, self).__init__(parent)
#
#         self.setContentsMargins(0, 0, 0, 0)
#
#
# class ScrollArea(QScrollArea):
#     """
#     baseclass für eine scroll_area (das ein TabWidget beinhaltet)
#     """
#
#     def __init__(self, parent=None):
#         super(ScrollArea, self).__init__(parent)
#
#         self.parent = parent
#
#         self.setFrameShape(0)
#         self.setFrameShadow(0)
#         self.setLineWidth(0)
#
#         self.setWidgetResizable(True)
#
#
# class TabWidget(QTabWidget):
#     """
#     baseclass für ein TabWidget
#     """
#
#     def __init__(self, parent=None):
#         super(TabWidget, self).__init__(parent)
#
#         self.parent = parent
#
#         self.setContentsMargins(0, 0, 0, 0)
#
#         self.setTabsClosable(True)
#         self.setMovable(True)
#
#         self.tabCloseRequested.connect(self.closeTab)
#
#     def closeTab(self, widget_index):
#         """
#         schließe ein tab im tab_widget; außerdem muss das main_widget aus der
#         main_widget_list gelöscht werden
#         """
#
#         del_widget = self.widget(self.currentIndex())
#         if del_widget in self.parent.parent._main_widget_list:
#             self.parent.parent._main_widget_list.remove(del_widget)
#
#         """entferne den aktuellen tab aus dem tab_widget"""
#         self.removeTab(widget_index)
#         """"""
#
#         self.removeLastMainarea()
#
#     def removeLastMainarea(self):
#         """
#         wenn kein tab in diesem tab_widget mehr vorhanden sind, dann lösche die
#         gesamte main_area
#         """
#         if self.count() == 0:
#             self.parent.closeMainArea()
#
#     def resizeEvent(self, QResizeEvent):
#         super().resizeEvent(QResizeEvent)
#
#         size = self.size()
#         self.tabBar().setMaximumWidth(size.width() - 50)