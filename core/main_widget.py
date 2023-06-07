
from PyQt5.QtCore import pyqtSlot, pyqtSignal


class MainWidget:
    """
    baseclass für ein widget, das direkt im 'AlmgisMainWindow' platziert ist;
    es ist in einen DisplayAreaFrame eingebettet
    """

    update_app = pyqtSignal()

    def updateMainWidget(self):
        """
        methode um das main_widget zu aktualisieren
        """
        pass

    @pyqtSlot()
    def do_update_application(self):

        self.update_app.emit()
