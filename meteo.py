import random
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt, QRectF
from PySide6.QtGui import QPixmap

class MeteoManager:
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget
        self.paused = False  # booléen pause

        self.evenements = {
            "typhon": "images/typhon.png",
            "givre": "images/givre.png",
            "foudre": "images/foudre.png",
            "volcan": "images/volcan.png"
        }

        self.tailles = {
            "typhon": (100, 100),
            "givre": (80, 80),
            "foudre": (80, 120),
            "volcan": (120, 120)
        }

        self.evenements_actifs = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.lancer_evenement)
        self.demarrer_timer_aleatoire()

    def demarrer_timer_aleatoire(self):
        if self.paused:
            return  # ne rien faire si en pause
        interval = random.randint(10_000, 15_000)
        self.timer.start(interval)

    def lancer_evenement(self):
        evenement = random.choice(list(self.evenements.keys()))
        image_path = self.evenements[evenement]

        label = QLabel(self.parent_widget)
        pixmap = QPixmap(image_path)
        width, height = self.tailles[evenement]
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)

        parent_width = self.parent_widget.width()
        parent_height = self.parent_widget.height()
        x = random.randint(0, max(0, parent_width - width))
        y = random.randint(0, max(0, parent_height - height))
        label.move(x, y)
        label.setAttribute(Qt.WA_TransparentForMouseEvents)
        label.show()

        rect = QRectF(x, y, width, height)

        duree = random.randint(10_000, 20_000)

        # Timer suppression avec fonction liée à l'instance
        timer_suppression = QTimer()
        timer_suppression.setSingleShot(True)
        timer_suppression.timeout.connect(lambda lbl=label: self.supprimer_event(lbl))
        timer_suppression.start(duree)

        self.evenements_actifs.append({
            "type": evenement,
            "label": label,
            "rect": rect,
            "timer_suppression": timer_suppression
        })

        self.demarrer_timer_aleatoire()

    def supprimer_event(self, label):
        if self.paused:
            # Si pause, on ne supprime pas l'événement
            return

        # Supprimer l'événement actif et le label
        self.evenements_actifs = [e for e in self.evenements_actifs if e["label"] != label]
        label.deleteLater()

    def set_paused(self, paused: bool):
        self.paused = paused
        if paused:
            self.timer.stop()  # Arrêter la création de nouveaux événements
            # On ne stoppe PAS les timers de suppression pour garder les événements visibles
        else:
            self.demarrer_timer_aleatoire()  # Relancer le timer pour les événements

    def get_evenements_actifs(self):
        return [(e["rect"], e["type"]) for e in self.evenements_actifs]

    def verifier_collisions(self, planes, selected_plane):
        evenements = self.get_evenements_actifs()
        from collision_meteo import CollisionManager
        CollisionManager.check_collision_et_evitement(planes, selected_plane, evenements)
