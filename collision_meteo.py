# collision_meteo_fixed.py
import math
from PySide6.QtCore import QObject, QTimer, QDateTime, QPointF, QUrl
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import QSoundEffect


class CollisionManager(QObject):

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
        self.explosion_sound = QSoundEffect()
        self.explosion_sound.setSource(QUrl.fromLocalFile("explosion.wav"))
        self.explosion_sound.setVolume(0.5)
        self.explosion_pixmap = QPixmap("boum.png")
        self.meteo_malus = -100

    def _tick(self):
        if CollisionManager.paused:
            return

        now = QDateTime.currentMSecsSinceEpoch()
        conditions = self.meteo_manager.get_conditions()

        for plane in self.game_widget.planes:
            if getattr(plane.avion, "fuel", 1) <= 0:
                continue  # avion arrêté

            if self._avoid_until.get(plane, 0) > now:
                continue

            for cond in conditions:
                if self._intersects_plane(cond, plane):

                    if plane is self.game_widget.selected_plane:
                        explosion_label = QLabel(self.game_widget)
                        explosion_label.setPixmap(self.explosion_pixmap)
                        explosion_label.setScaledContents(True)
                        explosion_label.setFixedSize(50, 50)
                        explosion_label.move(int(plane.pos.x()), int(plane.pos.y()))
                        explosion_label.show()
                        explosion_label.raise_()
                        self.explosion_sound.play()

                        QTimer.singleShot(500, explosion_label.deleteLater)

                        if hasattr(self.game_widget, "update_score") and callable(self.game_widget.update_score):
                            new_score = self.game_widget.update_score(self.meteo_malus)

                            # Game Over si score <= 0
                            if new_score is not None and new_score <= 0:
                                if hasattr(self.game_widget, "show_game_over") and callable(
                                        self.game_widget.show_game_over):
                                    self.game_widget.show_game_over()

                        # Appliquer évitement pour continuer le jeu
                        self._apply_avoidance(plane, cond)
                        self._avoid_until[plane] = now + self.avoid_duration_ms
                        break

                    else:
                        self._apply_avoidance(plane, cond)
                        self._avoid_until[plane] = now + self.avoid_duration_ms
                        break

    def _intersects_plane(self, cond, plane):
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

    def _apply_avoidance(self, plane, cond):
        try:
            center = getattr(cond, "pos", QPointF(0, 0))
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
