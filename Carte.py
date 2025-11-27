import random
import math
from PySide6.QtCore import Qt, QTimer, QPointF, Signal
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QImage, QTransform
from PySide6.QtWidgets import QWidget
from Avions import Avions
from collision_meteo import CollisionManager

# Classe : Avion en mouvement
class MovingPlane:
    def __init__(self, avion, x, y):
        self.avion = avion
        self.pos = QPointF(x, y)

        # Calcul initial de la vitesse selon le cap
        rad = math.radians(self.avion.cap - 90)
        speed = self.avion.vitesse / 250.0
        self.vx = math.cos(rad) * speed
        self.vy = math.sin(rad) * speed

        # Icône
        self.size = 20
        self.icon = QPixmap("Images/Avion.png")
        if self.icon.isNull():
            print("ERREUR : icône avion introuvable")
        else:
            self.icon = self.icon.scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.size = 45

        self.blink = 0
        self.last_angle = rad
        self.update_avion_cap()

    # Mouvement & Fuel
    def move(self, w, h):
        """Déplace l’avion et rebondit sur les bords"""
        self.pos.setX(self.pos.x() + self.vx)
        self.pos.setY(self.pos.y() + self.vy)
        bounced = False

        if self.pos.x() < 0: self.pos.setX(0); self.vx *= -1; bounced = True
        elif self.pos.x() > w: self.pos.setX(w); self.vx *= -1; bounced = True
        if self.pos.y() < 0: self.pos.setY(0); self.vy *= -1; bounced = True
        elif self.pos.y() > h: self.pos.setY(h); self.vy *= -1; bounced = True

        if bounced and (self.vx != 0 or self.vy != 0):
            self.last_angle = math.atan2(self.vy, self.vx)
            self.update_avion_cap()

    def update_fuel(self):
        """Consommation de carburant et arrêt si fuel = 0"""
        conso_sec = self.avion.vitesse / 500.0
        conso_tick = conso_sec / 60.0
        self.avion.fuel = max(0, self.avion.fuel - conso_tick)

        if self.avion.fuel == 0:
            self.vx = self.vy = 0
            self.avion.altitude = 0
            self.avion.vitesse = 0
            self.update_avion_cap()

        self.blink += 1
        if self.vx != 0 or self.vy != 0:
            self.last_angle = math.atan2(self.vy, self.vx)
            self.update_avion_cap()

    # Angles & direction
    def angle(self):
        if self.vx != 0 or self.vy != 0:
            return math.atan2(self.vy, self.vx)
        return self.last_angle

    def update_avion_cap(self):
        if self.vx != 0 or self.vy != 0:
            self.avion.cap = (math.degrees(math.atan2(self.vy, self.vx)) + 90) % 360

    def update_velocity_from_cap(self):
        rad = math.radians(self.avion.cap - 90)
        speed = self.avion.vitesse / 250.0
        self.vx = math.cos(rad) * speed
        self.vy = math.sin(rad) * speed
        if self.vx != 0 or self.vy != 0:
            self.last_angle = math.atan2(self.vy, self.vx)

    # Couleur et état
    def get_color(self):
        """Retourne la couleur selon le fuel et blink"""
        fuel = self.avion.fuel
        normal_color = (50, 120, 255)
        warning_color = (255, 0, 0)
        critical_color = (0, 0, 0)

        if self.vx == 0 and self.vy == 0:
            if fuel > 20: return normal_color
            elif fuel > 5: return warning_color
            else: return critical_color

        if fuel > 20: color = normal_color
        elif fuel > 5: color = warning_color if (self.blink // 30) % 2 == 0 else normal_color
        else: color = critical_color if (self.blink // 10) % 2 == 0 else warning_color

        return color

    def is_blinking(self):
        return self.avion.fuel <= 20

    def is_in_urgence(self):
        return self.is_blinking() or self.avion.fuel <= 5

    def is_in_attente(self):
        return not self.is_blinking() and self.avion.fuel > 5

from meteo import MeteoManager

# Classe : Widget de jeu
class GameWidget(QWidget):
    avion_selectionne_changed = Signal(object)
    avion_updated = Signal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Avions orientés")
        self.resize(800, 600)

        # Variables principales
        self.background = QPixmap("Images/Fond_carte.png")
        self.planes = []
        self.selected_plane = None
        self.stop_timers = {}
        self.mode_highlight = None

        # Ajouter un avion initial
        self.add_plane()
        self.meteo_manager = MeteoManager(self)

        self.collision_manager = CollisionManager(self, self.meteo_manager)

        # Timer de mise à jour
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_plane)
        self.set_random_spawn_time()

    # Gestion pause & spawn
    def set_paused(self, paused: bool):
        if paused:
            self.timer.stop()
            self.spawn_timer.stop()
        else:
            self.timer.start()
            self.set_random_spawn_time()

    def set_random_spawn_time(self):
        self.spawn_timer.start(random.randint(5000, 10000))

    def random_plane_data(self):
        altitude = random.randint(1000, 12000)
        vitesse = random.randint(200, 900)
        fuel = random.randint(10, 100)
        cap = random.randint(0, 359)
        return Avions(None, altitude, vitesse, fuel, cap)

    def add_plane(self):
        x = random.randint(50, max(50, self.width() - 50))
        y = random.randint(50, max(50, self.height() - 50))
        avion = self.random_plane_data()
        plane = MovingPlane(avion, x, y)
        self.planes.append(plane)
        self.avion_updated.emit(plane)

    def spawn_plane(self):
        self.add_plane()
        self.set_random_spawn_time()

    # Mise à jour & suppression
    def update_game(self):
        w, h = self.width(), self.height()
        for p in self.planes[:]:
            prev_vx, prev_vy = p.vx, p.vy
            p.move(w, h)
            p.update_fuel()
            self.avion_updated.emit(p)
            # Timer pour enlever les avions arrêtés
            if (prev_vx != 0 or prev_vy != 0) and p.vx == 0 and p.vy == 0:
                if p not in self.stop_timers:
                    timer = QTimer(self)
                    timer.setSingleShot(True)
                    timer.timeout.connect(lambda pl=p: self.remove_plane(pl))
                    timer.start(5000)
                    self.stop_timers[p] = timer
        self.update()

    def remove_plane(self, plane):
        if plane in self.planes: self.planes.remove(plane)
        if plane in self.stop_timers: self.stop_timers.pop(plane)
        self.avion_updated.emit(plane)

    # Dessin
    def draw_plane_icon(self, painter, plane: MovingPlane):
        angle_deg = math.degrees(plane.angle()) + 90
        icon = plane.icon
        if icon.isNull(): return

        transform = QTransform()
        transform.rotate(angle_deg)
        rotated = icon.transformed(transform, Qt.SmoothTransformation)

        r, g, b = plane.get_color()
        color = QColor(r, g, b)

        # Gestion surbrillance
        if self.mode_highlight and plane is not self.selected_plane:
            if self.mode_highlight == "urgence" and plane.is_in_attente():
                color.setAlpha(100)
            elif self.mode_highlight == "attente" and plane.is_in_urgence():
                color.setAlpha(100)

        # Teinte
        tinted = QImage(rotated.size(), QImage.Format_ARGB32)
        tinted.fill(Qt.transparent)
        pt = QPainter(tinted)
        pt.setCompositionMode(QPainter.CompositionMode_Source)
        pt.drawPixmap(0, 0, rotated)
        pt.setCompositionMode(QPainter.CompositionMode_SourceIn)
        pt.fillRect(tinted.rect(), color)
        pt.end()

        # Dessin final
        x = plane.pos.x() - tinted.width() / 2
        y = plane.pos.y() - tinted.height() / 2
        painter.drawImage(x, y, tinted)

        # Cercle autour du plan sélectionné
        if plane is self.selected_plane:
            painter.setPen(QPen(QColor(50, 120, 255), 3))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(plane.pos, plane.size, plane.size)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background.isNull():
            scaled = self.background.scaled(self.rect().size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled)
        painter.setRenderHint(QPainter.Antialiasing)
        for plane in self.planes:
            self.draw_plane_icon(painter, plane)

    # Sélection via souris
    def mousePressEvent(self, event):
        pos = event.position()
        clicked = False
        for p in self.planes:
            dx, dy = pos.x() - p.pos.x(), pos.y() - p.pos.y()
            if dx * dx + dy * dy <= (p.size * 1.2) ** 2:
                self.selected_plane = p
                clicked = True
                self.avion_selectionne_changed.emit(p.avion)
                break
        if not clicked:
            self.selected_plane = None
            self.avion_selectionne_changed.emit(None)
        self.update()

    # Contrôles
    def monter_selected(self): self._apply_to_selected("monter")
    def descendre_selected(self): self._apply_to_selected("descendre")
    def gauche_selected(self): self._apply_to_selected("gauche", True)
    def droite_selected(self): self._apply_to_selected("droite", True)
    def accelerer_selected(self): self._apply_to_selected("accelerer", True)
    def ralentir_selected(self): self._apply_to_selected("ralentir", True)

    def urgence_selected(self):
        self.mode_highlight = None if self.mode_highlight == "urgence" else "urgence"
        self.update()

    def attente_selected(self):
        self.mode_highlight = None if self.mode_highlight == "attente" else "attente"
        self.update()

    def reset_highlight(self):
        self.mode_highlight = None
        self.update()

    def atterrir_selected(self):
        """Retire l’avion sélectionné de la carte et le renvoie."""
        if self.selected_plane:
            plane = self.selected_plane
            self.selected_plane = None
            self.planes.remove(plane)
            self.avion_selectionne_changed.emit(None)
            return plane
        return None

    # Méthodes internes
    def _apply_to_selected(self, action, update_velocity=False):
        """Applique une action à l’avion sélectionné"""
        if self.selected_plane:
            getattr(self.selected_plane.avion, action)()
            if update_velocity: self._update_velocity_from_cap(self.selected_plane)
            self.avion_updated.emit(self.selected_plane)
            self.update()

    def _update_velocity_from_cap(self, plane: MovingPlane):
        plane.update_velocity_from_cap()

    def update_plane_position(self, plane):
        """
        Redessine uniquement l'avion passé en paramètre
        pour que les touches soient instantanées.
        """
        if plane not in self.planes:
            return

        # Définir un rectangle autour de l'avion (zone à rafraîchir)
        w = plane.size * 2
        h = plane.size * 2
        rect = plane.pos.toPoint().x() - plane.size, plane.pos.toPoint().y() - plane.size, w, h
        self.update(*rect)
