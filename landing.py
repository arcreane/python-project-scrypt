#landing.py
import random
from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt

class LandingView(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)

        # Images de base
        self.pixmap_attente = QPixmap("Images/Piste_attente.png")
        self.pixmap_avion = QPixmap("Images/Piste_avion.png")
        self.plane_overlay = QPixmap("Images/avion_attente.png")

        self.current_pixmap = self.pixmap_attente
        self.locked = False
        self.setPixmap(self.current_pixmap)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 150)

        # État interne
        self.global_paused = False
        self.ground_plane_active = False
        self.ground_x = 20
        self.ground_y = 20
        self.ground_scale = 0.50

        # Cache pour optimiser le redraw
        self._overlay_cached = None
        self._last_position = (-1, -1)

    def set_selected_plane(self, plane):
        if self.locked or self.ground_plane_active:
            return
        self.current_pixmap = self.pixmap_avion if plane else self.pixmap_attente
        self._apply_current_pixmap()

    def lock_with_plane_overlay(self, overlay_path=None, position="topleft"):
        if overlay_path:
            overlay = QPixmap(overlay_path)
            if not overlay.isNull():
                self.plane_overlay = overlay

        self.locked = True
        self._compose_overlay(position)

    def unlock(self):
        self.locked = False
        self.current_pixmap = self.pixmap_attente
        self._apply_current_pixmap()

    def _apply_current_pixmap(self):
        if self.current_pixmap and not self.current_pixmap.isNull():
            self.setPixmap(self.current_pixmap.scaled(
                self.width(), self.height(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            ))
        else:
            self.clear()

    def resizeEvent(self, event):
        self._apply_current_pixmap()
        super().resizeEvent(event)

    # --------------------------
    # Gestion du ground plane
    # --------------------------
    def activate_ground_plane(self, overlay_path=None):
        self.locked = True
        self.ground_plane_active = True

        # Choix aléatoire si overlay_path non fourni
        if overlay_path is None:
            # Liste des images possibles
            images = [
                "Images/Photo_atterrissage_1.png",
                "Images/Photo_atterrissage_2.png",
                "Images/Photo_atterrissage_3.png",
                "Images/Photo_atterrissage_4.png",
                "Images/Photo_atterrissage_5.png",
                "Images/Photo_atterrissage_6.png",
            ]
            overlay_path = random.choice(images)

        self.plane_overlay = QPixmap(overlay_path)
        self.ground_x = 40
        self.ground_y = 40
        self.ground_scale = 0.5
        self._overlay_cached = None
        self._last_position = (-1, -1)
        self.update_ground_plane()


    def update_ground_plane(self):
        if not self.ground_plane_active:
            return

        # Redessiner overlay seulement si la position a changé
        if self._last_position != (self.ground_x, self.ground_y) or self._overlay_cached is None:
            overlay_small = self.plane_overlay.scaled(
                int(self.plane_overlay.width() * self.ground_scale),
                int(self.plane_overlay.height() * self.ground_scale),
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )
            self._overlay_cached = overlay_small
            self._last_position = (self.ground_x, self.ground_y)

        # Composer l'image finale
        composed = QPixmap(self.pixmap_avion)
        painter = QPainter(composed)
        painter.drawPixmap(self.ground_x, self.ground_y, self._overlay_cached)
        painter.end()

        self.current_pixmap = composed
        self._apply_current_pixmap()

    def move_ground_plane(self, dx=0, dy=0):
        if not self.ground_plane_active or self.global_paused:
            return

        self.ground_x += dx
        self.ground_y += dy

        max_x = self.pixmap_avion.width() - int(self.plane_overlay.width() * self.ground_scale)
        max_y = self.pixmap_avion.height() - int(self.plane_overlay.height() * self.ground_scale)

        self.ground_x = max(0, min(self.ground_x, max_x))
        self.ground_y = max(0, min(self.ground_y, max_y))

        self.update_ground_plane()

        if self.ground_y >= max_y:
            self.finish_landing()

    def finish_landing(self):
        self.ground_plane_active = False
        self.locked = False

        # Appel du callback si défini (Crash d’avion)
        if hasattr(self, "landing_crash_callback") and callable(self.landing_crash_callback):
            self.landing_crash_callback()
        else:
            self.current_pixmap = self.pixmap_attente
            self._apply_current_pixmap()
