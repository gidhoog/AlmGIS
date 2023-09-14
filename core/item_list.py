#!/usr/bin/env python

from functools import partial

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QFrame, \
    QLabel, QPushButton, QWidget, QSplitter


class Itemlist(QWidget):
    """
    eine Klasse um einzelne Elemente (ListItem) in einer Liste darzustellen
    """

    changendListElements = pyqtSignal(list)

    """a dict with the selected items; id as key and data as value"""
    _itemlist = {}
    """a list with the possible instances for this item_list"""
    _possible_instances = []
    """"""

    item_id_list = []

    parent = 0

    @property  # getter
    def itemlist(self):

        return self._itemlist

    @itemlist.setter
    def itemlist(self, value):

        self._itemlist = value

    @property  # getter
    def possible_instances(self):

        self._possible_instances = self.getPossibleInstances()

        return self._possible_instances

    @possible_instances.setter
    def possible_instances(self, value):

        self._possible_instances = value

    def __init__(self, parent):
        super(Itemlist, self).__init__(parent)

        self.parent = parent

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def initItemlist(self, item_list):

        """convert the given tag_string to a list, set the tag-list and
        refresh the tag_bar;
        this code considers if the string is empty"""

        self.itemlist = item_list

        self.setItemlist(self.itemlist)

    def getItemIds(self):

        return self.item_id_list

    def setItemlist(self, item_list):

        horrSplitter = QSplitter()
        horrSplitter.setOrientation(Qt.Horizontal)
        self.layout.addWidget(horrSplitter)

        self.item_id_list = []

        sort_item_list = sorted(item_list.items(),
                                key=lambda x: x[1],
                                reverse=True)

        for item in sort_item_list:

            element = ListItem(self,
                               item_id=item[0],
                               item_text=item[1])

            element.adjustSize()
            print(f"{item[1]}-width: {element.width()}     layout-size:{self.width()}")

            element.del_button.clicked.connect(
                lambda a, del_pers=item[0]: self.delListItem(del_pers))

            self.item_id_list.append(item[0])
            self.layout.insertWidget(0, element)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:

        print(f".............{self.__class__.__name__} resized!!!!!")

        super().resizeEvent(a0)

    def delListItem(self, item_id):
        """
        delete a item from the list with the given item_id
        :param item_id:
        :return:
        """
        pass

    def clearLayout(self):

        for i in reversed(range(self.layout.count())):

            wid = self.layout.itemAt(i).widget()
            wid.deleteLater()
            self.layout.removeWidget(wid)
            wid.setParent(None)

    def getPossibleInstances(self):
        """
        create a list with the possible instances and return it
        :return:
        """
        return []

class ListItem(QFrame):
    """
    ein Element in der ItemList
    """

    _item_id = None
    _item_text = ""

    active_icon_path = ':/svg/resources/icons/small_delete_cross_active'
    inactive_icon_path = ':/svg/resources/icons/small_delete_cross_inactive'

    @property  # getter
    def item_id(self):

        return self._item_id

    @item_id.setter
    def item_id(self, value):

        self._item_id = value

    @property  # getter
    def item_text(self):

        self._item_text = self.guiTagBar.getTagString()
        return self._item_text

    @item_text.setter
    def item_text(self, value):

        self.guiTagBar.initTagBar(value)
        self._item_text = value

    def __init__(self, parent=None, item_text=None, item_id=None):
        super(ListItem, self).__init__(parent)

        self.parent = parent

        self.active_icon = QIcon(self.active_icon_path)
        self.inactive_icon = QIcon(self.inactive_icon_path)

        self.item_id = item_id

        self.setStyleSheet('border:1px solid rgb(192, 192, 192); border-radius: 4px;')
        self.setContentsMargins(2, 2, 2, 2)
        self.setFixedHeight(28)

        element_layout = QHBoxLayout()
        element_layout.setContentsMargins(2, 2, 2, 2)
        element_layout.setSpacing(2)
        self.setLayout(element_layout)

        label = QLabel(str(item_text))
        label.setStyleSheet('border:0px')
        label.setFixedHeight(16)
        element_layout.addWidget(label)

        # self.del_button = QPushButton('x')
        self.del_button = QPushButton(self)
        # icon = QIcon(':/svg/resources/icons/small_delete_cross_inactive')
        self.del_button.setIcon(self.inactive_icon)
        self.del_button.setIconSize(QSize(8, 8))
        # self.del_button.setFixedSize(20, 20)
        self.del_button.setStyleSheet('border:0px; font-weight:bold')
        self.del_button.installEventFilter(self)
        # self.del_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.del_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.del_button.setFixedWidth(12)
        element_layout.addWidget(self.del_button)

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

    def eventFilter(self, event_object, event):

        if event.type() == QEvent.Enter and event_object is self.del_button:
            self.del_button.setIcon(self.active_icon)

        if event.type() == QEvent.Leave and event_object is self.del_button:
            self.del_button.setIcon(self.inactive_icon)

        return super().eventFilter(event_object, event)
