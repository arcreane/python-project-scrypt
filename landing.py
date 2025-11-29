# landing.py
import random
from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QSoundEffect


# Classe : Vue d'atterrissage
class LandingView(QLabel):
    """
    Widget représentant la piste et l'avion en attente ou en atterrissage.
    Gère l'affichage, la composition des overlays et la vérification de la zone d'atterrissage.
    """

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 150)

        # Images de base
        self.pixmap_attente = QPixmap("Images/Piste_attente.png")
        self.pixmap_avion = QPixmap("Images/Piste_avion.png")
        self.plane_overlay = QPixmap("Images/avion_attente.png")
        self.current_pixmap = self.pixmap_attente

        # État interne
        self.locked = False
        self.global_paused = False
        self.ground_plane_active = False
        self.ground_x = 20
        self.ground_y = 20
        self.ground_scale = 0.50
        self._overlay_cached = None
        self._last_position = (-1, -1)

        # Sons
        self.son_plouf = QSoundEffect()
        self.son_plouf.setSource(QUrl.fromLocalFile("Musiques/plouf.wav"))
        self.son_plouf.setVolume(0.9)

        # Appliquer l'image initiale
        self._apply_current_pixmap()

    # Sélection et verrouillage
    def set_selected_plane(self, plane):
        """Met à jour l'image selon qu'un avion est sélectionné."""
        if self.locked or self.ground_plane_active:
            return
        self.current_pixmap = self.pixmap_avion if plane else self.pixmap_attente
        self._apply_current_pixmap()

    def lock_with_plane_overlay(self, overlay_path=None, position="topleft"):
        """Verrouille la vue et applique un overlay."""
        if overlay_path:
            overlay = QPixmap(overlay_path)
            if not overlay.isNull():
                self.plane_overlay = overlay

        self.locked = True
        self._compose_overlay(position)

    def unlock(self):
        """Déverrouille la vue et remet la piste en attente."""
        self.locked = False
        self.current_pixmap = self.pixmap_attente
        self._apply_current_pixmap()

    # Gestion de l'image et redimensionnement
    def _apply_current_pixmap(self):
        """Applique l'image actuelle en redimensionnant au widget."""
        if self.current_pixmap and not self.current_pixmap.isNull():
            self.setPixmap(self.current_pixmap.scaled(
                self.width(), self.height(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            ))
        else:
            self.clear()

    def resizeEvent(self, event):
        """Réapplique le pixmap lors du redimensionnement."""
        self._apply_current_pixmap()
        super().resizeEvent(event)

    # Activation et gestion de l'avion au sol
    def activate_ground_plane(self, overlay_path=None):
        """Active l'avion sur la piste avec overlay."""
        self.locked = True
        self.ground_plane_active = True

        # Choix aléatoire si overlay_path non fourni
        if overlay_path is None:
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
        """Redessine l'avion au sol avec overlay si actif."""
        if not self.ground_plane_active:
            return

        if self._last_position != (self.ground_x, self.ground_y) or self._overlay_cached is None:
            overlay_small = self.plane_overlay.scaled(
                int(self.plane_overlay.width() * self.ground_scale),
                int(self.plane_overlay.height() * self.ground_scale),
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )
            self._overlay_cached = overlay_small
            self._last_position = (self.ground_x, self.ground_y)

        composed = QPixmap(self.pixmap_avion)
        painter = QPainter(composed)
        painter.drawPixmap(self.ground_x, self.ground_y, self._overlay_cached)
        painter.end()

        self.current_pixmap = composed
        self._apply_current_pixmap()

    def move_ground_plane(self, dx=0, dy=0):
        """Déplace l'avion sur la piste et vérifie l'atterrissage."""
        if not self.ground_plane_active or self.global_paused:
            return

        # Déplacement
        self.ground_x += dx
        self.ground_y += dy

        max_x = self.pixmap_avion.width() - int(self.plane_overlay.width() * self.ground_scale)
        max_y = self.pixmap_avion.height() - int(self.plane_overlay.height() * self.ground_scale)

        self.ground_x = max(0, min(self.ground_x, max_x))
        self.ground_y = max(0, min(self.ground_y, max_y))

        self.update_ground_plane()
        self._check_landing_zone()

    # Vérification de la zone d'atterrissage
    def _check_landing_zone(self):
        """Vérifie si l'avion est sur la piste ou en dehors."""
        overlay_height = int(self.plane_overlay.height() * self.ground_scale)
        overlay_width = int(self.plane_overlay.width() * self.ground_scale)

        # Zone piste
        piste_top = int(self.pixmap_avion.height() * 0.58)
        piste_bottom = int(self.pixmap_avion.height() * 0.79)
        piste_left_bottom = int(self.pixmap_avion.width() * 0.235)
        piste_right_bottom = int(self.pixmap_avion.width() * 0.06)

        if (piste_top <= self.ground_y <= piste_bottom - overlay_height and
                piste_left_bottom <= self.ground_x <= self.pixmap_avion.width() - piste_right_bottom - overlay_width):
            self.finish_landing(success=True)
            return

        # Zone hors limite → crash / game over
        landing_limit_y = self.pixmap_avion.height() * 0.8
        if self.ground_y + overlay_height > landing_limit_y:
            if hasattr(self, "son_plouf") and self.son_plouf:
                self.son_plouf.play()
            if hasattr(self, "landing_malus_callback") and callable(self.landing_malus_callback):
                self.landing_malus_callback(-200)
            if hasattr(self, "landing_game_over_callback") and callable(self.landing_game_over_callback):
                self.landing_game_over_callback()
            self.finish_landing(success=False)

    # Fin d'atterrissage
    def finish_landing(self, success=False):
        """Termine la séquence d'atterrissage."""
        self.ground_plane_active = False
        self.locked = False

        if success:
            if hasattr(self, "landing_finished_callback") and callable(self.landing_finished_callback):
                self.landing_finished_callback()
            self.current_pixmap = self.pixmap_attente
            self._apply_current_pixmap()
            return

        # Crash
        if hasattr(self, "landing_crash_callback") and callable(self.landing_crash_callback):
            self.landing_crash_callback()
        else:
            self.current_pixmap = self.pixmap_attente
            self._apply_current_pixmap()
