import random
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt, QRectF
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

        # Liste des événements actifs
        self.evenements_actifs = []

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
        x = random.randint(0, max(0, parent_width - width))
        y = random.randint(0, max(0, parent_height - height))
        label.move(x, y)
        label.setAttribute(Qt.WA_TransparentForMouseEvents)  # laisser passer les clics
        label.show()

        # Ajouter à la liste des événements actifs
        rect = QRectF(x, y, width, height)
        self.evenements_actifs.append({"type": evenement, "label": label, "rect": rect})

        # Supprimer après 5 à 10 secondes
        duree = random.randint(5_000, 10_000)

        def supprimer_event():
            # Retirer l'événement actif et supprimer le label
            self.evenements_actifs = [
                e for e in self.evenements_actifs if e["label"] != label
            ]
            label.deleteLater()

        QTimer.singleShot(duree, supprimer_event)

        # Relancer le timer pour le prochain événement
        self.demarrer_timer_aleatoire()

    # ---------- Méthode pour la carte / avion ----------
    def get_evenements_actifs(self):
        """Renvoie une liste de tuples (rect, type) pour collision/évitement"""
        return [(e["rect"], e["type"]) for e in self.evenements_actifs]
