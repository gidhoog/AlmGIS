import sys

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItemModel
from qgis.PyQt.QtWidgets import QWidget

from core import db_session_cm
from core.data_model import BRechtsgrundlage, BGstAwbStatus
from core.scopes.gst import gst_gemeinsame_werte_UI


class GstGemeinsameWerte(gst_gemeinsame_werte_UI.Ui_GstGemeinsameWerte, QWidget):
    """mit diesem Formular können ein oder mehrere Gst zugeordnet werden"""

    def __init__(self, parent=None):
        super(__class__, self).__init__()

        self.setupUi(self)

        self.parent = parent

        self.initWidget()

    def initWidget(self):

        self.setAwbStatusCombo()
        self.setRechtsgrundlageCombo()

    def setAwbStatusCombo(self):

        try:
            with db_session_cm() as session:
                session.expire_on_commit = False
                awb_status_query = session.query(BGstAwbStatus)\
                    .order_by(BGstAwbStatus.sort)\
                    .all()

            """erstelle ein model mit 2 spalten für das awb-status-combo"""
            self.awb_status_model = QStandardItemModel(len(awb_status_query), 2)
            for i in range(len(awb_status_query)):
                id = awb_status_query[i].id
                name = awb_status_query[i].name
                self.awb_status_model.setData(self.awb_status_model.index(i, 0),
                                              id, Qt.EditRole)
                self.awb_status_model.setData(self.awb_status_model.index(i, 1),
                                              name, Qt.DisplayRole)
                self.awb_status_model.setData(self.awb_status_model.index(i, 0),
                                              awb_status_query[i], Qt.UserRole)

            """"""

            """weise dem combo das model zu"""
            self.uiAwbStatusCombo.setModel(self.awb_status_model)
            self.uiAwbStatusCombo.setModelColumn(1)
            """"""
        except:
            print(f"Error in '{self.__class__.__name__}':", sys.exc_info())

    def setRechtsgrundlageCombo(self):

        try:
            with db_session_cm() as session:
                session.expire_on_commit = False
                rechtsgrunglage_query = session.query(BRechtsgrundlage)\
                    .order_by(BRechtsgrundlage.sort)\
                    .all()

            self.rechtsgrundlage_model = QStandardItemModel(len(rechtsgrunglage_query), 2)

            for i in range(len(rechtsgrunglage_query)):
                id = rechtsgrunglage_query[i].id
                name = rechtsgrunglage_query[i].name
                self.rechtsgrundlage_model.setData(self.rechtsgrundlage_model.index(i, 0), id, Qt.EditRole)
                self.rechtsgrundlage_model.setData(self.rechtsgrundlage_model.index(i, 1), name, Qt.DisplayRole)
                self.rechtsgrundlage_model.setData(self.rechtsgrundlage_model.index(i, 0), rechtsgrunglage_query[i], Qt.UserRole)

            self.uiRechtsformCombo.setModel(self.rechtsgrundlage_model)
            self.uiRechtsformCombo.setModelColumn(1)
            print(f"rechtsgrundlage wurde gesetzt")
        except:
            print("Error:", sys.exc_info())

    def reject(self):

        print(f"Abbruch")

    def accept(self):

        print(f"OKAY")
