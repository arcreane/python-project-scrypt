# esthetisme_boutons_jeu.py
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt


class ImageButton(QPushButton):
    """
    QPushButton personnalisé affichant une image de fond
    avec le texte centré par-dessus.
    """

    def __init__(self, text="", image_path=None, parent=None):
        super().__init__(text, parent)
        self.image_path = image_path
        self.pixmap = QPixmap(image_path) if image_path else None
        self.scaled_pixmap = None

        # Style de base
        self.setStyleSheet("color: white; font-weight: bold;")
        self.setMinimumHeight(60)

    # Redimensionnement
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.pixmap:
            # Mise à l’échelle de l’image à la taille actuelle du bouton
            self.scaled_pixmap = self.pixmap.scaled(
                self.width(),
                self.height(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )

    # Dessin personnalisé
    def paintEvent(self, event):
        painter = QPainter(self)

        # Dessiner l’image mise à l’échelle
        if self.scaled_pixmap:
            painter.drawPixmap(0, 0, self.scaled_pixmap)

        # Dessiner le texte centré par-dessus
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

        painter.end()
