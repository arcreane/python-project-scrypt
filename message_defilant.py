# MarqueeLabel.py
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6 import QtGui


# Classe : Label déroulant
class MarqueeLabel(QLabel):
    """
    QLabel personnalisé affichant un texte défilant horizontalement.
    """

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        # Alignement et texte
        self.setAlignment(Qt.AlignVCenter)
        self.offset = self.width()  # Position initiale du texte (à droite)

        # Timer pour le défilement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._scroll_text)
        self.timer.start(30)  # Vitesse du défilement en ms

        # Style du texte
        font = QtGui.QFont("Consolas", 20, QtGui.QFont.Bold)
        self.setFont(font)
        self.setStyleSheet("background-color: black; color: pink;")

    # Méthodes privées
    def _scroll_text(self):
        """
        Décale le texte vers la gauche et le remet à droite
        lorsqu'il sort complètement du widget.
        """
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        self.offset -= 2  # vitesse de défilement

        # Reset si le texte est complètement sorti
        if self.offset < -text_width:
            self.offset = self.width()

        self.update()

    def paintEvent(self, event):
        """
        Dessine le texte avec l'offset courant.
        """
        painter = QtGui.QPainter(self)
        painter.setFont(self.font())
        painter.setPen(QtGui.QColor("pink"))

        x = self.offset
        y = int(self.height() / 2 + self.fontMetrics().ascent() / 2)
        painter.drawText(x, y, self.text())
