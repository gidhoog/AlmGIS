from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu
from qga.gui.main_window_gui import QgaMainWindowGui


class AlmMainWindowGui(QgaMainWindowGui):

    openKontakteAllMainWdgSgn = pyqtSignal()

    openGstMainWdgSgn = pyqtSignal()
    openGstMainAwbWdgSgn = pyqtSignal()

    def __init__(self, ctrl=None):
        super(AlmMainWindowGui, self).__init__(ctrl)

        # self.useMenuBar = False

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

    def createMenus(self):
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
        # self.menuGst.addAction(self.actionOpenKontakteAlle)

        self.menuAkte = QMenu()
        self.menuAkte.setTitle('Akte')
        self.menuAkte.addAction(self.actionAlleAkte)

    def addMenus(self):

        self.menuBar().addMenu(self.menuProject)
        self.menuBar().addMenu(self.menuKontakte)
        self.menuBar().addMenu(self.menuGst)
        self.menuBar().addMenu(self.menuAkte)
        self.menuBar().addMenu(self.menuImport)
        self.menuBar().addMenu(self.menuHelp)

    def setupToolBar(self):

        self.uiToolBar.addAction(self.actionOpenKontakteAlle)
        self.uiToolBar.addAction(self.actionOpenGstAll)
