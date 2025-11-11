import platform
import sys
from time import sleep, time

from qga import Qga, QgaSettingsUser
from qga.core.splash import QgaSplash
# from qga.splash import QgaSplash
from qgis.core import QgsApplication
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPixmap

# from almgis import settings_user
from almgis.core.logger import Logger
from almgis.core.main_window import AlmMainWindow

"""import after the settings"""
# from almgis.mainwindow import AlmMainWindow
# from almgis.logger import Logger
""""""

# print(f'PATH: ++++++++++++++++++++++++++++++++++++++++++++++')
# for path in sys.path:
#     print(path)
# print(f'++++++++++++++++++++++++++++++++++++++++++++++++++++')

if sys.version < '3.0':
    sys.exit("This program requires a python3 runtime")

def run():

    app = QgsApplication([], True)

    """use a splashscreen"""
    start = time()
    pixmap = QPixmap("splash.png")
    splash = QgaSplash(pixmap)
    splash.showMessage("Die Anwendung wird geladen, "
                       "bitte warten ...",
                       Qt.black)
    splash.show()

    while time() - start < 0.3:
        # sleep(0.001)
        app.processEvents()
    """remove if you want, only needed to show the splashscreen longer!"""
    sleep(2.0)
    """"""

    Logger.info("+ + + + AlmGis gestartet !!! + + + +")
    # Logger.info(f'setting_app file_name: {settings_app.fileName()}')
    # Logger.info(f'setting_user file_name: {settings_user.fileName()}')

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

    # app.setOrganizationName('NoeABB2')
    # app.setApplicationName('AlmGIS2')
    #
    # Qga.SettingsUser = QgaSettingsUser(QSettings.IniFormat, QSettings.UserScope, 'NoeABB2', 'AlmGIS2')

    main_window = AlmMainWindow()
    # main_window.setWindowState(Qt.WindowMaximized)
    main_window.setupMainWindow()
    main_window.ui.show()

    splash.finish(main_window.ui)

    sys.exit(app.exec())


if __name__ == '__main__':

    run()
