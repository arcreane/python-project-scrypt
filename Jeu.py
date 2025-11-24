import sys
import math
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QGroupBox, QSizePolicy, QListWidget, QListWidgetItem, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen, QConicalGradient
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from Carte import GameWidget
from message_defilant import MarqueeLabel
from meteo import MeteoManager
from landing import LandingView


# ---------- QLabel avec contour noir ----------
class ContouredLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.font())
        text = self.text()
        rect = self.rect()

        # Contour noir
        pen = QPen(QColor(0, 0, 0))
        painter.setPen(pen)
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for dx, dy in offsets:
            painter.drawText(rect.translated(dx, dy), Qt.AlignCenter, text)

        # Texte blanc au-dessus
        pen = QPen(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(rect, Qt.AlignCenter, text)
        painter.end()


# ---------- QProgressBar avec contour de texte ----------
class ContouredProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTextVisible(True)
        self.setMinimumHeight(50)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.font())

        text = self.text()
        rect = self.rect()

        # Contour noir
        pen = QPen(QColor(0, 0, 0))
        painter.setPen(pen)
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for dx, dy in offsets:
            painter.drawText(rect.translated(dx, dy), Qt.AlignCenter, text)

        # Texte blanc au-dessus
        pen = QPen(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawText(rect, Qt.AlignCenter, text)
        painter.end()


# ---------------- ContouredCompass (boussole stylée comme les barres) ----------------
class ContouredCompass(QWidget):
    def __init__(self):
        super().__init__()
        self.cap = 0
        self.setMinimumHeight(220)  # augmente la taille verticale
        self.setMinimumWidth(220)  # assure que la largeur suit pour un cercle plus grand

    def set_cap(self, cap):
        try:
            self.cap = float(cap) % 360
        except Exception:
            self.cap = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 12

        # Fond sombre + bordure arrondie (visuellement cohérent avec les barres)
        painter.setBrush(QColor(34, 34, 34))  # #222-like
        painter.setPen(QPen(QColor(68, 68, 68), 2))  # #444-like
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 10, 10)

        # Cercle intérieur (bord noir)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawEllipse(center, radius, radius)

        # N/E/S/W avec contour noir + texte blanc (même traitement que pour les barres)
        font = self.font()
        painter.setFont(font)
        for angle, label in [(0, "N"), (90, "E"), (180, "S"), (270, "W")]:
            rad = math.radians(angle)
            x = center.x() + (radius - 20) * math.cos(rad)
            y = center.y() - (radius - 20) * math.sin(rad)

            # contour noir (4 offsets)
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                painter.setPen(QColor(0, 0, 0))
                painter.drawText(x + dx - 6, y + dy + 6, label)

            # texte blanc
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(x - 6, y + 6, label)

        # Aiguille avec gradient rouge -> orange (cohérent visuellement avec les barres)
        painter.save()
        painter.translate(center.x(), center.y())
        painter.rotate(-self.cap)  # on inverse la rotation pour pointer vers le cap
        grad = QConicalGradient(0, 0, 0)
        grad.setColorAt(0.0, QColor(255, 0, 0))
        grad.setColorAt(1.0, QColor(255, 165, 0))
        pen = QPen(QColor(255, 0, 0), 4)
        painter.setPen(pen)
        painter.setBrush(grad)
        # dessiner une ligne horizontale (puisque on a pivoté le contexte)
        painter.drawLine(0, 0, int(radius * 0.78), 0)
        painter.restore()

        painter.end()


class MainGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.paused = False
        self.setWindowTitle("SkyLink")
        self.showFullScreen()

        # ---------- Barre du haut ----------
        barre_haut = QWidget()
        barre_haut.setMaximumHeight(40)
        barre_haut.setStyleSheet("background-color: #5D4482;")
        layout_barre = QHBoxLayout(barre_haut)
        layout_barre.setContentsMargins(5, 5, 5, 5)
        layout_barre.setSpacing(5)

        message_label = QLabel("L'équipe Scrypt vous souhaite une bonne partie !")
        message_label.setAlignment(Qt.AlignCenter)
        font = message_label.font()
        font.setPointSize(18)
        font.setBold(True)
        message_label.setFont(font)
        message_label.setStyleSheet("color: white;")
        layout_barre.addWidget(message_label)
        layout_barre.addStretch(1)

        btn_pause = QPushButton("Pause")
        btn_pause.clicked.connect(self.toggle_pause)
        self.btn_pause = btn_pause
        btn_recommencer = QPushButton("Recommencer")
        btn_quitter = QPushButton("Quitter")
        btn_quitter.clicked.connect(self.retour_menu)
        layout_barre.addWidget(btn_pause)
        layout_barre.addWidget(btn_recommencer)
        layout_barre.addWidget(btn_quitter)

        # Style des boutons
        btn_pause.setStyleSheet("""
            QPushButton { background-color: rgba(80, 150, 255, 140); color: white; border-radius: 10px; padding: 8px 16px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #C5A6F0; }
        """)
        btn_recommencer.setStyleSheet("""
            QPushButton { background-color: #5BC074; color: white; border-radius: 10px; padding: 8px 16px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #79D890; }
        """)
        btn_quitter.setStyleSheet("""
            QPushButton { background-color: #E85757; color: white; border-radius: 10px; padding: 8px 16px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #FF6F6F; }
        """)

        # ---------- Zone centrale ----------
        self.label_stats = QLabel("Stats")
        self.label_stats.setFrameShape(QLabel.Panel)
        self.label_stats.setAlignment(Qt.AlignCenter)

        self.label_message = MarqueeLabel("Rien à signaler")
        self.label_message.setFixedHeight(40)

        self.landing_view = LandingView()

        # Carte
        carte_box = QGroupBox()
        carte_box.setFlat(True)
        carte_box.setStyleSheet("QGroupBox { border: none; }")
        layout_carte = QVBoxLayout()
        layout_carte.setContentsMargins(0, 0, 0, 0)
        layout_carte.setSpacing(0)
        self.widget_carte = GameWidget()
        self.widget_carte.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout_carte.addWidget(self.widget_carte)
        carte_box.setLayout(layout_carte)
        self.meteo_manager = MeteoManager(self.widget_carte)

        # ---------- Liste des avions ----------
        self.liste_avions = QListWidget()
        self.liste_avions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.liste_avions.setAlternatingRowColors(True)
        self.liste_avions.setStyleSheet("""
            QListWidget::item:selected { background-color: #88C0D0; color: black; }
            QListWidget::item:hover { background-color: #A3D0E0; }
        """)

        group_avions = QGroupBox("Avions")
        layout_avions = QVBoxLayout()
        layout_avions.addWidget(self.liste_avions)
        group_avions.setLayout(layout_avions)

        # ---------- Musique d'ambiance ----------
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource("Musiques/Musique_jeu.mp3")
        self.player.setLoops(QMediaPlayer.Infinite)
        self.player.play()

        # ---------- Boutons de contrôle ----------
        btn_monter = QPushButton("Monter")
        btn_descendre = QPushButton("Descendre")
        btn_gauche = QPushButton("Gauche")
        btn_droite = QPushButton("Droite")
        btn_atterrir = QPushButton("Atterrir")
        btn_attente = QPushButton("Attente")
        btn_urgence = QPushButton("Urgence")
        btn_accelerer = QPushButton("Accélérer")
        btn_ralentir = QPushButton("Ralentir")

        for b in [btn_monter, btn_descendre, btn_gauche, btn_droite,
                  btn_atterrir, btn_attente, btn_urgence, btn_accelerer, btn_ralentir]:
            b.setFixedHeight(60)

        btn_gauche.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_droite.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Connexion des boutons
        btn_monter.clicked.connect(self.widget_carte.monter_selected)
        btn_descendre.clicked.connect(self.widget_carte.descendre_selected)
        btn_gauche.clicked.connect(self.widget_carte.gauche_selected)
        btn_droite.clicked.connect(self.widget_carte.droite_selected)
        btn_urgence.clicked.connect(self.widget_carte.urgence_selected)
        btn_attente.clicked.connect(self.widget_carte.attente_selected)

        group_controles = QGroupBox("Contrôles")
        layout_controles = QVBoxLayout()
        layout_controles.addStretch(1)

        # Informations de l'avion sélectionné avec contour
        self.label_nom_avion = ContouredLabel("Aucun avion sélectionné")
        self.label_nom_avion.setAlignment(Qt.AlignCenter)
        font = self.label_nom_avion.font()
        font.setPointSize(20)
        font.setBold(True)
        self.label_nom_avion.setFont(font)
        layout_controles.addWidget(self.label_nom_avion)

        # --- Boussole ajoutée ici (entre le nom et les barres) ---
        self.compass = ContouredCompass()
        layout_controles.addWidget(self.compass)

        self.bar_altitude = ContouredProgressBar()
        self.bar_vitesse = ContouredProgressBar()
        self.bar_fuel = ContouredProgressBar()

        self.bar_altitude.setFormat("Altitude : %v m")
        self.bar_vitesse.setFormat("Vitesse : %v km/h")
        self.bar_fuel.setFormat("Carburant : %v %")

        # Valeurs initiales
        self.bar_altitude.setMaximum(12000)
        self.bar_altitude.setValue(0)
        self.update_progress_bar_spectrum(self.bar_altitude, 0, 12000, [(80, 0, 120), (120, 200, 255)])

        self.bar_vitesse.setMaximum(900)
        self.bar_vitesse.setValue(0)
        self.update_progress_bar_spectrum(self.bar_vitesse, 0, 900,
                                          [(128,0,128),(0,0,255),(0,255,0),(255,255,0),(255,128,0),(255,0,0)])

        self.bar_fuel.setMaximum(100)
        self.bar_fuel.setValue(0)
        self.update_progress_bar_spectrum(self.bar_fuel, 0, 100, [(255,0,0),(255,255,0)])

        # Layouts
        layout_controles.addWidget(self.bar_altitude)
        layout_controles.addWidget(self.bar_vitesse)
        layout_controles.addWidget(self.bar_fuel)
        layout_controles.addWidget(btn_urgence)
        layout_controles.addWidget(btn_attente)
        layout_controles.addWidget(btn_atterrir)
        group_controles.setLayout(layout_controles)

        group_instructions = QGroupBox("Instructions")
        layout_instructions = QVBoxLayout()
        layout_instructions.setContentsMargins(0, 0, 0, 0)
        layout_instructions.setSpacing(5)

        layout_instructions.addWidget(btn_monter)
        layout_instructions.addWidget(btn_descendre)

        layout_gauche_droite = QHBoxLayout()
        layout_gauche_droite.setSpacing(5)
        layout_gauche_droite.addWidget(btn_gauche)
        layout_gauche_droite.addWidget(btn_droite)
        layout_instructions.addLayout(layout_gauche_droite)

        layout_instructions.addWidget(btn_accelerer)
        layout_instructions.addWidget(btn_ralentir)
        group_instructions.setLayout(layout_instructions)

        # ---------- Layouts principaux ----------
        layout_gauche = QVBoxLayout()
        layout_gauche.addWidget(group_controles)
        layout_gauche.addWidget(group_instructions)

        layout_centre = QVBoxLayout()
        layout_centre.addWidget(carte_box, 5)
        layout_centre.addWidget(self.label_message, 1)
        layout_centre.addWidget(self.landing_view, 5)

        layout_droite = QVBoxLayout()
        layout_droite.addWidget(self.label_stats)
        layout_droite.addWidget(group_avions, 1)

        layout_zone_jeu = QHBoxLayout()
        layout_zone_jeu.addLayout(layout_droite, 1)
        layout_zone_jeu.addLayout(layout_centre, 2)
        layout_zone_jeu.addLayout(layout_gauche, 1)

        layout_global = QVBoxLayout()
        layout_global.addWidget(barre_haut)
        layout_global.addLayout(layout_zone_jeu)

        central_widget = QWidget()
        central_widget.setLayout(layout_global)
        self.setCentralWidget(central_widget)

        # ---------- Connections liste <-> carte ----------
        self.liste_avions.currentItemChanged.connect(self.on_liste_avion_selected)
        self.widget_carte.avion_selectionne_changed.connect(self.on_carte_avion_selected)
        self.widget_carte.avion_updated.connect(self.update_plane_list_item)

    # ---------- Fonctions ----------
    def toggle_pause(self):
        self.paused = not self.paused
        self.widget_carte.set_paused(self.paused)
        from collision_meteo import CollisionManager
        CollisionManager.paused = self.paused
        if hasattr(self.meteo_manager, 'set_paused'):
            self.meteo_manager.set_paused(self.paused)
        self.btn_pause.setText("Reprendre" if self.paused else "Pause")

    def update_progress_bar_spectrum(self, bar, value, maximum, spectrum):
        value = max(0, min(value, maximum))
        bar.setMaximum(maximum)
        bar.setValue(value)

        t = value / maximum
        n = len(spectrum) - 1
        idx = min(int(t * n), n - 1)
        t_local = (t * n) - idx
        r = int(spectrum[idx][0] + (spectrum[idx + 1][0] - spectrum[idx][0]) * t_local)
        g = int(spectrum[idx][1] + (spectrum[idx + 1][1] - spectrum[idx][1]) * t_local)
        b = int(spectrum[idx][2] + (spectrum[idx + 1][2] - spectrum[idx][2]) * t_local)

        bar.setStyleSheet(f"""
        QProgressBar {{
            border: 2px solid #444;
            border-radius: 10px;
            background: #222;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: white;
        }}
        QProgressBar::chunk {{
            border-radius: 10px;
            margin: 2px;
            background-color: rgb({r},{g},{b});
        }}
        """)

    def update_plane_list_item(self, plane):
        if plane not in self.widget_carte.planes:
            for i in range(self.liste_avions.count()):
                item = self.liste_avions.item(i)
                if item.data(Qt.UserRole) == plane:
                    self.liste_avions.takeItem(i)
                    break
            if self.widget_carte.selected_plane == plane:
                self.bar_altitude.setValue(0)
                self.bar_vitesse.setValue(0)
                self.bar_fuel.setValue(0)
            return

        for i in range(self.liste_avions.count()):
            item = self.liste_avions.item(i)
            if item.data(Qt.UserRole) == plane:
                item.setText(
                    f"{plane.avion.nom} - Alt: {plane.avion.altitude} m - Vit: {plane.avion.vitesse} km/h - Fuel: {plane.avion.fuel:.1f}% - Cap: {plane.avion.cap:.1f}°")
                break
        else:
            item = QListWidgetItem(
                f"{plane.avion.nom} - Alt: {plane.avion.altitude} m - Vit: {plane.avion.vitesse} km/h - Fuel: {plane.avion.fuel:.1f}% - Cap: {plane.avion.cap:.1f}°")
            item.setData(Qt.UserRole, plane)
            self.liste_avions.addItem(item)

        if plane is self.widget_carte.selected_plane:
            self.update_progress_bar_spectrum(self.bar_altitude, plane.avion.altitude, 12000,
                                              [(80, 0, 120), (120, 200, 255)])
            vitesse_spectrum = [(128, 0, 128), (0, 0, 255), (0, 255, 0),
                                (255, 255, 0), (255, 128, 0), (255, 0, 0)]
            self.update_progress_bar_spectrum(self.bar_vitesse, plane.avion.vitesse, 900, vitesse_spectrum)
            self.update_progress_bar_spectrum(self.bar_fuel, plane.avion.fuel, 100, [(255, 0, 0), (255, 255, 0)])
            # Mise à jour de la boussole si l'avion sélectionné change
            try:
                self.compass.set_cap(plane.avion.cap)
            except Exception:
                pass

    def on_liste_avion_selected(self, current, previous):
        if current:
            plane = current.data(Qt.UserRole)
            self.widget_carte.selected_plane = plane
            self.landing_view.set_selected_plane(plane)
            self.widget_carte.update()
            self.update_plane_list_item(plane)
            self.label_nom_avion.setText(plane.avion.nom)
            # mettre à jour la boussole
            try:
                self.compass.set_cap(plane.avion.cap)
            except Exception:
                pass

    def on_carte_avion_selected(self, avion):
        if avion is None:
            self.label_nom_avion.setText("Aucun avion sélectionné")
            self.bar_altitude.setValue(0)
            self.bar_vitesse.setValue(0)
            self.bar_fuel.setValue(0)
            self.landing_view.set_selected_plane(None)
            # reset boussole
            try:
                self.compass.set_cap(0)
            except Exception:
                pass
            return
        self.label_nom_avion.setText(avion.nom)
        self.update_plane_list_item(avion)
        self.landing_view.set_selected_plane(avion)
        # mettre à jour la boussole
        try:
            self.compass.set_cap(avion.cap)
        except Exception:
            pass
        for i in range(self.liste_avions.count()):
            item = self.liste_avions.item(i)
            if item.data(Qt.UserRole).avion == avion:
                self.liste_avions.setCurrentItem(item)
                return

    def retour_menu(self):
        if self.player:
            self.player.stop()
        from Accueil import Window
        self.menu_window = Window()
        self.menu_window.showFullScreen()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGameWindow()
    window.show()
    sys.exit(app.exec())
