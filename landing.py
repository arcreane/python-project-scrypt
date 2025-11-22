from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class LandingView(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)  # on ne force pas le QLabel à étirer n'importe comment
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
        self.update_pixmap()

    def resizeEvent(self, event):
        self.update_pixmap()
        super().resizeEvent(event)

    def update_pixmap(self):
        if self.current_pixmap:
            # Redimensionne l'image pour qu'elle tienne dans le QLabel, en gardant le ratio
            scaled = self.current_pixmap.scaled(
                self.width(), self.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled)
