#!/usr/bin/env python

from qgis.PyQt.QtCore import QEvent
from qgis.PyQt.QtSvg import QSvgWidget
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout

import resources_rc
from app_core import db_session_cm
from app_core.data_model import McInfoButton


class InfoButton(QWidget):

    icon_size = 15
    icon_file_enter = ':/svg/resources/icons/info_blue.svg'
    icon_file_leave = ':/svg/resources/icons/info_grey.svg'
    _html_file = ""
    _info_element = None

    _info_id = 0

    @property  # getter
    def html_file(self):

        return self._html_file

    @html_file.setter
    def html_file(self, value):

        self._html_file = value

        with open(self._html_file + '.html') as f:
            self.html_text = f.read()

    @property  # getter
    def info_element(self):
        return self._info_element

    @info_element.setter
    def info_element(self, value):

        id_str = str(self.info_id)

        if value:

            self._info_element = value

            title = self._info_element.title
            content = self._info_element.content
            # id_str = str(self._info_element.id)

        else:
            title = "Info"
            content = "Keine Information vorhanden."
            # id_str = '---'

        html = '''<!DOCTYPE html>'''\
               '''<html lang="en">'''\
               '''<head>'''\
               '''<meta charset="UTF-10">'''\
               '''<title>Title</title>'''\
               '''</head>'''\
               '''<body>''' + \
               '''<b>'''+ title +'''</b>'''\
               '''<hr><br/>'''\
               + content + \
               '''<hr><p align="right">InfoID: '''\
               + id_str + \
               '''</p></body>'''\
               '''</html>'''

        self.icon_widget.setToolTip(html)

    @property  # getter
    def info_id(self):

        return self._info_id

    @info_id.setter
    def info_id(self, value):

        self._info_id = value

        with db_session_cm(name=f'set info button -{value}-') as session:
            info_mci = session.get(McInfoButton, value)

            self.info_element = info_mci

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.parent = parent

        self.setFixedWidth(25)

        lay = QVBoxLayout(self)
        self.setLayout(lay)

        self.icon_widget = QSvgWidget(self.icon_file_leave)
        self.icon_widget.setFixedHeight(self.icon_size)
        self.icon_widget.setFixedWidth(self.icon_size)

        lay.addWidget(self.icon_widget)

        self.icon_widget.installEventFilter(self)

        lay.setContentsMargins(0, 0, 0, 0)

        self.html_text = 'Noch keine Information vorhanden.'

        self.info_element = None

    def initInfoButton(self, info_id):

        self.info_id = info_id

    def eventFilter(self, event_object, event):

        if event.type() == QEvent.Enter and event_object is self.icon_widget:
            self.icon_widget.load(self.icon_file_enter)

        if event.type() == QEvent.Leave and event_object is self.icon_widget:
            self.icon_widget.load(self.icon_file_leave)

        return super().eventFilter(event_object, event)
