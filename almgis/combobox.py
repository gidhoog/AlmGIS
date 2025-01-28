from qga.combobox import ActionAdd

from almgis.data_session import session_cm


class AlmActionAdd(ActionAdd):

    def __init__(self, parent):
        super(ActionAdd, self).__init__(parent)

        self.session_cm = session_cm