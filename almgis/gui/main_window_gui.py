from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu
from qga.gui.main_window_gui import QgaMainWindowGui


class AlmMainWindowGui(QgaMainWindowGui):

    openKontakteAllMainWdgSgn = pyqtSignal()

    openGstMainWdgSgn = pyqtSignal()
    openGstMainAwbWdgSgn = pyqtSignal()

    openGdbImportPathSgn = pyqtSignal()
    importGdbImportPathSgn = pyqtSignal()

    def __init__(self, ctrl=None):
        super(AlmMainWindowGui, self).__init__(ctrl)

        # self.useMenuBar = False

    def createActions(self):
        super().createActions()

        self.actions.create(self, 'kontakt.main_all', '&Kontakte',
                            'Ctrl+K',
                            icon=':/svg/icons/contacts.svg')

    def connectActions(self):
        super().connectActions()

        self.actions.add_connections({
            'kontakt.main_all': self.ctrl.openKontakteAllMainWdg,
        })

    def setupActions(self):
        super().setupActions()

        self.actionAlleAkte = QAction()
        self.actionAlleAkte.setText('alle Akte')
        self.actionAlleAkte.setIcon(
            QIcon(':/svg/icons/mActionFileNew.svg'))

        self.actionOpenKontakteAlle = QAction()
        self.actionOpenKontakteAlle.setText('Kontakte')
        self.actionOpenKontakteAlle.setIcon(
            QIcon(':/svg/icons/contacts.svg'))
        self.actionOpenKontakteAlle.triggered.connect(self.openKontakteAllMainWdgSgn)

        self.actionOpenGstAll = QAction()
        self.actionOpenGstAll.setText('Vorrat')
        self.actionOpenGstAll.setIcon(
            QIcon(':/svg/icons/gst_all.svg'))
        self.actionOpenGstAll.triggered.connect(self.openGstMainWdgSgn)

        self.actionOpenGstAwb = QAction()
        self.actionOpenGstAwb.setText('Alm- und Weidebuch')
        self.actionOpenGstAwb.setIcon(
            QIcon(':/svg/icons/gst_all.svg'))
        self.actionOpenGstAwb.triggered.connect(self.openGstMainAwbWdgSgn)

        self.actionOpenGdbImpPath = QAction()
        self.actionOpenGdbImpPath.setText('öffne Gst-Importverzeichnis')
        self.actionOpenGdbImpPath.setIcon(
            QIcon(':/svg/icons/mActionFileOpen.svg'))
        self.actionOpenGdbImpPath.triggered.connect(self.openGdbImportPathSgn)

        # self.actionOpenGdbImpPath.triggered.connect(
        #     self.ctrl.openImportBevShpSgn)
        self.actionOpenGdbImpPath.triggered.connect(
            self.test01)

        self.actionImportGdbImpPath = QAction()
        self.actionImportGdbImpPath.setText('Gst-Importverzeichnis neu einlesen')
        self.actionImportGdbImpPath.setIcon(
            QIcon(':/svg/icons/import.svg'))
        self.actionImportGdbImpPath.triggered.connect(self.importGdbImportPathSgn)

    def test01(self):

        print(f'...')

    def setupMenus(self):
        super().setupMenus()

        self.menuKontakte = QMenu()
        self.menuKontakte.setTitle('Kontakte')
        self.menuBar().addMenu(self.menuKontakte)
        self.menuKontakte.addAction(self.actions.get('kontakt.main_all'))

    def createMenus(self):  # löschen
        super().createMenus()

        self.menuKontakte = QMenu()
        self.menuKontakte.setTitle('Kontakte')
        self.menuKontakte.addAction(self.actionOpenKontakteAlle)

        self.menuGst = QMenu()
        self.menuGst.setTitle('Grundstücke')
        self.menuGst.addAction(self.actionOpenGstAll)
        self.menuGst.addAction(self.actionOpenGstAwb)
        # self.menuGst.addAction(self.actionOpenKontakteAlle)

        self.menuImport = QMenu()
        self.menuImport.setTitle('Import')
        self.menuImport.addAction(self.actionOpenGdbImpPath)
        self.menuImport.addAction(self.actionImportGdbImpPath)
        # self.menuGst.addAction(self.actionOpenKontakteAlle)

        self.menuAkte = QMenu()
        self.menuAkte.setTitle('Akte')
        self.menuAkte.addAction(self.actionAlleAkte)

    # def addMenus(self):
    #     super().addMenus()
    #
    #     self.menuBar().addMenu(self.menuProject)
    #     # self.menuBar().addMenu(self.menuKontakte)
    #     # self.menuBar().addMenu(self.menuGst)
    #     # self.menuBar().addMenu(self.menuAkte)
    #     # self.menuBar().addMenu(self.menuImport)
    #     # self.menuBar().addMenu(self.menuHelp)

    def setupToolBar(self):

        self.uiToolBar.addAction(self.actionOpenKontakteAlle)
        self.uiToolBar.addAction(self.actionOpenGstAll)
