import sys


print(f'PATH: ++++++++++++++++++++++++++++++++++++++++++++++')
for path in sys.path:
    print(path)
print(f'++++++++++++++++++++++++++++++++++++++++++++++++++++')
from qgis.core import QgsApplication
from app_core.main_window import AlmgisMainWindow
from app_core.logger import LOGGER
from importlib import resources

# from PyQt5.QtWidgets import QWidget

if sys.version < '3.0':
    sys.exit("This program requires a python3 runtime")


def run():

    # QgsApplication.setPrefixPath("C:/PROGRA~1/OSGeo4W/apps/qgis-ltr", True)
    QgsApplication.setPrefixPath("C:/work/_anwendungen/OSGeo4W/apps/qgis-ltr", True)
    app = QgsApplication([], True)
    # app.setPrefixPath("/var/lib/flatpak/app/org.qgis.qgis", True)
    app.initQgis()

    main_window = AlmgisMainWindow()
    # aaa = QWidget()

    main_window.setupMainWindow()

    main_window.show()

    LOGGER.debug("almgis started! + + + + + + + + + + + + + + + + ")

    sys.exit(app.exec_())


if __name__ == '__main__':

    run()
