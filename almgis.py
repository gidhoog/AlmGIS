import platform
import sys

from PyQt5.QtCore import Qt

from almgis import settings_user, settings_app

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

    Logger.info("+ + + + AlmGis gestartet !!! + + + +")
    Logger.info(f'setting_app file_name: {settings_app.fileName()}')
    Logger.info(f'setting_user file_name: {settings_user.fileName()}')

    app = QgsApplication([], True)

    if platform.system() == 'Linux':
        app.setPrefixPath("/var/lib/flatpak/app/org.qgis.qgis",
                          True)
    elif platform.system() == 'Windows':
        app.setPrefixPath("C:/work/_anwendungen/OSGeo4W/apps/qgis-ltr",
                          True)
    else:
        Logger.error(f'cannot set PrefixPath for QGIS! --> Quit app!')
        return

    app.initQgis()

    main_window = AlmMainWindow()
    main_window.setWindowState(Qt.WindowMaximized)
    main_window.show()
    main_window.setupMainWindow()
    main_window.selectStartProject()

    sys.exit(app.exec_())


if __name__ == '__main__':

    run()
