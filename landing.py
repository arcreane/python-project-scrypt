from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class LandingView(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)  # on ne force pas le QLabel à étirer n'importe comment
        self.current_pixmap = QPixmap("Images/zone_attente_atterrissage.png")
        self.setPixmap(self.current_pixmap)

        # **Important** : laisse le layout décider de la taille, mais ne force pas le widget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 150)  # taille minimale pour ne pas être écrasé

    def set_selected_plane(self, plane):
        if plane is None:
            self.current_pixmap = QPixmap("Images/zone_attente_atterrissage.png")
        else:
            self.current_pixmap = QPixmap("Images/zone_atterrissage_avion.png")
        self.setPixmap(self.current_pixmap)

    def resizeEvent(self, event):
        """Redimensionner l'image pour qu'elle remplisse le QLabel"""
        if self.current_pixmap:
            self.setPixmap(self.current_pixmap.scaled(
                self.width(), self.height(),
                Qt.IgnoreAspectRatio,  # on ignore le ratio pour remplir
                Qt.SmoothTransformation
            ))
        super().resizeEvent(event)