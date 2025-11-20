from qga import Qga
from qga.core.start_wdg import QgaStartWdg, QgaStartOptionLast, \
    QgaStartOptionOther, QgaStartOptionNew

from almgis.database.models import DmSettings


class AlmStartWdg(QgaStartWdg):

    def __init__(self, parent=None):
        super(AlmStartWdg, self).__init__(parent)

        self.start_options = [QgaStartOptionLast(self),
                              QgaStartOptionOther(self),
                              QgaStartOptionNew(self)]

        self.settings_dmc = DmSettings

        self.last_project_file = Qga.Settings.User.value('paths/last_project_file')
