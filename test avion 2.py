import sys
import random
import math
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QFont, QPolygonF
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

    def move(self, w, h):
        # Déplacement
        self.pos.setX(self.pos.x() + self.vx)
        self.pos.setY(self.pos.y() + self.vy)

        # Rebonds
        if self.pos.x() < 0 or self.pos.x() > w:
            self.vx *= -1
        if self.pos.y() < 0 or self.pos.y() > h:
            self.vy *= -1

    def update_fuel(self):
        conso_sec = self.avion.vitesse / 500.0
        conso_tick = conso_sec / 60.0
        self.avion.fuel = max(0, self.avion.fuel - conso_tick)

        if self.avion.fuel == 0:
            self.vx = 0
            self.vy = 0

        self.blink += 1

        # Met à jour le dernier angle si avion en mouvement
        if self.vx != 0 or self.vy != 0:
            self.last_angle = math.atan2(self.vy, self.vx)

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


class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Avions - Triangles orientés")
        self.resize(800, 600)

        self.planes = []
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
        x = random.randint(50, 750)
        y = random.randint(50, 550)
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

        color = plane.get_color()
        painter.setBrush(QColor(*color))
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
        for p in self.planes:
            dx = pos.x() - p.pos.x()
            dy = pos.y() - p.pos.y()
            if dx*dx + dy*dy <= (p.size * 1.2)**2:
                av = p.avion

                # Calcul du cap réel selon vecteur déplacement
                if p.vx != 0 or p.vy != 0:
                    real_cap = (math.degrees(math.atan2(p.vy, p.vx)) + 90) % 360
                else:
                    # si avion arrêté, garder le dernier angle
                    real_cap = (math.degrees(p.last_angle) + 90) % 360

                print(f"✈️ {av.nom}")
                print(f"  Altitude : {av.altitude} m")
                print(f"  Vitesse  : {av.vitesse} km/h")
                print(f"  Fuel     : {av.fuel:.1f} %")
                print(f"  Cap      : {real_cap:.1f}°")
                print()
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GameWidget()
    w.show()
    sys.exit(app.exec())
