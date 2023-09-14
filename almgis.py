import sys
from qgis.core import QgsApplication, QgsProviderRegistry
from core.main_window import AlmgisMainWindow

from PyQt5.QtWidgets import QWidget

if sys.version < '3.0':
    sys.exit("This program requires a python3 runtime")


def run():

    # QgsApplication.setPrefixPath("C:/PROGRA~1/OSGeo4W/apps/qgis-ltr", True)
    QgsApplication.setPrefixPath("C:/work/_anwendungen/OSGeo4W/apps/qgis-ltr", True)
    app = QgsApplication([], True)
    app.initQgis()

    main_window = AlmgisMainWindow()
    aaa = QWidget()

    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':

    run()
