from PyQt5.QtWidgets import QDialog
from qga.entity import QgaEntity, QgaEntityDialog

from almgis import ProjectSessionCls
# from almgis import DbSession
# from almgis.data_view import AlmDataView
from almgis.logger import Logger


class AlmEntity(QgaEntity):

    def __init__(self, parent=None):
        super(AlmEntity, self).__init__(parent)

        self.session = ProjectSessionCls()
        self.logger = Logger


class AlmEntityDialog(QgaEntityDialog):

    def __init__(self, parent=None):
        super(AlmEntityDialog, self).__init__(parent)
