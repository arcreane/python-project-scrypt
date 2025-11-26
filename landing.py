from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt

class LandingView(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)  # on ne force pas le QLabel à étirer n'importe comment
        self.current_pixmap = QPixmap("Images/Piste_attente.png")
        self.overlay_plane = None  # contiendra l'image de l'avion
        self.setPixmap(self.current_pixmap)

        # **Important** : laisse le layout décider de la taille, mais ne force pas le widget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 150)  # taille minimale pour ne pas être écrasé

    def set_selected_plane(self, plane):
        if plane is None:
            self.current_pixmap = QPixmap("Images/Piste_attente.png")
        else:
            self.current_pixmap = QPixmap("Images/Piste_avion.png")
        self.setPixmap(self.current_pixmap)
        self.overlay_plane = None

    def resizeEvent(self, event):
        """Redimensionner l'image pour qu'elle remplisse le QLabel"""
        if self.current_pixmap:
            self.setPixmap(self.current_pixmap.scaled(
                self.width(), self.height(),
                Qt.IgnoreAspectRatio,  # on ignore le ratio pour remplir
                Qt.SmoothTransformation
            ))
        super().resizeEvent(event)

    def show_plane(self, image_path):
        """Affiche un avion en superposition sur la piste."""
        self.overlay_plane = QPixmap(image_path)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.overlay_plane:
            painter = QPainter(self)
            # Taille de l'avion : 25% de la largeur de la piste
            w = self.width() * 0.25
            h = w * (self.overlay_plane.height() / self.overlay_plane.width())
            x = 20
            y = 20

            painter.drawPixmap(
                int(x), int(y),
                int(w), int(h),
                self.overlay_plane
            )
            painter.end()
