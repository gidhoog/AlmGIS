import platform
import sys
from time import sleep, time
from qgis.core import QgsApplication
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import QSplashScreen

from almgis import settings_user, settings_app
"""import after the settings"""
from almgis.mainwindow import AlmMainWindow
from almgis.logger import Logger
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
    splash = CustomSplashScreen(pixmap)
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
    Logger.info(f'setting_app file_name: {settings_app.fileName()}')
    Logger.info(f'setting_user file_name: {settings_user.fileName()}')



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
    # main_window.selectStartProject()

    splash.finish(main_window)

    sys.exit(app.exec_())

class CustomSplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.message = ""
        self.color = Qt.black
        self.font = QFont("Arial", 12, QFont.Bold)

    def showMessage(self, message, color=Qt.black, font=None):
        self.message = message
        self.color = color
        if font:
            self.font = font
        self.update()

    def drawContents(self, painter):
        painter.save()
        painter.setPen(QColor(self.color))
        painter.setFont(self.font)
        # Define a rectangle at the bottom of the splash screen
        margin = 20
        rect = QRect(
            margin,
            self.height() - margin - 30,  # 30 is an arbitrary height for the text area
            self.width() - 2 * margin,
            30
        )
        painter.drawText(rect, Qt.AlignCenter | Qt.AlignVCenter, self.message)
        painter.restore()



if __name__ == '__main__':

    run()
