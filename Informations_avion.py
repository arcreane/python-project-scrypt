from PySide6.QtWidgets import QLabel, QWidget, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen


# Nom de l'avion
class ContouredLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.font())
        text = self.text()
        rect = self.rect()

        # Contour noir
        pen = QPen(QColor(0, 0, 0))
        painter.setPen(pen)
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for dx, dy in offsets:
            painter.drawText(rect.translated(dx, dy), Qt.AlignCenter, text)

        # Texte blanc au-dessus
        pen = QPen(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(rect, Qt.AlignCenter, text)
        painter.end()


# Barres progressives
class ContouredProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTextVisible(True)
        self.setMinimumHeight(50)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.font())

        text = self.text()
        rect = self.rect()

        # Contour noir
        pen = QPen(QColor(0, 0, 0))
        painter.setPen(pen)
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for dx, dy in offsets:
            painter.drawText(rect.translated(dx, dy), Qt.AlignCenter, text)

        # Texte blanc au-dessus
        pen = QPen(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(rect, Qt.AlignCenter, text)
        painter.end()


# Boussole
class ContouredCompass(QWidget):
    def __init__(self):
        super().__init__()
        self.cap = 0
        self.setMinimumSize(100, 100)
        self.setMaximumSize(200, 200)

    def set_cap(self, cap):
        try:
            self.cap = float(cap) % 360
        except Exception:
            self.cap = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # carré basé sur la plus petite dimension
        size = min(self.width(), self.height())
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = size // 2 - 8

        # Fond carré avec bord arrondi
        square_size = size
        top_left_x = center_x - square_size // 2
        top_left_y = center_y - square_size // 2
        painter.setBrush(QColor(34, 34, 34))  # fond sombre
        painter.setPen(QPen(QColor(68, 68, 68), 2))  # bordure
        painter.drawRoundedRect(top_left_x, top_left_y, square_size, square_size, 8, 8)

        # Cercle intérieur plus visible
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)

        # N/E/S/W avec contour noir et texte blanc
        painter.setFont(self.font())
        padding_text = 6  # distance entre le cercle et le texte
        offsets = {
            "N": (0, -radius + padding_text),
            "E": (radius - padding_text, 0),
            "S": (0, radius - padding_text),
            "W": (-radius + padding_text, 0)
        }

        for label, (dx, dy) in offsets.items():
            x = center_x + dx
            y = center_y + dy

            # contour noir
            for ox, oy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
                painter.setPen(QColor(0,0,0))
                painter.drawText(int(x+ox-4), int(y+oy+4), label)

            # texte blanc
            painter.setPen(QColor(255,255,255))
            painter.drawText(int(x-4), int(y+4), label)

        # Aiguille rouge pointant vers le cap de l’avion
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.cap)
        pen = QPen(QColor(255,0,0), 2)
        painter.setPen(pen)
        painter.setBrush(QColor(255,0,0))
        painter.drawLine(0, 0, 0, -int(radius*0.78))
        painter.restore()

        painter.end()