from qga.alchemy import DmBaseCommunity
from qga.notify import QgaToast, QgaToastPreset, QgaToastPosition
from qga.settings_wdg import QgaSettingsDialog, QgaSettingsWdg
from qgis.PyQt.QtGui import QAction

from qgis.PyQt.QtGui import QIcon
from sqlalchemy import create_engine

from almgis import settings_user, settings_app, settings_project, \
    settings_general, settings_colors, settings_paths, settings_constants, \
    ProjectSessionCls, CommunitySessionCls

from almgis.about import AlmAboutDialog
from almgis.data_model import DmSettings
from almgis.logger import Logger
from almgis.projectstartselector import AlmStartDialog, AlmProjectStartSelector
from almgis.scopes.akte.akte_all_main import AkteAllMainWidget
from almgis.scopes.gst.gst_all_main import GstAllMainWidget

from almgis.scopes.kontakt.kontakt_main import KontaktMainWidget

from qga.mainwindow import QgaMainWindow


class AlmMainWindow(QgaMainWindow):

    def __init__(self, parent=None):
        super(AlmMainWindow, self).__init__(parent)

        self.session_cls = ProjectSessionCls
        self.logger = Logger
        self.dmc_settings = DmSettings

        QgaToast.setMaximumOnScreen(4)

        self.about_dialog_cls = AlmAboutDialog

        self.settings_dlg_cls = QgaSettingsDialog
        self.settings_wdg_cls = QgaSettingsWdg

        self._project_file = None
        self._selected_mainarea = None

        Logger.info("create Mainwindwos!!")

    def setupMainWindow(self):
        super().setupMainWindow()

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

        # self.uiActionOpenHelp = QAction()
        # self.uiActionOpenHelp.setText('öffne AlmGIS-Wiki')
        # # self.uiAktionOpenSettings.setIcon(
        # #     QIcon(':/svg/resources/icons/contacts.svg'))
        #
        # self.uiActionOpenAbout = QAction()
        # self.uiActionOpenAbout.setText('über AlmGIS')
        # # self.uiAktionOpenSettings.setIcon(
        # #     QIcon(':/svg/resources/icons/contacts.svg'))

        self.uiAktionTestSuccess = QAction()
        self.uiAktionTestSuccess.setText('Erfolg')
        self.uiAktionTestWarning = QAction()
        self.uiAktionTestWarning.setText('Wahrnung')
        self.uiAktionTestError = QAction()
        self.uiAktionTestError.setText('Error')
        self.uiAktionTestInfo = QAction()
        self.uiAktionTestInfo.setText('Info')

    def bindSettings(self):

        self.settings_app = settings_app
        self.settings_user = settings_user
        self.settings_project = settings_project

        self.settings_general = settings_general
        self.settings_colors = settings_colors
        self.settings_paths = settings_paths
        self.settings_constants = settings_constants

    def configureDatabases(self):

        # todo: see https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#partitioning-strategies-e-g-multiple-database-backends-per-session

        community_db_file = self.settings_user.value('paths/community_db_file')
        print(f'...')
        # community_engine = configureSession(CommunitySessionCls,
        #                                     self.logger,
        #                                     community_db_file)
        engine_string = 'sqlite:///' + community_db_file
        community_engine = create_engine(engine_string, echo=False)

        CommunitySessionCls.configure(binds={DmBaseCommunity: community_engine})

    def signalsAction(self):
        super().signalsAction()

        # self.uiActionOpenHelp.triggered.connect(self.openHelpUrl)
        # self.uiActionOpenAbout.triggered.connect(self.openAboutDialog)

        self.uiAktionOpenAkteMain.triggered.connect(
            lambda x,
                   wid_cls=AkteAllMainWidget:
            self.openMainWidget(wid_cls))

        self.uiAktionOpenKontakteMain.triggered.connect(
            lambda x,
                   wid_cls=KontaktMainWidget:
            self.openMainWidget(wid_cls))

        self.uiAktionOpenGstZuornungMain.triggered.connect(
            lambda x,
                   wid_cls=GstAllMainWidget:
            self.openMainWidget(wid_cls))

        self.uiAktionTestInfo.triggered.connect(self.testNotifyInfo)
        self.uiAktionTestSuccess.triggered.connect(self.testNotifySuccess)
        self.uiAktionTestWarning.triggered.connect(self.testNotifyWarning)
        self.uiAktionTestError.triggered.connect(self.testNotifyError)

    def testNotifyInfo(self):

        toast = QgaToast(self)
        toast.setDuration(5000)  # Hide after x seconds
        toast.setTitle('Information')
        toast.setText('Das ist eine wichtige Information.')
        toast.applyPreset(QgaToastPreset.INFORMATION)  # Apply style preset
        toast.setPosition(QgaToastPosition.BOTTOM_RIGHT)
        toast.show()

    def testNotifySuccess(self, title=None, text=None):

        toast = QgaToast(self)
        toast.setDuration(5000)  # Hide after x seconds

        if title:
            toast.setTitle(title)
        else:
            toast.setTitle('Wichtige Aufgabe')

        if text:
            toast.setText(text)
        else:
            toast.setText('Die wichtige Aufgabe wurde erfogreich beendet.')

        toast.applyPreset(QgaToastPreset.SUCCESS)  # Apply style preset
        toast.setPosition(QgaToastPosition.BOTTOM_RIGHT)
        toast.show()

    def testNotifyWarning(self):

        toast = QgaToast(self)
        toast.setDuration(5000)  # Hide after x seconds
        toast.setTitle('Wahrnung')
        toast.setText('Achtung, das ist eine Wahrnung!')
        toast.applyPreset(QgaToastPreset.WARNING)  # Apply style preset
        toast.setPosition(QgaToastPosition.BOTTOM_RIGHT)
        toast.show()

    def testNotifyError(self):

        toast = QgaToast(self)
        toast.setDuration(5000)  # Hide after x seconds
        toast.setTitle('Fehler')
        toast.setText('Die wichtige Aufgabe konnte nicht erledigt werden!')
        toast.applyPreset(QgaToastPreset.ERROR)  # Apply style preset
        toast.setPosition(QgaToastPosition.BOTTOM_RIGHT)
        toast.show()

    def createMenuBar(self):
        super().createMenuBar()

        self.uiMenuTest = self.uiMenuBar.addMenu('Test')
        self.uiMenuTestNotify = self.uiMenuTest.addMenu('Benachrichtigungen')
        self.uiMenuTestNotify.addAction(self.uiAktionTestInfo)
        self.uiMenuTestNotify.addAction(self.uiAktionTestSuccess)
        self.uiMenuTestNotify.addAction(self.uiAktionTestWarning)
        self.uiMenuTestNotify.addAction(self.uiAktionTestError)

        # self.uiMenuAkte = self.menuBar().addMenu('Akte')
        # self.uiMenuAkte.addAction(self.uiAktionOpenAkteMain)
        #
        # self.uiMenuGst = self.menuBar().addMenu('Grundstücke')
        # self.uiMenuGst.addAction(self.uiAktionOpenGstZuornungMain)
        #
        # self.uiMenuKontakte = self.menuBar().addMenu('Kontakte')
        # self.uiMenuKontakte.addAction(self.uiAktionOpenKontakteMain)
        #
        # self.uiMenuSonstiges = self.menuBar().addMenu('Sonstiges')
        # self.uiMenuSonstiges.addAction(self.uiAktionCutAwbKomplex)
        # self.uiMenuSonstiges.addAction(self.uiAktionOpenGstImportPath)
        # self.uiMenuSonstiges.addAction(self.uiAktionImportGst)
        # self.uiMenuSonstiges.addAction(self.uiAktionOpenSettings)

        # self.uiMenuHilfe = self.menuBar().addMenu('Hilfe')
        # self.uiMenuHilfe.addAction(self.uiActionOpenHelp)
        # self.uiMenuHilfe.addAction(self.uiActionOpenAbout)

    def createToolBar(self):

        self.uiToolBar.addAction(self.uiAktionOpenAkteMain)
        self.uiToolBar.addAction(self.uiAktionOpenKontakteMain)
        self.uiToolBar.addAction(self.uiAktionOpenGstZuornungMain)

    def initStatusBar(self):
        super().initStatusBar()

    def useProjectSelector(self):
        """open the projectstartselector on start"""

        self.startDialog = AlmStartDialog(self)
        ps = AlmProjectStartSelector(self.startDialog)
        ps.setupProjectStartSelector()

        self.startDialog.enableApply = True
        self.startDialog.insertWidget(ps)

        result = self.startDialog.exec()

    def openSettings(self):
        super().openSettings()

        if self.settings_user.value('project_start_selector') == 'True':
            self.settings_wdg.uiUseProjectStartSelectorCBox.setChecked(True)
        elif self.settings_user.value('project_start_selector') == 'False':
            self.settings_wdg.uiUseProjectStartSelectorCBox.setChecked(False)

        self.settings_dlg.exec()
