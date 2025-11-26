# landing.py
from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt

class LandingView(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)
        # images de base
        self.pixmap_attente = QPixmap("Images/Piste_attente.png")
        self.pixmap_avion = QPixmap("Images/Piste_avion.png")
        # image d'overlay pour l'avion posé
        self.plane_overlay = QPixmap("Images/avion_attente.png")
        # état interne
        self.current_pixmap = self.pixmap_attente
        self.locked = False
        self.setPixmap(self.current_pixmap)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 150)

        self.ground_plane_active = False
        self.ground_x = 20
        self.ground_y = 20
        self.ground_scale = 0.25  # 🔥 augmenter l'échelle pour un avion plus grand

    def set_selected_plane(self, plane):
        if self.locked:
            return
        if plane is None:
            self.current_pixmap = self.pixmap_attente
        else:
            self.current_pixmap = self.pixmap_avion
        self._apply_current_pixmap()

    def lock_with_plane_overlay(self, overlay_path=None, position="topleft"):
        if overlay_path:
            overlay = QPixmap(overlay_path)
            if not overlay.isNull():
                self.plane_overlay = overlay

        self.locked = True
        base = self.pixmap_avion
        composed = QPixmap(base.size())
        composed.fill(Qt.transparent)
        painter = QPainter(composed)
        painter.drawPixmap(0, 0, base)

        # 🔥 Redimensionnement plus grand
        scale_factor = 0.50
        ow = int(self.plane_overlay.width() * scale_factor)
        oh = int(self.plane_overlay.height() * scale_factor)
        overlay_small = self.plane_overlay.scaled(ow, oh, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        bw, bh = base.width(), base.height()
        margin = max(6, int(min(bw, bh) * 0.03))

        if position == "topleft":
            x = margin
            y = margin
        elif position == "topright":
            x = bw - overlay_small.width() - margin
            y = margin
        elif position == "center":
            x = (bw - overlay_small.width()) // 2
            y = (bh - overlay_small.height()) // 2
        else:
            x = margin
            y = margin

        painter.drawPixmap(x, y, overlay_small)
        painter.end()
        self.current_pixmap = composed
        self._apply_current_pixmap()

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

    def activate_ground_plane(self, overlay_path="Images/avion_attente.png"):
        self.locked = True
        self.plane_overlay = QPixmap(overlay_path)
        self.ground_plane_active = True
        self.ground_x = 20
        self.ground_y = 20
        self.update_ground_plane()

    def update_ground_plane(self):
        if not self.ground_plane_active:
            return

        base = self.pixmap_avion
        composed = QPixmap(base.size())
        composed.fill(Qt.transparent)
        painter = QPainter(composed)
        painter.drawPixmap(0, 0, base)

        # 🔥 utiliser ground_scale augmenté
        overlay_small = self.plane_overlay.scaled(
            int(self.plane_overlay.width() * self.ground_scale),
            int(self.plane_overlay.height() * self.ground_scale),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        painter.drawPixmap(self.ground_x, self.ground_y, overlay_small)
        painter.end()

        self.current_pixmap = composed
        self._apply_current_pixmap()

    def move_ground_plane(self, dx=0, dy=0):
        if not self.ground_plane_active:
            return

        self.ground_x += dx
        self.ground_y += dy

        # limites
        max_x = self.pixmap_avion.width() - int(self.plane_overlay.width() * self.ground_scale)
        max_y = self.pixmap_avion.height() - int(self.plane_overlay.height() * self.ground_scale)

        self.ground_x = max(0, min(self.ground_x, max_x))
        self.ground_y = max(0, min(self.ground_y, max_y))

        self.update_ground_plane()

        # 🔹 Check si l'avion atteint le bas
        if self.ground_y >= max_y:
            self.finish_landing()

    def finish_landing(self):
        self.ground_plane_active = False
        self.locked = False
        self.current_pixmap = self.pixmap_attente
        self._apply_current_pixmap()

        # 🔹 Émettre un signal pour informer MainGameWindow
        if hasattr(self, "landing_finished_callback") and callable(self.landing_finished_callback):
            self.landing_finished_callback()
