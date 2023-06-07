from PyQt5.QtWidgets import QWidget
from core import print_content_widget_UI


class PrintContentWidget(print_content_widget_UI.Ui_PrintContentWidget, QWidget):
    """
    klasse um beim erstellen eines kartenausdruckes im main_gis zusätzliche
    informationen, die dann in der karte engefügt werden, abzufragen
    """

    _content = ''
    _remark = ''
    _user = ''

    @property  # getter
    def content(self):

        self._content = self.uiContentLedit.text()
        return self._content

    @content.setter
    def content(self, value):

        self.uiContentLedit.setText(value)
        self._content = value

    @property  # getter
    def user(self):

        self._user = self.uiUserLedit.text()
        return self._user

    @user.setter
    def user(self, value):

        self.uiUserLedit.setText(value)
        self._user = value

    @property  # getter
    def remark(self):

        self._remark = self.uiRemarkTedit.toPlainText()
        return self._remark

    @remark.setter
    def remark(self, value):

        self.uiRemarkTedit.setPlainText(value)
        self._remark = value

    def __init__(self, parent=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent
