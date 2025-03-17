import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QApplication, QDialog, QTextEdit, QToolBar, QAction, QVBoxLayout,
    QPushButton, QColorDialog, QComboBox
)
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QPixmap


# see: https://www.perplexity.ai/search/create-a-simple-wysiwyg-html-e-OgkcTcBHTEKXQpQ3v7gSow

class HTMLEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('WYSIWYG HTML Editor')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.editor = QTextEdit()
        self.editor.setFont(QFont('Times', 12))
        self.editor.setFontPointSize(12)

        test = """<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
    <h1>Hello, World!</h1>
    <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">This is a <strong>test</strong>.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>"""

        self.editor.setText(test)

        self.image_combo = QComboBox()
        self.populate_image_combo()
        self.image_combo.currentIndexChanged.connect(self.insert_image)

        self.toolbar = QToolBar()
        self.create_toolbar()

        self.accept_button = QPushButton('Accept')
        self.accept_button.clicked.connect(self.accept)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.editor)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

        # layout.addWidget(self.image_combo)

    def populate_image_combo(self):
        self.image_combo.addItem("Select an image...")
        self.image_combo.addItem("Image 1", ":/images/image1.png")
        self.image_combo.addItem("Image 2", ":/images/image2.png")
        self.image_combo.addItem("Image 3", ":/images/image3.png")

    def insert_image(self, index):
        if index > 0:  # Ignore the first item which is just a prompt
            image_path = self.image_combo.itemData(index)
            cursor = self.editor.textCursor()
            image = QPixmap(image_path)
            if not image.isNull():
                image = image.scaled(QSize(100, 100),
                                     aspectRatioMode=1)  # Scale image to 100x100 pixels
                cursor.insertImage(image)
            self.image_combo.setCurrentIndex(0)  # Reset combo box selection

    def create_toolbar(self):
        # Bold Action
        bold_action = QAction(QIcon.fromTheme('format-text-bold'), 'Bold', self)
        bold_action.triggered.connect(self.toggle_bold)
        self.toolbar.addAction(bold_action)

        # Italic Action
        italic_action = QAction(QIcon.fromTheme('format-text-italic'), 'Italic', self)
        italic_action.triggered.connect(self.toggle_italic)
        self.toolbar.addAction(italic_action)

        # Underline Action
        underline_action = QAction(QIcon.fromTheme('format-text-underline'), 'Underline', self)
        underline_action.triggered.connect(self.toggle_underline)
        self.toolbar.addAction(underline_action)

        self.font_size_combo = QComboBox()
        font_sizes = ['8', '9', '10', '11', '12', '14', '16', '18', '20', '22',
                      '24', '28', '36']
        self.font_size_combo.addItems(font_sizes)
        self.font_size_combo.setCurrentText('12')  # Default font size
        self.font_size_combo.currentTextChanged.connect(self.set_font_size)
        self.toolbar.addWidget(self.font_size_combo)

        # Color Picker Action
        color_action = QAction(QIcon.fromTheme('format-text-color'), 'Text Color', self)
        color_action.triggered.connect(self.pick_color)
        self.toolbar.addAction(color_action)

        self.toolbar.addWidget(self.image_combo)

    def toggle_bold(self):
        if self.editor.fontWeight() == QFont.Bold:
            self.editor.setFontWeight(QFont.Normal)
        else:
            self.editor.setFontWeight(QFont.Bold)

    def toggle_italic(self):
        self.editor.setFontItalic(not self.editor.fontItalic())

    def toggle_underline(self):
        self.editor.setFontUnderline(not self.editor.fontUnderline())

    def set_font_size(self, size):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontPointSize(float(size))
            cursor.mergeCharFormat(fmt)
        else:
            self.editor.setFontPointSize(float(size))

    def pick_color(self):
        # Open QColorDialog to select a color
        color = QColorDialog.getColor()

        if color.isValid():
            # Apply the selected color to the selected text
            cursor = self.editor.textCursor()
            if not cursor.hasSelection():
                cursor.select(QTextCursor.WordUnderCursor)  # Select word if no selection is made
            fmt = cursor.charFormat()
            fmt.setForeground(color)
            cursor.mergeCharFormat(fmt)

    def get_html(self):
        return self.editor.toHtml()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = HTMLEditorDialog()
    if dialog.exec_() == QDialog.Accepted:
        print(dialog.get_html())
    sys.exit(app.exec_())
