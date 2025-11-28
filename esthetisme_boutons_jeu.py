#esthetisme_boutons_jeu.py
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt

class ImageButton(QPushButton):
    def __init__(self, text="", image_path=None, parent=None):
        super().__init__(text, parent)
        self.image_path = image_path
        self.pixmap = QPixmap(image_path) if image_path else None
        self.setStyleSheet("color: white; font-weight: bold;")
        self.setMinimumHeight(60)
        self.scaled_pixmap = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.pixmap:
            self.scaled_pixmap = self.pixmap.scaled(
                self.width(), self.height(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.scaled_pixmap:
            painter.drawPixmap(0, 0, self.scaled_pixmap)

        # Texte centré par-dessus l'image
        painter.setPen(QColor(255, 255, 255))  # couleur du texte
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

        painter.end()
