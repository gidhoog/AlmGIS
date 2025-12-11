from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from qga import Qga
from qga.core.main_window import QgaMainWindow
from qga.database.alchemy import DmBaseCommon
from qga.database.session import QgaCommonSessionCls
from qga.gui.notify import QgaNotify
from qga.gui.settings_wdg import QgaSettingsDialog, QgaSettingsWdg
from sqlalchemy import create_engine

from almgis.core.dialog import AlmDialog
from almgis.scopes.kontakt.kontakt_main import KontaktMainWidget
from almgis.database.models import DmSettings
from almgis.gui.about import AlmAboutDialog
from almgis.gui.main_window_gui import AlmMainWindowGui
from almgis.gui.start_wdg_gui import AlmStartWdg


class AlmMainWindow(QgaMainWindow):

    def __init__(self):
        super(AlmMainWindow, self).__init__()

        self.ui = AlmMainWindowGui(self)

        self.start_dlg_cls = AlmDialog
        self.start_wdg_cls = AlmStartWdg

        self.dmc_settings = DmSettings

        QgaNotify.setMaximumOnScreen(4)

        self.about_dialog_cls = AlmAboutDialog

        self.settings_dlg_cls = QgaSettingsDialog
        self.settings_wdg_cls = QgaSettingsWdg

        self._project_file = None
        self._selected_mainarea = None

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

        # self.ui.actionOpenKontakteAlle.triggered.connect(
        #     self.openKontakteAllMainWdg)
        # self.ui.openKontakteAllMainWdgSgn.connect(self.openKontakteAllMainWdg)
        self.ui.openKontakteAllMainWdgSgn.connect(
            self.openKontakteAllMainWdg)

        self.ui.openGstAllMainWdgSgn.connect(self.openGstAllMainWdg)

    def setupDatabasesCommon(self):
        """
        richte die datenbanken für almgis ein;
        siehe: https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#partitioning-strategies-e-g-multiple-database-backends-per-session
        """

        """hole file_path der common_db"""
        common_db_file = Qga.Settings.User.value('paths/common_db_file')
        """"""

        """richte die session 'QgaCommonSessionCls' ein"""
        engine_string = 'sqlite:///' + common_db_file
        community_engine = create_engine(engine_string, echo=False)
        QgaCommonSessionCls.configure(binds={DmBaseCommon: community_engine})
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

        self.showNotify(QgaNotifyPreset.SUCCESS)

    def testNotifyInfo(self):

        self.showNotify(QgaNotifyPreset.INFORMATION)

    def testNotifyWarning(self):

        self.showNotify(QgaNotifyPreset.WARNING)

    def testNotifyError(self):

        self.showNotify(QgaNotifyPreset.ERROR)

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

    def openKontakteAllMainWdg(self):
        # self.openMainWidget(KontaktMainWidget, debug=False)
        self.insertMainWdg(KontaktMainWidget,
                           'alle Kontakte neu')

    def openGstAllMainWdg(self):
        print(f'open gst all')
        # self.openMainWidget(KontaktMainWidget, debug=True)

    def openSettings(self):
        super().openSettings()

        if Qga.Settings.User.value('project_start_selector') == 'True':
            self.settings_wdg.uiUseProjectStartSelectorCBox.setChecked(True)
        elif Qga.Settings.User.value('project_start_selector') == 'False':
            self.settings_wdg.uiUseProjectStartSelectorCBox.setChecked(False)

        self.settings_dlg.exec_qga()
