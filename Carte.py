# Carte.py
import sys
import random
import math
from PySide6.QtCore import Qt, QTimer, QPointF, Signal
from PySide6.QtGui import QPainter, QColor, QFont, QPolygonF, QPen
from PySide6.QtWidgets import QApplication, QWidget
from Avions import Avions


class MovingPlane:
    """Triangle représentant un avion avec fuel, mouvement et clignotement."""
    def __init__(self, avion, x, y):
        self.avion = avion
        self.pos = QPointF(x, y)

        # Déplacement initial selon cap (0° = haut)
        rad = math.radians(self.avion.cap - 90)
        speed = self.avion.vitesse / 250.0
        self.vx = math.cos(rad) * speed
        self.vy = math.sin(rad) * speed

        self.size = 20
        self.blink = 0

        # Dernier angle valide pour conserver orientation si avion arrêté
        self.last_angle = rad

        # Mettre à jour le cap initial de l'avion
        self.update_avion_cap()

    def move(self, w, h):
        # Déplacement
        self.pos.setX(self.pos.x() + self.vx)
        self.pos.setY(self.pos.y() + self.vy)

        # Rebonds
        bounced = False
        if self.pos.x() < 0:
            self.pos.setX(0)
            self.vx *= -1
            bounced = True
        elif self.pos.x() > w:
            self.pos.setX(w)
            self.vx *= -1
            bounced = True

        if self.pos.y() < 0:
            self.pos.setY(0)
            self.vy *= -1
            bounced = True
        elif self.pos.y() > h:
            self.pos.setY(h)
            self.vy *= -1
            bounced = True

        # si rebond, mettre à jour last_angle pour garder orientation cohérente
        if bounced and (self.vx != 0 or self.vy != 0):
            self.last_angle = math.atan2(self.vy, self.vx)
            self.update_avion_cap()

    def update_fuel(self):
        conso_sec = self.avion.vitesse / 500.0
        conso_tick = conso_sec / 60.0
        self.avion.fuel = max(0, self.avion.fuel - conso_tick)

        if self.avion.fuel == 0:
            self.vx = 0
            self.vy = 0
            self.avion.altitude = 0
            self.update_avion_cap()  # figer le cap si avion arrêté

        self.blink += 1

        # Met à jour le dernier angle si avion en mouvement
        if self.vx != 0 or self.vy != 0:
            self.last_angle = math.atan2(self.vy, self.vx)
            self.update_avion_cap()

    def angle(self):
        # Angle du triangle : mouvement réel si en mouvement, sinon dernier angle
        if self.vx != 0 or self.vy != 0:
            return math.atan2(self.vy, self.vx)
        return self.last_angle

    def get_color(self):
        fuel = self.avion.fuel

        normal_color = (255, 80, 80)
        warning_color = (255, 150, 0)
        critical_color = (255, 255, 255)

        if self.vx == 0 and self.vy == 0:
            if fuel > 20:
                color = normal_color
            elif fuel > 5:
                color = warning_color
            else:
                color = critical_color
            return color

        if fuel > 20:
            color = normal_color
        elif fuel > 5:
            if (self.blink // 30) % 2 == 0:
                color = warning_color
            else:
                color = normal_color
        else:
            if (self.blink // 10) % 2 == 0:
                color = critical_color
            else:
                color = warning_color

        return color

    def update_avion_cap(self):
        """Met à jour avion.cap selon la direction réelle du mouvement."""
        if self.vx != 0 or self.vy != 0:
            self.avion.cap = (math.degrees(math.atan2(self.vy, self.vx)) + 90) % 360



class GameWidget(QWidget):
    """Widget de la carte / zone de jeu."""
    # Signal émis quand l'avion sélectionné change : on envoie l'instance Avions
    avion_selectionne_changed = Signal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Avions - Triangles orientés")
        self.resize(800, 600)

        self.planes = []
        self.selected_plane = None  # MovingPlane sélectionné
        self.add_plane()  # avion initial

        # Timer d’animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

        # Timer d’apparition aléatoire
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_plane)
        self.set_random_spawn_time()

    def set_random_spawn_time(self):
        delay = random.randint(5000, 10000)
        self.spawn_timer.start(delay)

    def random_plane_data(self):
        nom = f"Avion {len(self.planes)+1}"
        altitude = random.randint(1000, 12000)
        vitesse = random.randint(200, 900)
        fuel = random.randint(10, 100)
        cap = random.randint(0, 359)
        return Avions(nom, altitude, vitesse, fuel, cap)

    def add_plane(self):
        x = random.randint(50, max(50, self.width() - 50))
        y = random.randint(50, max(50, self.height() - 50))
        avion = self.random_plane_data()
        self.planes.append(MovingPlane(avion, x, y))

    def spawn_plane(self):
        self.add_plane()
        self.set_random_spawn_time()

    def update_game(self):
        w = self.width()
        h = self.height()
        for p in self.planes:
            p.move(w, h)
            p.update_fuel()
        self.update()

    def draw_triangle(self, painter, plane: MovingPlane):
        angle = plane.angle()
        s = plane.size
        base = s * 0.6

        triangle = [
            QPointF(s, 0),
            QPointF(-s, base),
            QPointF(-s, -base)
        ]

        rotated = []
        for pt in triangle:
            rx = pt.x() * math.cos(angle) - pt.y() * math.sin(angle)
            ry = pt.x() * math.sin(angle) + pt.y() * math.cos(angle)
            rotated.append(QPointF(rx + plane.pos.x(), ry + plane.pos.y()))

        # couleur de remplissage
        color = plane.get_color()
        painter.setBrush(QColor(*color))

        # contour spécial si sélectionné
        if plane is self.selected_plane:
            pen = QPen(QColor(50, 120, 255), 3)  # contour bleu épais
        else:
            pen = QPen(Qt.black, 1)

        painter.setPen(pen)
        painter.drawPolygon(QPolygonF(rotated))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for plane in self.planes:
            self.draw_triangle(painter, plane)
            painter.setPen(Qt.black)
            painter.setFont(QFont("Arial", 10))
            text_y = plane.pos.y() + plane.size + 15
            if text_y > self.height() - 5:
                text_y = plane.pos.y() - plane.size - 5

            painter.drawText(
                plane.pos.x() - 30, text_y, 100, 15,
                Qt.AlignCenter,
                plane.avion.nom
            )

    def mousePressEvent(self, event):
        pos = event.position()
        clicked = False
        for p in self.planes:
            dx = pos.x() - p.pos.x()
            dy = pos.y() - p.pos.y()
            if dx*dx + dy*dy <= (p.size * 1.2)**2:
                self.selected_plane = p
                clicked = True

                # émettre le signal avec l'objet Avions réel
                self.avion_selectionne_changed.emit(p.avion)

                # afficher infos dans la console (cap réel)
                if p.vx != 0 or p.vy != 0:
                    real_cap = (math.degrees(math.atan2(p.vy, p.vx)) + 90) % 360
                else:
                    real_cap = (math.degrees(p.last_angle) + 90) % 360

                print(f"✈️ {p.avion.nom}")
                print(f"  Altitude : {p.avion.altitude} m")
                print(f"  Vitesse  : {p.avion.vitesse} km/h")
                print(f"  Fuel     : {p.avion.fuel:.1f} %")
                print(f"  Cap      : {real_cap:.1f}°")
                print()
                break

        if not clicked:
            # cliquer nulle part désélectionne
            self.selected_plane = None
            self.avion_selectionne_changed.emit(None)

        self.update()

    # ---------- API pour contrôler l'avion sélectionné ----------
    def _update_velocity_from_cap(self, plane: MovingPlane):
        """Recalcule vx/vy à partir de plane.avion.cap et plane.avion.vitesse."""
        if plane is None:
            return
        # normaliser cap
        plane.avion.cap = plane.avion.cap % 360
        # si fuel = 0 -> ne pas redémarrer
        if plane.avion.fuel == 0:
            plane.vx = 0
            plane.vy = 0
            return
        rad = math.radians(plane.avion.cap - 90)
        speed = plane.avion.vitesse / 250.0
        plane.vx = math.cos(rad) * speed
        plane.vy = math.sin(rad) * speed
        # mettre à jour last_angle
        if plane.vx != 0 or plane.vy != 0:
            plane.last_angle = math.atan2(plane.vy, plane.vx)

    def monter_selected(self):
        if self.selected_plane:
            self.selected_plane.avion.monter()
            # altitude modifiée, on peut rafraîchir immédiatement
            self.update()

    def descendre_selected(self):
        if self.selected_plane:
            self.selected_plane.avion.descendre()
            self.update()

    def gauche_selected(self):
        if self.selected_plane:
            self.selected_plane.avion.gauche()
            # mettre à jour la vitesse/orientation graphique
            self._update_velocity_from_cap(self.selected_plane)
            self.update()

    def droite_selected(self):
        if self.selected_plane:
            self.selected_plane.avion.droite()
            self._update_velocity_from_cap(self.selected_plane)
            self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GameWidget()
    w.show()
    sys.exit(app.exec())
