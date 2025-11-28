from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6 import QtGui

class MarqueeLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignVCenter)

        # Position de départ (à droite du widget)
        self.offset = self.width()

        # Timer pour le défilement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scrollText)
        self.timer.start(30)  # vitesse du défilement

        # Style du texte
        font = QtGui.QFont("Consolas", 20, QtGui.QFont.Bold)
        self.setFont(font)
        self.setStyleSheet("background-color: black; color: purple;")

    def scrollText(self):
        text_width = self.fontMetrics().horizontalAdvance(self.text())

        # Défilement vers la gauche
        self.offset -= 2

        # Si le texte est entièrement sorti à gauche, on remet au départ à droite
        if self.offset < -text_width:
            self.offset = self.width()

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setFont(self.font())
        painter.setPen(QtGui.QColor("purple"))
        painter.drawText(
            self.offset,
            int(self.height()/2 + self.fontMetrics().ascent()/2),
            self.text()
        )


