import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QGroupBox, QSizePolicy, QListWidget, QListWidgetItem, QProgressBar,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from Carte import GameWidget
from message_defilant import MarqueeLabel
from meteo import MeteoManager


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

        self.label_message = MarqueeLabel("Rien à signaler")  # message défilant
        self.label_message.setFixedHeight(40)

        self.label_piste = QLabel("Piste de côté")
        self.label_piste.setFrameShape(QLabel.Panel)
        self.label_piste.setAlignment(Qt.AlignCenter)

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
        self.player.setSource("Musiques/musique_de_fond_interface_principale.mp3")
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

        for b in [btn_monter, btn_descendre, btn_gauche, btn_droite,
                  btn_atterrir, btn_attente, btn_urgence]:
            b.setFixedHeight(60)

        # Connexion des boutons
        btn_monter.clicked.connect(self.widget_carte.monter_selected)
        btn_descendre.clicked.connect(self.widget_carte.descendre_selected)
        btn_gauche.clicked.connect(self.widget_carte.gauche_selected)
        btn_droite.clicked.connect(self.widget_carte.droite_selected)

        group_controles = QGroupBox("Contrôles")
        layout_controles = QVBoxLayout()
        layout_controles.addStretch(1)

        # --- Barres d’information avion sélectionné ---
        self.bar_altitude = QProgressBar()
        self.bar_vitesse = QProgressBar()
        self.bar_fuel = QProgressBar()

        self.bar_altitude.setFormat("Altitude : %v m")
        self.bar_vitesse.setFormat("Vitesse : %v km/h")
        self.bar_fuel.setFormat("Carburant : %v %")

        # Taille épaisse
        self.bar_altitude.setFixedHeight(50)
        self.bar_vitesse.setFixedHeight(50)
        self.bar_fuel.setFixedHeight(50)

        # Style classique (la couleur du chunk sera dynamique)
        bar_style = """
        QProgressBar {
            border: 2px solid #444;
            border-radius: 10px;
            background: #222;
            text-align: center;
            font-size: 18px;
            color: white;
            height: 50px;
        }
        QProgressBar::chunk {
            border-radius: 10px;
            margin: 2px;
            background-color: #5BC074;
        }
        """
        self.bar_altitude.setStyleSheet(bar_style)
        self.bar_vitesse.setStyleSheet(bar_style)
        self.bar_fuel.setStyleSheet(bar_style)

        layout_controles.addWidget(self.bar_altitude)
        layout_controles.addWidget(self.bar_vitesse)
        layout_controles.addWidget(self.bar_fuel)

        layout_controles.addWidget(btn_urgence)
        layout_controles.addWidget(btn_attente)
        layout_controles.addWidget(btn_atterrir)
        group_controles.setLayout(layout_controles)

        group_instructions = QGroupBox("Instructions")
        layout_instructions = QVBoxLayout()
        layout_instructions.addWidget(btn_monter)
        layout_instructions.addWidget(btn_descendre)
        layout_instructions.addWidget(btn_gauche)
        layout_instructions.addWidget(btn_droite)
        group_instructions.setLayout(layout_instructions)

        # ---------- Layouts principaux ----------
        layout_gauche = QVBoxLayout()
        layout_gauche.addWidget(group_controles)
        layout_gauche.addWidget(group_instructions)

        layout_centre = QVBoxLayout()
        layout_centre.addWidget(carte_box, 5)
        layout_centre.addWidget(self.label_message, 1)
        layout_centre.addWidget(self.label_piste, 5)

        layout_droite = QVBoxLayout()
        layout_droite.addWidget(self.label_stats)
        layout_droite.addWidget(group_avions, 1)

        layout_zone_jeu = QHBoxLayout()
        layout_zone_jeu.addLayout(layout_droite, 1)
        layout_zone_jeu.addLayout(layout_centre, 2)
        layout_zone_jeu.addLayout(layout_gauche, 1)

        # Layout global
        layout_global = QVBoxLayout()
        layout_global.addWidget(barre_haut)
        layout_global.addLayout(layout_zone_jeu)

        central_widget = QWidget()
        central_widget.setLayout(layout_global)
        self.setCentralWidget(central_widget)

        # ---------- Connections pour liste <-> carte ----------
        self.liste_avions.currentItemChanged.connect(self.on_liste_avion_selected)
        self.widget_carte.avion_selectionne_changed.connect(self.on_carte_avion_selected)
        self.widget_carte.avion_updated.connect(self.update_plane_list_item)


    def toggle_pause(self):
        self.paused = not self.paused
        self.widget_carte.set_paused(self.paused)

        from collision_meteo import CollisionManager
        CollisionManager.paused = self.paused
        if hasattr(self.meteo_manager, 'set_paused'):
            self.meteo_manager.set_paused(self.paused)
        if self.paused:
            self.btn_pause.setText("Reprendre")
        else:
            self.btn_pause.setText("Pause")

        # ---------- Fonctions de couleur ----------
        def lerp_color(self, c1, c2, t):
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            return (r, g, b)

        def update_progress_bar_spectrum(self, bar, value, maximum, spectrum):
            """
            Met à jour une QProgressBar avec couleur dynamique et texte lisible.
            Le chunk est en dégradé, et le texte reste lisible grâce à un léger contour.
            """
            # Clamp value
            value = max(0, min(value, maximum))
            bar.setMaximum(maximum)
            bar.setValue(value)

            # Calcul couleur du chunk selon spectre
            t = value / maximum
            n = len(spectrum) - 1
            idx = min(int(t * n), n - 1)
            t_local = (t * n) - idx
            r = int(spectrum[idx][0] + (spectrum[idx + 1][0] - spectrum[idx][0]) * t_local)
            g = int(spectrum[idx][1] + (spectrum[idx + 1][1] - spectrum[idx][1]) * t_local)
            b = int(spectrum[idx][2] + (spectrum[idx + 1][2] - spectrum[idx][2]) * t_local)

            # Choix de la couleur du texte : blanc ou noir selon luminosité du chunk
            brightness = (r * 0.299 + g * 0.587 + b * 0.114)
            text_color = "white" if brightness < 160 else "black"

            # Style de la barre avec texte lisible
            bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #444;
                border-radius: 10px;
                background: #222;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                color: {text_color};
                height: 50px;
            }}
            QProgressBar::chunk {{
                border-radius: 10px;
                margin: 2px;
                background-color: rgb({r},{g},{b});
            }}
            """)

    # ---------- Mise à jour instantanée de la liste ----------
    def update_plane_list_item(self, plane):
        """Met à jour la liste des avions et supprime après 5s d'arrêt."""
        if plane not in self.widget_carte.planes:
            # Supprime de la liste si présent
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

        # Sinon, met à jour ou ajoute l’avion dans la liste
        for i in range(self.liste_avions.count()):
            item = self.liste_avions.item(i)
            if item.data(Qt.UserRole) == plane:
                item.setText(
                    f"{plane.avion.nom} - Alt: {plane.avion.altitude} m - "
                    f"Vit: {plane.avion.vitesse} km/h - "
                    f"Fuel: {plane.avion.fuel:.1f}% - "
                    f"Cap: {plane.avion.cap:.1f}°"
                )
                break
        else:
            item = QListWidgetItem(
                f"{plane.avion.nom} - Alt: {plane.avion.altitude} m - "
                f"Vit: {plane.avion.vitesse} km/h - "
                f"Fuel: {plane.avion.fuel:.1f}% - "
                f"Cap: {plane.avion.cap:.1f}°"
            )
            item.setData(Qt.UserRole, plane)
            self.liste_avions.addItem(item)

        if plane is self.widget_carte.selected_plane:
            # Altitude : violet foncé → bleu clair
            self.update_progress_bar_spectrum(self.bar_altitude, plane.avion.altitude, 12000,
                                              [(80,0,120),(120,200,255)])
            # Vitesse : spectre complet
            vitesse_spectrum = [
                (128,0,128),(0,0,255),(0,255,0),(255,255,0),(255,128,0),(255,0,0)
            ]
            self.update_progress_bar_spectrum(self.bar_vitesse, plane.avion.vitesse, 900,
                                              vitesse_spectrum)
            # Fuel : rouge → jaune
            self.update_progress_bar_spectrum(self.bar_fuel, plane.avion.fuel, 100,
                                              [(255,0,0),(255,255,0)])

    # ---------- Sélection liste -> carte ----------
    def on_liste_avion_selected(self, current, previous):
        if current:
            plane = current.data(Qt.UserRole)
            self.widget_carte.selected_plane = plane
            self.widget_carte.update()
            self.update_plane_list_item(plane)

    # ---------- Sélection carte -> liste ----------
    def on_carte_avion_selected(self, avion):
        if avion is None:
            self.bar_altitude.setValue(0)
            self.bar_vitesse.setValue(0)
            self.bar_fuel.setValue(0)
            return
        self.update_plane_list_item(avion)
        for i in range(self.liste_avions.count()):
            item = self.liste_avions.item(i)
            if item.data(Qt.UserRole).avion == avion:
                self.liste_avions.setCurrentItem(item)
                return

    # ---------- Pause ----------
    def toggle_pause(self):
        self.en_pause = not self.en_pause
        if self.en_pause:
            self.widget_carte.timer.stop()
            self.btn_pause.setText("Reprendre")
        else:
            self.widget_carte.timer.start()
            self.btn_pause.setText("Pause")

    # ---------- Retour au menu ----------
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
