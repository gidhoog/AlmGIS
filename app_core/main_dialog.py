from app_core import main_dialog_UI
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox


class MainDialog(QDialog, main_dialog_UI.Ui_MainDialog):
    """
    baseclass für alle dialoge
    """

    extension_frame = None

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        self._parent = parent

        self.dialog_size = []  # w, h

        self._dialog_window_title = 'AlmGIS'

        self.dialogWidget = None

        self._guiButtonsDbbox = QDialogButtonBox(self)
        self._guiButtonsDbbox.setOrientation(Qt.Horizontal)
        self._guiButtonsDbbox.setStandardButtons(
            self._guiButtonsDbbox.Cancel | self._guiButtonsDbbox.Ok)

        self._guiCancelDbtn = self._guiButtonsDbbox.button(
            self._guiButtonsDbbox.Cancel)
        self._guiApplyDbtn = self._guiButtonsDbbox.button(
            self._guiButtonsDbbox.Ok)

        self._guiApplyDbtn.setVisible(False)

        self._guiButtonsDbbox.clicked.connect(self._clicked)

        self._enableApply = False

        self.uiButtonsHlay.addWidget(self._guiButtonsDbbox)

    @property  # getter
    def dialog_window_title(self):
        return self._dialog_window_title

    @dialog_window_title.setter
    def dialog_window_title(self, dialog_window_title):
        """
        set the dialog_window_title
        """
        self.setWindowTitle(dialog_window_title)

        self._dialog_window_title = dialog_window_title

    @property  # getter
    def enableApply(self):
        return self._dialog_window_title

    @enableApply.setter
    def enableApply(self, enableApply):
        """
        aktiviere den 'apply' button
        """
        self._guiApplyDbtn.setVisible(enableApply)
        self._guiApplyDbtn.setEnabled(enableApply)
        self._guiApplyDbtn.setAutoDefault(enableApply)

        self._enableApply = enableApply

    def centerDialogInGivenWidget(self, widget):
        """zentriere den dialog im übergebenen widget
        """

        """hole die globale position des widgets"""
        pos = widget.mapToGlobal(widget.pos())
        """"""

        if widget is not None:
            px = pos.x()
            py = pos.y()
            py2 = widget.geometry().y()
            pw = widget.geometry().width()
            ph = widget.geometry().height()

        """setze die neue x position des widgets"""
        new_x = pos.x()+(widget.size().width()/2) - (
                self.dialogWidget.size().width() / 2)

        # new_y = pos.y()-py2 + 20
        new_y = pos.y()-py2

        self.setGeometry(int(new_x), int(new_y), self.dialogWidget.size().width(),
                         self.dialogWidget.size().height())
        """"""

    def initDialog(self, entity_widget, center_in=None, width=None, height=None):
        """
        initialisiere den dialog
        """

        self.insertWidget(entity_widget)
        self.resize(self.minimumSizeHint())

        if width is not None and height is not None:
            self.resize(width, height)
        elif self.dialog_size != []:
            self.resize(self.dialog_size[0], self.dialog_size[1])

        if center_in is not None:
            self.centerDialogInGivenWidget(center_in)

    def set_apply_button_text(self, text):
        """
        ändere den text für den 'apply' button
        """
        self._guiApplyDbtn.setText(text)

    def set_reject_button_text(self, text):
        """
        ändere den text für den 'reject' button
        """
        self._guiCancelDbtn.setText(text)

    def insertWidget(self, widg):
        """
        füge das widget unten im layout ein
        """
        self.dialogWidget = widg
        # self.dialogWidget.adjustSize()

        self.uiWidgetsVlay.addWidget(self.dialogWidget)

    def _clicked(self, but):
        """
         methode die aufgerufen wird , wenn ein button der QDialogButtonBox
         gedrückt wird
         """

        """hole die rolle der QDialogButtonBox"""
        role = self._guiButtonsDbbox.buttonRole(but)

        if role == QDialogButtonBox.AcceptRole:
            self.accept()

        elif role == QDialogButtonBox.ApplyRole:
            self.accept()

        elif role == QDialogButtonBox.RejectRole:
            self.reject()

    def accept(self) -> None:
        """
        subclass in subclassed classes; important to call
        'QDialog.accept(self)' in the 'top'-subclass
        (e.g. AktDialog) to finish (z.g. close) the dialog
        """
        QDialog.accept(self)

    def reject(self):

        QDialog.reject(self)
