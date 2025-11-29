# meteo.py
import random
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt, QRectF, Signal, QObject, QPointF
from PySide6.QtGui import QPixmap


# Classe : Gestion des événements météo
class MeteoManager(QObject):
    """
    Gère les événements météo dans le jeu :
    - Typhon, givre, foudre, volcan
    - Apparition aléatoire et suppression automatique
    - Signal émis à chaque changement
    """

    evenements_changed = Signal()  # Signal déclenché quand la liste change

    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.paused = False

        # Définition des types d’événements et chemins d’images
        self.evenements = {
            "typhon": "images/Meteo_typhon.png",
            "givre": "images/Meteo_givre.png",
            "foudre": "images/Meteo_foudre.png",
            "volcan": "images/Meteo_volcan.png"
        }

        # Tailles spécifiques pour chaque type
        self.tailles = {
            "typhon": (100, 100),
            "givre": (80, 80),
            "foudre": (80, 120),
            "volcan": (120, 120)
        }

        self.evenements_actifs = []

        # Timer principal pour lancer les événements aléatoires
        self.timer = QTimer()
        self.timer.timeout.connect(self.lancer_evenement)
        self.demarrer_timer_aleatoire()

    # Gestion du timer principal
    def demarrer_timer_aleatoire(self):
        """Démarre un timer aléatoire pour l’apparition d’un événement météo."""
        if self.paused:
            return
        interval = random.randint(10_000, 15_000)
        self.timer.start(interval)

    # Création et suppression d’événements
    def lancer_evenement(self):
        """Crée un événement météo aléatoire et le positionne sur le widget."""
        if self.paused:
            return

        # Choix aléatoire du type
        evenement = random.choice(list(self.evenements.keys()))
        image_path = self.evenements[evenement]

        # Création du QLabel associé
        label = QLabel(self.parent_widget)
        pixmap = QPixmap(image_path)
        width, height = self.tailles[evenement]
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)

        # Position aléatoire
        parent_width = self.parent_widget.width()
        parent_height = self.parent_widget.height()
        x = random.randint(0, max(0, parent_width - width))
        y = random.randint(0, max(0, parent_height - height))
        label.move(x, y)
        label.setAttribute(Qt.WA_TransparentForMouseEvents)
        label.show()

        rect = QRectF(x, y, width, height)

        # Timer de suppression automatique
        duree = random.randint(10_000, 20_000)
        timer_suppression = QTimer()
        timer_suppression.setSingleShot(True)
        timer_suppression.timeout.connect(lambda lbl=label: self.supprimer_event(lbl))
        timer_suppression.start(duree)

        # Sauvegarde dans la liste des événements actifs
        self.evenements_actifs.append({
            "type": evenement,
            "label": label,
            "rect": rect,
            "timer_suppression": timer_suppression
        })

        # Signal de mise à jour
        self.evenements_changed.emit()
        self.demarrer_timer_aleatoire()

    def supprimer_event(self, label):
        """Supprime un événement météo donné."""
        if self.paused:
            return  # Conserver l'affichage si en pause
        self.evenements_actifs = [e for e in self.evenements_actifs if e["label"] != label]
        label.deleteLater()
        self.evenements_changed.emit()

    # Pause / reprise
    def set_paused(self, paused: bool):
        """Met en pause ou reprend l'apparition des événements météo."""
        self.paused = paused
        if paused:
            self.timer.stop()
        else:
            self.demarrer_timer_aleatoire()

    # Accesseurs
    def get_evenements_actifs(self):
        """Retourne la liste simplifiée des événements actifs [(rect, type), ...]."""
        return [(e["rect"], e["type"]) for e in self.evenements_actifs]

    def get_conditions(self):
        """
        Retourne la liste des événements sous forme compatible
        avec CollisionManager (position centrale et rayon).
        """
        conditions = []
        for e in self.evenements_actifs:
            rect = e["rect"]
            cx = rect.x() + rect.width() / 2
            cy = rect.y() + rect.height() / 2
            radius = max(rect.width(), rect.height()) / 2

            # Objet simplifié pour CollisionManager
            class MeteoCond:
                pass

            obj = MeteoCond()
            obj.pos = QPointF(cx, cy)
            obj.radius = radius
            conditions.append(obj)

        return conditions
