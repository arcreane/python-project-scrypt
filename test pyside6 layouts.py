import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(QSize(800, 600))

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QVBoxLayout()

        layout2.addWidget(QLabel("Stats"))
        layout2.addWidget(QLabel("Avions"))
        layout3.addWidget(QLabel("Vue de haut"))
        layout3.addWidget(QLabel("Message"))
        layout3.addWidget(QLabel("Piste de côté"))
        layout4.addWidget(QLabel("Contrôles"))
        layout4.addWidget(QLabel("Instructions"))
        layout4.addWidget(QLabel("Actions"))

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)
        layout1.addLayout(layout4)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()