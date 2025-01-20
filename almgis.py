import sys


print(f'PATH: ++++++++++++++++++++++++++++++++++++++++++++++')
for path in sys.path:
    print(path)
print(f'++++++++++++++++++++++++++++++++++++++++++++++++++++')
from qgis.core import QgsApplication

from almgis.mainwindow import AlmMainWindow
from almgis.logger import Logger


if sys.version < '3.0':
    sys.exit("This program requires a python3 runtime")


def run():

    app = QgsApplication([], True)

    app.setPrefixPath(
        "C:/work/_anwendungen/OSGeo4W/apps/qgis-ltr",
        True)

    app.initQgis()

    main_window = AlmMainWindow()

    # main_window.setupMainWindow()

    main_window.show()

    # LOGGER.debug("almgis started! + + + + + + + + + + + + + + + + ")

    sys.exit(app.exec_())


if __name__ == '__main__':

    run()
