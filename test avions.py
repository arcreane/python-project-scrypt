import sys
import random

from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QGridLayout,
    QWidget,
)

couleurs = ['red', 'green', 'blue', 'orange', 'magenta', 'cyan', 'black']

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(QSize(800, 800))

        layout = QGridLayout()
        for i in range(100):
            layout.setRowMinimumHeight(i,100)
            layout.setColumnMinimumWidth(i,100)

        for i in range(7):
            coo = (random.randint(0,99), random.randint(0,99))
            while layout.itemAtPosition(coo[0], coo[1]) != None:
                coo = (random.randint(0, 99), random.randint(0, 99))
            layout.addWidget(Color(couleurs[i]), coo[0], coo[1])

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()