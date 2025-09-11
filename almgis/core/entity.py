from PyQt5.QtWidgets import QDialog
from qga.core.entity import QgaEntity


from qga.core.entity import QgaEntity, QgaEntityDialog

from almgis.core.dialog import AlmDialog


#
# from almgis import ProjectSessionCls
# # from almgis import DbSession
# # from almgis.data_view import AlmDataView
# from almgis.logger import Logger


class AlmEntity(QgaEntity):

    def __init__(self, parent=None):
        super(AlmEntity, self).__init__(parent)

        # self.session = ProjectSessionCls()
        # self.logger = Logger


class AlmEntityDialog(AlmDialog):

    def __init__(self, parent=None):
        super(AlmEntityDialog, self).__init__(parent)


