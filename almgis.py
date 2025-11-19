import platform
import sys
from time import sleep, time

from qga.core.logger import setupLogger
from qga.core.splash import QgaSplash
from qgis.core import QgsApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from almgis.core.main_window import AlmMainWindow
from almgis.core.settings import setupSettings

import logging

# print(f'PATH: ++++++++++++++++++++++++++++++++++++++++++++++')
# for path in sys.path:
#     print(path)
# print(f'++++++++++++++++++++++++++++++++++++++++++++++++++++')

if sys.version < '3.0':
    sys.exit("This program requires a python3 runtime")


def run():
    """
    app entry point
    :return:
    """

    """setup app basics"""
    setupSettings()
    setupLogger('almgis.log')
    """"""

    app_log = logging.getLogger(__name__)

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

    if platform.system() == 'Linux':
        app.setPrefixPath("/var/lib/flatpak/app/org.qgis.qgis",
                          True)
    elif platform.system() == 'Windows':
        app.setPrefixPath("C:/work/_anwendungen/OSGeo4W/apps/qgis-ltr",
                          True)
    else:
        app_log.error(f'cannot set PrefixPath for QGIS! --> Quit app!')
        return

    app_log.debug("+ + + + AlmGis gestartet !!! + + + +")

    app.initQgis()

    main_window = AlmMainWindow()
    # main_window.setWindowState(Qt.WindowMaximized)
    main_window.setupMainWindow()
    main_window.ui.show()

    splash.finish(main_window.ui)

    sys.exit(app.exec())


if __name__ == '__main__':

    run()
