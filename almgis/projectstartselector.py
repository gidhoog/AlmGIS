from qga.projectstartselector import *

from almgis import settings_user
from almgis.data_model import McSettings
from almgis.logger import Logger


class AlmStartDialog(StartDialog):

    def __init__(self, parent=None):
        super(AlmStartDialog, self).__init__(parent)

        self.logger = Logger


class AlmProjectStartSelector(QgaProjectStartSelector):

    def __init__(self, parent=None):
        super(AlmProjectStartSelector, self).__init__(parent)

        self.logger = Logger

        self.start_options = [QgaStartOptionLast(self),
                              QgaStartOptionOther(self),
                              QgaStartOptionNew(self)]

        self.settings_mc = McSettings

        self._last_project_file = settings_user.value('paths/last_project_file')
