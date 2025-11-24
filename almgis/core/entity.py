from PyQt5.QtWidgets import QDialog
from qga.core.entity import QgaEntity


from qga.core.entity import QgaEntity, QgaEntityDialog
from qga import Qga

# from almgis import ProjectSessionCls
from almgis.core.dialog import AlmDialog
# from almgis.database.sessions import session_cm, AlmPrjSessionCm


#
# from almgis import ProjectSessionCls
# # from almgis import DbSession
# # from almgis.data_view import AlmDataView
# from almgis.logger import Logger


class AlmEntity(QgaEntity):

    def __init__(self, parent=None, session=None, entity_dlg=None):
        super(AlmEntity, self).__init__(parent, session, entity_dlg)

        # self.session = Qga.ProjectSessionCls()
        # self.session_cm = session_cm()
        # self.prj_session_cm = AlmPrjSessionCm
        # self.logger = Logger


class AlmEntityDialog(AlmDialog):

    def __init__(self, parent=None):
        super(AlmEntityDialog, self).__init__(parent)


