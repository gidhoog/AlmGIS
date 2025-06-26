from qga.core.start_wdg import QgaStartWdg, QgaStartOptionLast, \
    QgaStartOptionOther, QgaStartOptionNew

from almgis import settings_user
from almgis.core.logger import Logger
from almgis.database.models import DmSettings

class AlmStartWdg(QgaStartWdg):

    def __init__(self, parent=None):
        super(AlmStartWdg, self).__init__(parent)

        self.logger = Logger

        self.start_options = [QgaStartOptionLast(self),
                              QgaStartOptionOther(self),
                              QgaStartOptionNew(self)]

        self.settings_dmc = DmSettings

        self.last_project_file = settings_user.value('paths/last_project_file')
