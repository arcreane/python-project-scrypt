# meteo.py
import random
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt, QRectF, Signal, QObject
from PySide6.QtGui import QPixmap

class MeteoManager(QObject):
    evenements_changed = Signal()  # Signal émis quand la liste des événements change

    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.paused = False

        self.evenements = {
            "typhon": "images/Meteo_typhon.png",
            "givre": "images/Meteo_givre.png",
            "foudre": "images/Meteo_foudre.png",
            "volcan": "images/Meteo_volcan.png"
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
            return  # Ne rien faire si en pause
        interval = random.randint(10_000, 15_000)
        self.timer.start(interval)

    def lancer_evenement(self):
        if self.paused:
            return
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

        self.evenements_changed.emit()
        self.demarrer_timer_aleatoire()

    def supprimer_event(self, label):
        if self.paused:
            # Ne pas supprimer si pause, garder affiché
            return
        self.evenements_actifs = [e for e in self.evenements_actifs if e["label"] != label]
        label.deleteLater()
        self.evenements_changed.emit()

    def set_paused(self, paused: bool):
        self.paused = paused
        if paused:
            self.timer.stop()
            # Ne pas arrêter timers suppression pour que les événements restent visibles
        else:
            self.demarrer_timer_aleatoire()

    def get_evenements_actifs(self):
        return [(e["rect"], e["type"]) for e in self.evenements_actifs]

    def get_conditions(self):
        """
        Fournit une liste simplifiée des événements météo,
        compatible avec CollisionManager.
        """
        conditions = []
        for e in self.evenements_actifs:
            rect = e["rect"]
            cx = rect.x() + rect.width() / 2
            cy = rect.y() + rect.height() / 2
            radius = max(rect.width(), rect.height()) / 2

            class MeteoCond:
                pass

            obj = MeteoCond()
            obj.pos = QPointF(cx, cy)
            obj.radius = radius
            conditions.append(obj)

        return conditions

    def get_message_meteo(self):
        if len(self.evenements_actifs) == 0:
            return "Rien à signaler"
        else:
            return "⚠️ Conditions météorologiques dangereuses détectées !"
