import random
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap

class MeteoManager:
    def __init__(self, parent_widget):

        self.parent_widget = parent_widget

        # Dictionnaire événements -> icônes
        self.evenements = {
            "typhon": "images/typhon.png",
            "givre": "images/givre.png",
            "foudre": "images/foudre.png"
        }

        # Tailles spécifiques pour chaque icône
        self.tailles = {
            "typhon": (100, 100),
            "givre": (80, 80),
            "foudre": (80, 120)
        }

        # Timer pour lancer les événements aléatoires
        self.timer = QTimer()
        self.timer.timeout.connect(self.lancer_evenement)
        self.demarrer_timer_aleatoire()

    def demarrer_timer_aleatoire(self):
        # Prochain événement entre 5 et 10 secondes
        interval = random.randint(5_000, 10_000)
        self.timer.start(interval)

    def lancer_evenement(self):
        # Choisir un événement aléatoire
        evenement = random.choice(list(self.evenements.keys()))
        image_path = self.evenements[evenement]

        # Créer un QLabel pour afficher l'icône
        label = QLabel(self.parent_widget)
        pixmap = QPixmap(image_path)
        width, height = self.tailles[evenement]
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)

        # Position aléatoire dans le widget_carte
        parent_width = self.parent_widget.width()
        parent_height = self.parent_widget.height()
        x = random.randint(0, max(0, parent_width - 20))
        y = random.randint(0, max(0, parent_height - 20))
        label.move(x, y)
        label.setAttribute(Qt.WA_TransparentForMouseEvents)  # laisser passer les clics
        label.show()

        # Supprimer l'événement après 5 à 10 secondes
        duree = random.randint(5_000, 10_000)
        QTimer.singleShot(duree, label.deleteLater)

        # Relancer le timer pour le prochain événement
        self.demarrer_timer_aleatoire()
