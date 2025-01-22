from qgis.PyQt.QtGui import QAction

from qgis.PyQt.QtGui import QIcon

from almgis import settings_user, settings_app, settings_project, \
    settings_general, settings_colors, settings_paths, settings_constants
from almgis import DbSession
from almgis.logger import Logger
from almgis.scopes.akte.akte_all_main import AkteAllMainWidget

from almgis.scopes.kontakt.kontakt_main import KontaktMainWidget

from qga.mainwindow import QgaMainWindow


class AlmMainWindow(QgaMainWindow):

    def __init__(self, parent=None):
        super(AlmMainWindow, self).__init__(parent)

        self.session = DbSession
        self.logger = Logger


    def declareActions(self):
        super().declareActions()

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

    def bindSettings(self):

        self.settings_app = settings_app
        self.settings_user = settings_user
        self.settings_project = settings_project

        self.settings_general = settings_general
        self.settings_colors = settings_colors
        self.settings_paths = settings_paths
        self.settings_constants = settings_constants

    def signalsAction(self):
        super().signalsAction()

        self.uiAktionOpenAkteMain.triggered.connect(
            lambda x,
                   wid_cls=AkteAllMainWidget,
                   session=DbSession:
            self.openMainWidget(wid_cls, session))

        self.uiAktionOpenKontakteMain.triggered.connect(
            lambda x,
                   wid_cls=KontaktMainWidget,
                   session=DbSession:
            self.openMainWidget(wid_cls, session))

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
