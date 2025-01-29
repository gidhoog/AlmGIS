from qga.entity import QgaEntity, QgaEntityDialog

from almgis import DbSession
from almgis.data_view import AlmDataView
from almgis.logger import Logger


class AlmEntity(QgaEntity):

    def __init__(self, parent=None):
        super(AlmEntity, self).__init__(parent)

        self.logger = Logger
        self.entity_session = DbSession


class AlmEntityDialog(QgaEntityDialog):

    def __init__(self, parent=None):
        super(AlmEntityDialog, self).__init__(parent)
