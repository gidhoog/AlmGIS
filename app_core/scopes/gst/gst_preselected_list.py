#!/usr/bin/env python
from app_core import db_session_cm
from app_core.data_model import BGst
from app_core.item_list import Itemlist


class PreselectedGstList(Itemlist):
    """
    Liste mit den für die Zuordnung vorgemerkten Grundstücken;
    ein Grundstück ist ein Element der Liste
    """

    def __init__(self, parent):
        super(PreselectedGstList, self).__init__(parent)

    def getPossibleInstances(self):

        with db_session_cm() as session:
            # session.expire_on_commit = False

            possible_inst = session.query(BGst.id, BGst.gst, BGst)\
                .all()

        return possible_inst

    def delListItem(self, item_id):

        self.parent.delPerson(item_id)


