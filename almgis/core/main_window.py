from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from qga.core.main_window import QgaMainWindow
from qga.gui.notify import QgaToast
from qga.gui.settings_wdg import QgaSettingsDialog, QgaSettingsWdg

from almgis import ProjectSessionCls, settings_app, settings_user, \
    settings_project, settings_general, settings_colors, settings_paths, \
    settings_constants
from almgis.core.kontakt.kontakt_main import KontaktMainWidget
# from almgis.core.kontakt.kontakt_main import KontaktMainWidget
from almgis.core.logger import Logger
from almgis.database.models import DmSettings, DmKontaktType
from almgis.gui.about import AlmAboutDialog
from almgis.gui.main_window_gui import AlmMainWindowGui
from almgis.gui.start_wdg_gui import AlmStartWdg


class AlmMainWindow(QgaMainWindow):

    def __init__(self):
        super(AlmMainWindow, self).__init__()

        self.ui = AlmMainWindowGui()

        self.start_wdg_cls = AlmStartWdg

        self.session_prj_cls = ProjectSessionCls
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

    def setupActions(self):
        super().setupActions()

        self.uiAktionOpenAkteMain = QAction()
        self.uiAktionOpenAkteMain.setText('Alle Akte')
        self.uiAktionOpenAkteMain.setIcon(
            QIcon(':/svg/icons/akte.svg'))

        self.uiAktionOpenGstZuornungMain = QAction()
        self.uiAktionOpenGstZuornungMain.setText('zugeordnete Grundstücke')
        self.uiAktionOpenGstZuornungMain.setIcon(
            QIcon(':/svg/icons/gst_all.svg'))

        self.actionOpenKontakteAlle = QAction()
        self.actionOpenKontakteAlle.setText('alle Kontakte')
        self.actionOpenKontakteAlle.setIcon(
            QIcon(':/svg/icons/contacts.svg'))

        self.uiAktionCutAwbKomplex = QAction()
        self.uiAktionCutAwbKomplex.setText('Verschnitt: Gst und Komplexe')
        # self.uiAktionCutAwbKomplex.setIcon(
        #     QIcon(':/svg/icons/contacts.svg'))

        self.uiAktionOpenSettings = QAction()
        self.uiAktionOpenSettings.setText('Einstellungen')
        # self.uiAktionOpenSettings.setIcon(
        #     QIcon(':/svg/icons/contacts.svg'))

        self.uiAktionOpenGstImportPath = QAction()
        self.uiAktionOpenGstImportPath.setText('öffne Gst-Importverzeichnis')
        self.uiAktionOpenGstImportPath.setIcon(
            QIcon(':/svg/icons/mActionFileOpen.svg'))

        self.uiAktionImportGst = QAction()
        self.uiAktionImportGst.setText('Gst-Importverzeichnis neu einlesen')
        self.uiAktionImportGst.setIcon(
            QIcon(':/svg/icons/import.svg'))

        # self.uiActionOpenHelp = QAction()
        # self.uiActionOpenHelp.setText('öffne AlmGIS-Wiki')
        # # self.uiAktionOpenSettings.setIcon(
        # #     QIcon(':/svg/icons/contacts.svg'))
        #
        # self.uiActionOpenAbout = QAction()
        # self.uiActionOpenAbout.setText('über AlmGIS')
        # # self.uiAktionOpenSettings.setIcon(
        # #     QIcon(':/svg/icons/contacts.svg'))

        self.uiAktionTestSuccess = QAction()
        self.uiAktionTestSuccess.setText('Erfolg')
        self.uiAktionTestWarning = QAction()
        self.uiAktionTestWarning.setText('Wahrnung')
        self.uiAktionTestError = QAction()
        self.uiAktionTestError.setText('Error')
        self.uiAktionTestInfo = QAction()
        self.uiAktionTestInfo.setText('Info')

    def connectSignals(self):
        super().connectSignals()

        self.ui.actionOpenKontakteAlle.triggered.connect(
            self.openMainWdgKontakteAlle)

    def setupSettings(self):

        self.settings_app = settings_app
        self.settings_user = settings_user

        """setze verschiedene attribute für die projekt-settings"""
        self.settings_project = settings_project
        self.settings_project.prj_session_cls = ProjectSessionCls
        self.settings_project.settings_dmc = DmSettings
        self.settings_project.logger = Logger
        """"""

        self.settings_general = settings_general
        self.settings_colors = settings_colors
        self.settings_paths = settings_paths
        self.settings_constants = settings_constants

    def setupDatabases(self):
        """
        richte die datenbanken für almgis ein;
        siehe: https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#partitioning-strategies-e-g-multiple-database-backends-per-session
        """

        """hole file_path der common_db"""
        common_db_file = self.settings_user.value('paths/common_db_file')
        """"""

        """richte die session 'CommunitySessionCls' ein"""
        engine_string = 'sqlite:///' + common_db_file
        community_engine = create_engine(engine_string, echo=False)
        CommunitySessionCls.configure(binds={DmBaseCommon: community_engine})
        """"""

    def signalsAction(self):
        super().signalsAction()

        # self.uiActionOpenHelp.triggered.connect(self.openHelpUrl)
        # self.uiActionOpenAbout.triggered.connect(self.openAboutDialog)

        # self.uiAktionOpenAkteMain.triggered.connect(
        #     lambda x,
        #            wid_cls=AkteAllMainWidget:
        #     self.openMainWidget(wid_cls))
        #
        # self.uiAktionOpenKontakteMain.triggered.connect(
        #     lambda x,
        #            wid_cls=KontaktMainWidget:
        #     self.openMainWidget(wid_cls))
        #
        # self.uiAktionOpenGstZuornungMain.triggered.connect(
        #     lambda x,
        #            wid_cls=GstAllMainWidget:
        #     self.openMainWidget(wid_cls))
        #
        # self.uiAktionTestInfo.triggered.connect(self.testNotifyInfo)
        # self.uiAktionTestSuccess.triggered.connect(self.testNotifySuccess)
        # self.uiAktionTestWarning.triggered.connect(self.testNotifyWarning)
        # self.uiAktionTestError.triggered.connect(self.testNotifyError)

    def testNotifySuccess(self):

        self.showNotify(QgaToastPreset.SUCCESS)

    def testNotifyInfo(self):

        self.showNotify(QgaToastPreset.INFORMATION)

    def testNotifyWarning(self):

        self.showNotify(QgaToastPreset.WARNING)

    def testNotifyError(self):

        self.showNotify(QgaToastPreset.ERROR)

    def setupMenuBar(self):
        super().setupMenuBar()

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

    def setupToolBar(self):

        self.uiToolBar.addAction(self.uiAktionOpenAkteMain)
        self.uiToolBar.addAction(self.actionOpenKontakteAlle)
        self.uiToolBar.addAction(self.uiAktionOpenGstZuornungMain)

    def setupStatusBar(self):
        super().setupStatusBar()

    # def useProjectSelector(self):
    #     """open the projectstartselector on start"""
    #
    #     self.startDialog = AlmStartDialog(self)
    #     ps = AlmProjectStartSelector(self.startDialog)
    #     ps.setupProjectStartSelector()
    #
    #     self.startDialog.enableApply = True
    #     self.startDialog.insertWidget(ps)
    #
    #     result = self.startDialog.exec()

    def openMainWdgKontakteAlle(self):

        self.openMainWidget(KontaktMainWidget)

    def openSettings(self):
        super().openSettings()

        if self.settings_user.value('project_start_selector') == 'True':
            self.settings_wdg.uiUseProjectStartSelectorCBox.setChecked(True)
        elif self.settings_user.value('project_start_selector') == 'False':
            self.settings_wdg.uiUseProjectStartSelectorCBox.setChecked(False)

        self.settings_dlg.exec_qga()

    def loadDefaultProjectData(self):

        default_session = ProjectSessionCls()

        kt1 = DmKontaktType()
        kt1.id = 0
        kt1.name = "Einzelperson"
        kt1.name_short = "E"
        kt1.sort = 0
        kt1.icon_01 = ":/svg/icons/person.svg"
        kt1.module = "almgis.scopes.kontakt.kontakt"
        kt1.type_class = "KontaktEinzel"
        kt1.dmi_class = "BKontaktEinzel"
        kt1.not_delete = 1
        kt1.sys_data = 1
        default_session.add(kt1)

        kt2 = DmKontaktType()
        kt2.id = 1
        kt2.name = "Gemeinschaft"
        kt2.name_short = "G"
        kt2.sort = 0
        kt2.icon_01 = ":/svg/icons/group.svg"
        kt2.module = "almgis.scopes.kontakt.kontakt"
        kt2.type_class = "Kontakt"
        kt2.dmi_class = "BKontaktGem"
        kt2.not_delete = 1
        kt2.sys_data = 1
        default_session.add(kt2)

        default_session.commit()