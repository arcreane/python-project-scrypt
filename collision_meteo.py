import math
from PySide6.QtCore import QRectF

class CollisionManager:
    @staticmethod
    def check_collision_et_evitement(planes, selected_plane, evenements):
        """
        planes : liste de MovingPlane
        selected_plane : l'avion sélectionné ou None
        evenements : liste de tuples (QRectF, type)
        """
        for p in planes:
            # ---------------- Avion sélectionné ----------------
            if p is selected_plane:
                for event_rect, event_type in evenements:
                    plane_rect = QRectF(
                        p.pos.x() - p.size, p.pos.y() - p.size,
                        p.size * 2, p.size * 2
                    )
                    if plane_rect.intersects(event_rect):
                        print(f"Game Over ! Collision avec {event_type}")
                        # ⚡ Bloquer l'avion immédiatement
                        p.vx = 0
                        p.vy = 0
                        p.avion.vitesse = 0
                        # ⚡ Optionnel : tu peux ajouter un flag pour game over
                        break
                continue  # ne teste pas la fuite pour l'avion sélectionné

            # ---------------- Avions non sélectionnés → fuite ----------------
            plane_rect = QRectF(
                p.pos.x() - p.size, p.pos.y() - p.size,
                p.size * 2, p.size * 2
            )

            for event_rect, event_type in evenements:
                if plane_rect.intersects(event_rect):
                    # Centre de l'événement
                    center_evt = event_rect.center()
                    dx = p.pos.x() - center_evt.x()
                    dy = p.pos.y() - center_evt.y()

                    # ⚡ Évite division par zéro si l'avion est exactement au centre
                    if dx == 0 and dy == 0:
                        dx, dy = 1, 0

                    # Calcul de l'angle de fuite
                    angle = math.atan2(dy, dx)
                    p.avion.cap = (math.degrees(angle) + 90) % 360

                    # Mettre à jour vx et vy selon le nouveau cap
                    p.update_velocity_from_cap()
                    break  # une seule fuite par événement détecté
