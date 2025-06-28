from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from qga.gui.main_window_gui import QgaMainWindowGui


class AlmMainWindowGui(QgaMainWindowGui):

    def __init__(self):
        super(AlmMainWindowGui, self).__init__()

        # self.useMenuBar = False

    def setupActions(self):
        super().setupActions()

        self.actionAlleAkte = QAction()
        self.actionAlleAkte.setText('alle Akte')
        self.actionAlleAkte.setIcon(
            QIcon(':/svg/icons/mActionFileNew.svg'))

    def setupMenuBar(self):
        super().setupMenuBar()

        self.menuAkte = self.menuBar().addMenu('Akte')
        self.menuAkte.addAction(self.actionAlleAkte)

        self.menuBar().addMenu(self.menuProject)
