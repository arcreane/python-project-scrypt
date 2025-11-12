import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFrame
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

        label = QLabel("Stats")
        label.setFrameShape(QFrame.Panel)
        label2 = (QLabel("Avions"))
        label2.setFrameShape(QFrame.Panel)
        label3 = (QLabel("Vue de haut"))
        label3.setFrameShape(QFrame.Panel)
        label4 = (QLabel("Message"))
        label4.setFrameShape(QFrame.Panel)
        label5 = (QLabel("Piste de côté"))
        label5.setFrameShape(QFrame.Panel)
        label6 = (QLabel("Contrôles"))
        label6.setFrameShape(QFrame.Panel)
        label7 = (QLabel("Instructions"))
        label7.setFrameShape(QFrame.Panel)
        label8 = (QLabel("Actions"))
        label8.setFrameShape(QFrame.Panel)

        layout2.addWidget(label)
        layout2.addWidget(label2)
        layout3.addWidget(label3)
        layout3.addWidget(label4)
        layout3.addWidget(label5)
        layout4.addWidget(label6)
        layout4.addWidget(label7)
        layout4.addWidget(label8)

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