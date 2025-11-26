import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QGroupBox, QSizePolicy, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

# Modules du projet
from Carte import GameWidget
from message_defilant import MarqueeLabel
from meteo import MeteoManager
from landing import LandingView
from collision_meteo import CollisionManager
from Informations_avion import ContouredLabel, ContouredProgressBar, ContouredCompass


class MainGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.paused = False
        self.setWindowTitle("SkyLink")
        self.showFullScreen()

        # Initialisation des composants
        self.init_top_bar()
        self.init_central_widgets()
        self.init_avion_controls()
        self.init_instructions()
        self.init_main_layout()
        self.init_connections()
        self.init_music()

    # Barre du haut
    def init_top_bar(self):
        self.barre_haut = QWidget()
        self.barre_haut.setMaximumHeight(40)
        self.barre_haut.setStyleSheet("background-color: #5D4482;")

        layout_barre = QHBoxLayout(self.barre_haut)
        layout_barre.setContentsMargins(5, 5, 5, 5)
        layout_barre.setSpacing(5)

        # Message
        self.message_label = QLabel("L'équipe Scrypt vous souhaite une bonne partie !")
        self.message_label.setAlignment(Qt.AlignCenter)
        font = self.message_label.font()
        font.setPointSize(18)
        font.setBold(True)
        self.message_label.setFont(font)
        self.message_label.setStyleSheet("color: white;")
        layout_barre.addWidget(self.message_label)
        layout_barre.addStretch(1)

        # Boutons
        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self.toggle_pause)
        self.btn_recommencer = QPushButton("Recommencer")
        self.btn_quitter = QPushButton("Quitter")
        self.btn_quitter.clicked.connect(self.retour_menu)

        for b, style in zip(
            [self.btn_pause, self.btn_recommencer, self.btn_quitter],
            [
                """
                QPushButton { background-color: rgba(80, 150, 255, 140); color: white;
                border-radius: 10px; padding: 8px 16px; font-size: 16px; font-weight: bold; }
                QPushButton:hover { background-color: #C5A6F0; }""",
                """
                QPushButton { background-color: #5BC074; color: white; border-radius: 10px;
                padding: 8px 16px; font-size: 16px; font-weight: bold; }
                QPushButton:hover { background-color: #79D890; }""",
                """
                QPushButton { background-color: #E85757; color: white; border-radius: 10px;
                padding: 8px 16px; font-size: 16px; font-weight: bold; }
                QPushButton:hover { background-color: #FF6F6F; }"""
            ]
        ):
            b.setStyleSheet(style)
            layout_barre.addWidget(b)

    # Widgets centraux
    def init_central_widgets(self):
        # Stats et message
        self.label_stats = QLabel("Stats")
        self.label_stats.setFrameShape(QLabel.Panel)
        self.label_stats.setAlignment(Qt.AlignCenter)

        self.label_message = MarqueeLabel("Rien à signaler")
        self.label_message.setFixedHeight(40)

        # Carte et météo
        self.landing_view = LandingView()
        self.widget_carte = GameWidget()
        self.widget_carte.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.meteo_manager = MeteoManager(self.widget_carte)

        self.carte_box = QGroupBox()
        self.carte_box.setFlat(True)
        self.carte_box.setStyleSheet("QGroupBox { border: none; }")
        layout_carte = QVBoxLayout()
        layout_carte.setContentsMargins(0, 0, 0, 0)
        layout_carte.setSpacing(0)
        layout_carte.addWidget(self.widget_carte)
        self.carte_box.setLayout(layout_carte)

        # Liste des avions
        self.liste_avions = QListWidget()
        self.liste_avions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.liste_avions.setAlternatingRowColors(True)
        self.liste_avions.setStyleSheet("""
            QListWidget::item:selected { background-color: #88C0D0; color: black; }
            QListWidget::item:hover { background-color: #A3D0E0; }
        """)

        self.group_avions = QGroupBox("Avions")
        layout_avions = QVBoxLayout()
        layout_avions.addWidget(self.liste_avions)
        self.group_avions.setLayout(layout_avions)

    # Groupe Contrôles
    def init_avion_controls(self):
        # Boutons
        self.btn_monter = QPushButton("Monter")
        self.btn_descendre = QPushButton("Descendre")
        self.btn_gauche = QPushButton("Gauche")
        self.btn_droite = QPushButton("Droite")
        self.btn_atterrir = QPushButton("Atterrir")
        self.btn_attente = QPushButton("Attente")
        self.btn_urgence = QPushButton("Urgence")
        self.btn_accelerer = QPushButton("Accélérer")
        self.btn_ralentir = QPushButton("Ralentir")

        self.all_buttons = [self.btn_monter, self.btn_descendre, self.btn_gauche, self.btn_droite,
                            self.btn_atterrir, self.btn_attente, self.btn_urgence, self.btn_accelerer, self.btn_ralentir]
        for b in self.all_buttons:
            b.setFixedHeight(60)

        self.btn_gauche.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_droite.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Connexion des boutons
        self.btn_monter.clicked.connect(self.widget_carte.monter_selected)
        self.btn_descendre.clicked.connect(self.widget_carte.descendre_selected)
        self.btn_gauche.clicked.connect(self.widget_carte.gauche_selected)
        self.btn_droite.clicked.connect(self.widget_carte.droite_selected)
        self.btn_accelerer.clicked.connect(self.widget_carte.accelerer_selected)
        self.btn_ralentir.clicked.connect(self.widget_carte.ralentir_selected)
        self.btn_urgence.clicked.connect(self.widget_carte.urgence_selected)
        self.btn_attente.clicked.connect(self.widget_carte.attente_selected)

        # Infos avion et boussole
        self.label_nom_avion = ContouredLabel("Sélectionner un avion")
        self.label_nom_avion.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = self.label_nom_avion.font()
        font.setPointSize(18)
        font.setBold(True)
        self.label_nom_avion.setFont(font)

        self.compass = ContouredCompass()
        layout_avion_top = QHBoxLayout()
        layout_avion_top.addWidget(self.label_nom_avion, 1)
        layout_avion_top.addWidget(self.compass, 0)

        # Progress bars
        self.bar_altitude = ContouredProgressBar()
        self.bar_vitesse = ContouredProgressBar()
        self.bar_fuel = ContouredProgressBar()
        self.bar_altitude.setFormat("Altitude : %v m")
        self.bar_vitesse.setFormat("Vitesse : %v km/h")
        self.bar_fuel.setFormat("Carburant : %v %")
        self.bar_altitude.setMaximum(12000)
        self.bar_vitesse.setMaximum(900)
        self.bar_fuel.setMaximum(100)
        self.update_progress_bar_spectrum(self.bar_altitude, 0, 12000, [(80,0,120),(120,200,255)])
        self.update_progress_bar_spectrum(self.bar_vitesse, 0, 900,
                                          [(128,0,128),(0,0,255),(0,255,0),(255,255,0),(255,128,0),(255,0,0)])
        self.update_progress_bar_spectrum(self.bar_fuel, 0, 100, [(255,0,0),(255,255,0)])

        # Layout du groupe
        self.group_controles = QGroupBox("Contrôles")
        layout_controles = QVBoxLayout()
        layout_controles.addLayout(layout_avion_top)

        layout_urgence_attente = QHBoxLayout()
        layout_urgence_attente.setSpacing(5)
        layout_urgence_attente.addWidget(self.btn_urgence)
        layout_urgence_attente.addWidget(self.btn_attente)

        layout_controles.addWidget(self.bar_altitude)
        layout_controles.addWidget(self.bar_vitesse)
        layout_controles.addWidget(self.bar_fuel)
        layout_controles.addLayout(layout_urgence_attente)
        layout_controles.addWidget(self.btn_atterrir)
        self.group_controles.setLayout(layout_controles)
        self.group_controles.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # Groupe Instructions
    def init_instructions(self):
        self.group_instructions = QGroupBox("Instructions")
        layout_instructions = QVBoxLayout()
        layout_instructions.setContentsMargins(0,0,0,0)
        layout_instructions.setSpacing(5)

        layout_instructions.addWidget(self.btn_monter)
        layout_instructions.addWidget(self.btn_descendre)
        layout_gauche_droite = QHBoxLayout()
        layout_gauche_droite.setSpacing(5)
        layout_gauche_droite.addWidget(self.btn_gauche)
        layout_gauche_droite.addWidget(self.btn_droite)
        layout_instructions.addLayout(layout_gauche_droite)
        layout_instructions.addWidget(self.btn_accelerer)
        layout_instructions.addWidget(self.btn_ralentir)
        self.group_instructions.setLayout(layout_instructions)
        self.group_instructions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # Layout principal
    def init_main_layout(self):
        layout_gauche = QVBoxLayout()
        layout_gauche.addWidget(self.group_controles, 1)
        layout_gauche.addWidget(self.group_instructions, 1)

        layout_centre = QVBoxLayout()
        layout_centre.addWidget(self.carte_box, 5)
        layout_centre.addWidget(self.label_message, 1)
        layout_centre.addWidget(self.landing_view, 5)

        layout_droite = QVBoxLayout()
        layout_droite.addWidget(self.label_stats)
        layout_droite.addWidget(self.group_avions, 1)

        layout_zone_jeu = QHBoxLayout()
        layout_zone_jeu.addLayout(layout_droite, 1)
        layout_zone_jeu.addLayout(layout_centre, 2)
        layout_zone_jeu.addLayout(layout_gauche, 1)

        layout_global = QVBoxLayout()
        layout_global.addWidget(self.barre_haut)
        layout_global.addLayout(layout_zone_jeu)

        central_widget = QWidget()
        central_widget.setLayout(layout_global)
        self.setCentralWidget(central_widget)

    # Connexions
    def init_connections(self):
        self.liste_avions.currentItemChanged.connect(self.on_liste_avion_selected)
        self.widget_carte.avion_selectionne_changed.connect(self.on_carte_avion_selected)
        self.widget_carte.avion_updated.connect(self.update_plane_list_item)

    # Musique
    def init_music(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource("Musiques/Musique_jeu.mp3")
        self.player.setLoops(QMediaPlayer.Infinite)
        self.player.play()

    # Fonctions utilitaires
    def toggle_pause(self):
        self.paused = not self.paused
        self.widget_carte.set_paused(self.paused)
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
            self.update_progress_bar_spectrum(self.bar_altitude, plane.avion.altitude, 12000, [(80,0,120),(120,200,255)])
            vitesse_spectrum = [(128,0,128),(0,0,255),(0,255,0),(255,255,0),(255,128,0),(255,0,0)]
            self.update_progress_bar_spectrum(self.bar_vitesse, plane.avion.vitesse, 900, vitesse_spectrum)
            self.update_progress_bar_spectrum(self.bar_fuel, plane.avion.fuel, 100, [(255,0,0),(255,255,0)])
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
            try:
                self.compass.set_cap(plane.avion.cap)
            except Exception:
                pass

    def on_carte_avion_selected(self, avion):
        if avion is None:
            self.label_nom_avion.setText("Sélectionner un avion")
            self.bar_altitude.setValue(0)
            self.bar_vitesse.setValue(0)
            self.bar_fuel.setValue(0)
            self.landing_view.set_selected_plane(None)
            try:
                self.compass.set_cap(0)
            except Exception:
                pass
            return
        self.label_nom_avion.setText(avion.nom)
        self.update_plane_list_item(avion)
        self.landing_view.set_selected_plane(avion)
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
