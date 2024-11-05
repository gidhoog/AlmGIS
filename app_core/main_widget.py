from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
from qgis.PyQt.QtWidgets import QMainWindow

from app_core import main_widget_UI


# class MainWidget(QWidget, main_widget_UI.Ui_MainWidget):
class MainWidget(QMainWindow, main_widget_UI.Ui_MainWidget):
    """
    baseclass für ein widget, das direkt im 'AlmgisMainWindow' platziert ist;
    es ist in einen DisplayAreaFrame eingebettet
    """

    update_app = pyqtSignal()

    def __init__(self, parent=None, session=None):
        super(__class__, self).__init__()
        self.setupUi(self)

    def initMainWidget(self):
        """
        methode zum initialisieren des Mainwidget's
        :return:
        """
        pass

    def updateMainWidget(self):
        """
        methode um das main_widget zu aktualisieren
        """
        pass

    @pyqtSlot()
    def do_update_application(self):

        self.update_app.emit()
