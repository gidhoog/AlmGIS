from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QPushButton, \
    QHBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a menu bar
        menubar = self.menuBar()

        # Create a left corner widget
        leftCornerWidget = QPushButton()
        button = QPushButton("Left")
        layout = QHBoxLayout(leftCornerWidget)
        layout.addWidget(button)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        leftCornerWidget.setLayout(layout)

        # Add the widget to the left corner
        menubar.setCornerWidget(leftCornerWidget, Qt.TopLeftCorner)

        # Create a right corner widget
        # rightCornerWidget = QPushButton()
        rightButton = QPushButton("Right")
        # rightLayout = QHBoxLayout(rightCornerWidget)
        # rightLayout.addWidget(rightButton)
        # rightLayout.setContentsMargins(0, 0, 0, 0)
        # rightCornerWidget.setLayout(rightLayout)

        # Add the widget to the right corner
        menubar.setCornerWidget(rightButton, Qt.TopRightCorner)


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
