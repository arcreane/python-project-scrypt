# collision_meteo.py
import math
from PySide6.QtCore import QObject, QTimer, QDateTime, QPointF


# Classe : Gestion des collisions et évitements météo
class CollisionManager(QObject):
    """
    Vérifie périodiquement les collisions entre les avions
    et les événements météo, et applique une manœuvre d'évitement.
    """
    paused = False  # Classe partagée pour pause globale

    def __init__(self, game_widget, meteo_manager, interval_ms=60, avoid_duration_ms=900):
        """
        Args:
            game_widget: Instance de GameWidget contenant la liste des avions.
            meteo_manager: Instance de MeteoManager fournissant les événements météo.
            interval_ms: Intervalle de vérification des collisions en millisecondes.
            avoid_duration_ms: Durée pendant laquelle un avion évite un événement météo (ms).
        """
        super().__init__(game_widget)
        self.game_widget = game_widget
        self.meteo_manager = meteo_manager
        self.avoid_duration_ms = avoid_duration_ms

        # Dictionnaire : avion -> timestamp fin évitement
        self._avoid_until = {}

        # Timer principal
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(interval_ms)

    # Tick principal : vérifie les collisions
    def _tick(self):
        if CollisionManager.paused:
            return

        now = QDateTime.currentMSecsSinceEpoch()
        conditions = self.meteo_manager.get_conditions()

        for plane in self.game_widget.planes:
            # Skip si avion à l'arrêt
            if getattr(plane.avion, "fuel", 1) <= 0:
                continue

            # Skip si avion en évitement
            if self._avoid_until.get(plane, 0) > now:
                continue

            # Vérification des collisions avec chaque événement météo
            for cond in conditions:
                if self._intersects_plane(cond, plane):

                    # 1) Cas spécial : avion sélectionné → destruction immédiate
                    if plane is self.game_widget.selected_plane:
                        print("⚠ Avion sélectionné détruit par la météo")
                        self.game_widget.remove_plane(plane)
                        break  # Ne plus traiter cet avion

                    # 2) Autres avions → évitement normal
                    self._apply_avoidance(plane, cond)
                    self._avoid_until[plane] = now + self.avoid_duration_ms
                    break

    # Détection collision avion ↔ événement météo
    def _intersects_plane(self, cond, plane):
        """
        Retourne True si l'avion intersecte l'événement météo.

        Args:
            cond: Objet météo avec attributs `pos` et `radius`.
            plane: Instance de MovingPlane.
        """
        try:
            center = getattr(cond, "pos", QPointF(0, 0))
            radius = getattr(cond, "radius", 40.0)
            dx = plane.pos.x() - center.x()
            dy = plane.pos.y() - center.y()
            dist2 = dx * dx + dy * dy
            threshold = (radius + getattr(plane, "size", 20)) ** 2
            return dist2 <= threshold
        except Exception:
            return False

    # Application manœuvre d'évitement
    def _apply_avoidance(self, plane, cond):
        """
        Modifie la direction de l'avion pour éviter l'événement météo.

        Args:
            plane: Instance de MovingPlane.
            cond: Objet météo avec attribut `pos`.
        """
        try:
            center = getattr(cond, "pos", QPointF(0, 0))
            vx = plane.pos.x() - center.x()
            vy = plane.pos.y() - center.y()

            # Cas particulier : avion exactement sur le centre
            if vx == 0 and vy == 0:
                vx, vy = 1.0, 0.0

            # Calcul nouvel angle (cap)
            angle_rad = math.atan2(vy, vx)
            new_cap = (math.degrees(angle_rad) + 90) % 360
            plane.avion.cap = new_cap
            plane.update_velocity_from_cap()
        except Exception:
            pass
