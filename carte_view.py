from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPixmap

class CarteView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background = QPixmap("ecran_fond_vue_de_haut.jpg")
        # Exemples d'avions
        self.avions = [
            {"pixmap": QPixmap("avion.png"), "x": 100, "y": 200},
            {"pixmap": QPixmap("avion.png"), "x": 300, "y": 400},
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)
        for avion in self.avions:
            painter.drawPixmap(avion["x"], avion["y"], avion["pixmap"])

    # Pour que tes connexions aux boutons fonctionnent, il faut définir ces méthodes :
    def monter_selected(self):
        print("Monter sélectionné")

    def descendre_selected(self):
        print("Descendre sélectionné")

    def gauche_selected(self):
        print("Gauche sélectionné")

    def droite_selected(self):
        print("Droite sélectionné")
