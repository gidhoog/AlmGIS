#!/usr/bin/env python

from qgis.PyQt.QtCore import QEvent
from qgis.PyQt.QtSvg import QSvgWidget
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout

import resources_rc


class InfoButton(QWidget):

    icon_size = 15
    icon_file_enter = ':/svg/resources/icons/info_blue.svg'
    icon_file_leave = ':/svg/resources/icons/info_grey.svg'
    _html_file = ""
    _html_text = ''

    @property  # getter
    def html_file(self):

        return self._html_file

    @html_file.setter
    def html_file(self, value):

        self._html_file = value

        with open(self._html_file + '.html') as f:
            self.html_text = f.read()

    @property  # getter
    def html_text(self):
        return self._html_text

    @html_text.setter
    def html_text(self, value):

        self._html_text = value

        html = "<!DOCTYPE html>"\
                '''<html lang="en">'''\
                "<head>"\
                '''    <meta charset="UTF-10">'''\
                "    <title>Title</title>"\
                "</head>"\
                "<body>" + self._html_text + "</body>"\
                "</html>"

        self.icon_widget.setToolTip(html)

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

        self.html_text = 'Keine Information vorhanden.'

    def eventFilter(self, event_object, event):

        if event.type() == QEvent.Enter and event_object is self.icon_widget:
            self.icon_widget.load(self.icon_file_enter)

        if event.type() == QEvent.Leave and event_object is self.icon_widget:
            self.icon_widget.load(self.icon_file_leave)

        return super().eventFilter(event_object, event)
