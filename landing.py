# landing.py
from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt, QRect

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
        self.locked = False   # quand True -> on garde piste avion verrouillée
        self.setPixmap(self.current_pixmap)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 150)

    def set_selected_plane(self, plane):
        """
        Comportement normal :
         - si plane is not None -> afficher piste avion
         - si plane is None -> afficher piste attente
        MAIS ne change rien si locked == True (Atterri verrouillé)
        """
        if self.locked:
            # verrou activé par un atterrissage : ne rien changer
            return

        if plane is None:
            self.current_pixmap = self.pixmap_attente
        else:
            self.current_pixmap = self.pixmap_avion

        # appliquer
        self._apply_current_pixmap()

    def lock_with_plane_overlay(self, overlay_path=None, position="topleft"):
        """
        Verrouille la piste en mode 'avion' et place l'overlay (avion) réduit à 25% de sa taille.
        """
        # Charger overlay personnalisé si fourni
        if overlay_path:
            overlay = QPixmap(overlay_path)
            if not overlay.isNull():
                self.plane_overlay = overlay

        self.locked = True

        # Base = piste avion
        base = self.pixmap_avion

        # Créer composition
        composed = QPixmap(base.size())
        composed.fill(Qt.transparent)
        painter = QPainter(composed)
        painter.drawPixmap(0, 0, base)

        # ---- 🔥 REDIMENSIONNEMENT DE L’OVERLAY ----
        scale_factor = 0.50  # 25% de la taille originale (tu peux mettre 0.15, 0.20 etc.)
        ow = int(self.plane_overlay.width() * scale_factor)
        oh = int(self.plane_overlay.height() * scale_factor)
        overlay_small = self.plane_overlay.scaled(ow, oh, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # --------------------------------------------------

        bw, bh = base.width(), base.height()
        margin = max(6, int(min(bw, bh) * 0.03))

        # Position topleft
        if position == "topleft":
            x = margin
            y = margin
        elif position == "topright":
            x = bw - overlay_small.width() - margin
            y = margin
        elif position == "center":
            x = (bw - overlay_small.width()) // 2
            y = (bh - overlay_small.height()) // 2
        else:  # fallback
            x = margin
            y = margin

        # Dessiner l'overlay réduit
        painter.drawPixmap(x, y, overlay_small)
        painter.end()

        self.current_pixmap = composed
        self._apply_current_pixmap()

    def unlock(self):
        """Déverrouille la piste (retour au comportement normal)."""
        self.locked = False
        self.current_pixmap = self.pixmap_attente
        self._apply_current_pixmap()

    def _apply_current_pixmap(self):
        """Appliquer current_pixmap à QLabel (et redimensionner proprement)."""
        if self.current_pixmap and not self.current_pixmap.isNull():
            self.setPixmap(self.current_pixmap.scaled(
                self.width(), self.height(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            ))
        else:
            self.clear()

    def resizeEvent(self, event):
        """Redimensionner à chaque resize."""
        self._apply_current_pixmap()
        super().resizeEvent(event)
