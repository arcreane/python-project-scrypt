# collision_meteo.py
import math
from PySide6.QtCore import QObject, QTimer, QDateTime, QPointF

class CollisionManager(QObject):
    """
    Vérifie périodiquement les collisions entre les avions
    et les événements météo, et applique une manœuvre d'évitement.
    """
    paused = False

    def __init__(self, game_widget, meteo_manager, interval_ms=60, avoid_duration_ms=900):
        super().__init__(game_widget)
        self.game_widget = game_widget
        self.meteo_manager = meteo_manager
        self.avoid_duration_ms = avoid_duration_ms
        self._avoid_until = {}  # plane -> timestamp fin d'évitement

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(interval_ms)

    def _tick(self):
        if CollisionManager.paused:
            return

        now = QDateTime.currentMSecsSinceEpoch()
        conditions = self.meteo_manager.get_conditions()

        for plane in self.game_widget.planes:
            if getattr(plane.avion, "fuel", 1) <= 0:
                continue  # avion arrêté

            # S'il est en évitement : ne rien faire
            if self._avoid_until.get(plane, 0) > now:
                continue

            for cond in conditions:
                if self._intersects_plane(cond, plane):

                    # 🔥 1) CAS SPÉCIAL : avion sélectionné → destruction immédiate
                    if plane is self.game_widget.selected_plane:
                        print("⚠ Avion sélectionné détruit par la météo")
                        self.game_widget.remove_plane(plane)
                        # IMPORTANT : ne plus traiter cet avion
                        break

                    # 🔥 2) Autres avions → évitement normal
                    self._apply_avoidance(plane, cond)
                    self._avoid_until[plane] = now + self.avoid_duration_ms
                    break

    def _intersects_plane(self, cond, plane):
        try:
            center = getattr(cond, "pos", QPointF(0, 0))
            radius = getattr(cond, "radius", 40.0)
            dx = plane.pos.x() - center.x()
            dy = plane.pos.y() - center.y()
            dist2 = dx*dx + dy*dy
            threshold = (radius + getattr(plane, "size", 20))**2
            return dist2 <= threshold
        except Exception:
            return False

    def _apply_avoidance(self, plane, cond):
        try:
            center = getattr(cond, "pos", QPointF(0,0))
            vx = plane.pos.x() - center.x()
            vy = plane.pos.y() - center.y()
            if vx == 0 and vy == 0:
                vx, vy = 1.0, 0.0

            angle_rad = math.atan2(vy, vx)
            new_cap = (math.degrees(angle_rad) + 90) % 360
            plane.avion.cap = new_cap
            plane.update_velocity_from_cap()
        except Exception:
            pass

