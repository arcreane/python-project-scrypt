# Informations_avions.py
from PySide6.QtWidgets import QLabel, QWidget, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen

# Classe : Label avec contour noir pour le texte
class ContouredLabel(QLabel):
    """
    QLabel personnalisé avec contour noir autour du texte.
    Utilisé pour afficher le nom des avions.
    """
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.font())
        rect = self.rect()
        text = self.text()

        # Dessin du contour noir
        pen = QPen(QColor(0, 0, 0))
        painter.setPen(pen)
        for dx, dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
            painter.drawText(rect.translated(dx, dy), Qt.AlignCenter, text)

        # Dessin du texte blanc au-dessus
        pen.setColor(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(rect, Qt.AlignCenter, text)
        painter.end()


# Classe : Barre de progression avec contour du texte
class ContouredProgressBar(QProgressBar):
    """
    QProgressBar avec texte contourné pour améliorer la lisibilité.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTextVisible(True)
        self.setMinimumHeight(50)

    def paintEvent(self, event):
        # Dessin standard de la barre
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.font())
        rect = self.rect()
        text = self.text()

        # Dessin du contour noir
        pen = QPen(QColor(0, 0, 0))
        painter.setPen(pen)
        for dx, dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
            painter.drawText(rect.translated(dx, dy), Qt.AlignCenter, text)

        # Dessin du texte blanc au-dessus
        pen.setColor(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(rect, Qt.AlignCenter, text)
        painter.end()


# Classe : Boussole avec cap et aiguille rouge
class ContouredCompass(QWidget):
    """
    Widget représentant une boussole avec N/E/S/W et aiguille indiquant le cap.
    """
    def __init__(self):
        super().__init__()
        self.cap = 0
        self.setMinimumSize(100, 100)
        self.setMaximumSize(200, 200)

    def set_cap(self, cap):
        """
        Met à jour le cap (0-359) et force le rafraîchissement du widget.
        """
        try:
            self.cap = float(cap) % 360
        except Exception:
            self.cap = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Calculs de base
        size = min(self.width(), self.height())
        center_x, center_y = self.width() // 2, self.height() // 2
        radius = size // 2 - 8

        # Fond carré avec bord arrondi
        square_size = size
        top_left_x = center_x - square_size // 2
        top_left_y = center_y - square_size // 2
        painter.setBrush(QColor(34, 34, 34))
        painter.setPen(QPen(QColor(68, 68, 68), 2))
        painter.drawRoundedRect(top_left_x, top_left_y, square_size, square_size, 8, 8)

        # Cercle intérieur
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)

        # N/E/S/W avec contour noir et texte blanc
        painter.setFont(self.font())
        padding = 6
        offsets = {
            "N": (0, -radius + padding),
            "E": (radius - padding, 0),
            "S": (0, radius - padding),
            "W": (-radius + padding, 0)
        }

        for label, (dx, dy) in offsets.items():
            x, y = center_x + dx, center_y + dy

            # contour noir
            for ox, oy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
                painter.setPen(QColor(0,0,0))
                painter.drawText(int(x+ox-4), int(y+oy+4), label)

            # texte blanc
            painter.setPen(QColor(255,255,255))
            painter.drawText(int(x-4), int(y+4), label)

        # Aiguille rouge pour le cap
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.cap)
        painter.setPen(QPen(QColor(255,0,0), 2))
        painter.setBrush(QColor(255,0,0))
        painter.drawLine(0, 0, 0, -int(radius*0.78))
        painter.restore()

        painter.end()
