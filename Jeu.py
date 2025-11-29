import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QGroupBox, QSizePolicy, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

# Modules du projet
from Carte import GameWidget
from message_defilant import MarqueeLabel
from meteo import MeteoManager
from landing import LandingView
from collision_meteo import CollisionManager
from Informations_avion import ContouredLabel, ContouredProgressBar, ContouredCompass
from esthetisme_avion_layout import style_layout_avions
from esthetisme_instructions_layout import style_layout_instructions
from Game_over import GameOverWidget
from game_level_manager import GameLevelManager
from esthetisme_stats_layout import style_layout_stats


class MainGameWindow(QMainWindow):

    # CONSTRUCTEUR
    def __init__(self):
        super().__init__()

        # États
        self.global_paused = False
        self.paused = False
        self.suppress_auto_selection = False
        self.control_ground_mode = False

        # Fenêtre
        self.setWindowTitle("SkyLink")
        self.showFullScreen()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        # Score
        self.score = 0
        self.score_label = QLabel("Score : 0")
        self._init_score_label()

        # Niveau
        self.niveau_label = QLabel("Niveau : 1")
        self._init_niveau_label()

        # UI générale
        self.init_top_bar()
        self.init_central_widgets()
        self.init_avion_controls()
        self.init_instructions()
        self.init_main_layout()

        # Gestion du niveau
        self.level_manager = GameLevelManager(self)

        # Timer du score
        self.score_timer = QTimer()
        self.score_timer.timeout.connect(self.update_score)
        self.score_timer.start(1000)

        # Connexions
        self.init_connections()

        # Météo → update message
        self.meteo_manager.evenements_changed.connect(self.mettre_a_jour_message_defilant)

        # Musique
        self.init_music()

        # Stats
        self.update_stats()

    # LABELS SCORE/NIVEAU
    def _init_score_label(self):
        font = self.score_label.font()
        font.setPointSize(20)
        font.setBold(True)
        self.score_label.setFont(font)
        self.score_label.setStyleSheet("color: #FFD700;")

    def _init_niveau_label(self):
        f = self.niveau_label.font()
        f.setPointSize(20)
        f.setBold(True)
        self.niveau_label.setFont(f)
        self.niveau_label.setStyleSheet("color: #87CEFA;")

    # BARRE DU HAUT
    def init_top_bar(self):
        self.barre_haut = QWidget()
        self.barre_haut.setMaximumHeight(40)
        self.barre_haut.setStyleSheet("background-color: #5D4482;")

        layout = QHBoxLayout(self.barre_haut)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Message
        self.message_label = QLabel("L'équipe Scrypt vous souhaite une bonne partie !")
        font = self.message_label.font()
        font.setPointSize(18)
        font.setBold(True)
        self.message_label.setFont(font)
        self.message_label.setStyleSheet("color: white;")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)
        layout.addStretch(1)

        # Boutons
        self.btn_pause = QPushButton("Pause")
        self.btn_recommencer = QPushButton("Recommencer")
        self.btn_quitter = QPushButton("Quitter")

        self.btn_pause.clicked.connect(self.toggle_pause)
        self.btn_recommencer.clicked.connect(self.recommencer_jeu)
        self.btn_quitter.clicked.connect(self.retour_menu)

        for btn, css in zip(
            [self.btn_pause, self.btn_recommencer, self.btn_quitter],
            [
                """QPushButton { background-color: rgba(80,150,255,140); color:white;
                border-radius:10px; padding:8px 16px; font-size:16px; font-weight:bold; }
                QPushButton:hover { background-color:#C5A6F0; }""",
                """QPushButton { background-color:#5BC074; color:white; border-radius:10px;
                padding:8px 16px; font-size:16px; font-weight:bold; }
                QPushButton:hover { background-color:#79D890; }""",
                """QPushButton { background-color:#E85757; color:white; border-radius:10px;
                padding:8px 16px; font-size:16px; font-weight:bold; }
                QPushButton:hover { background-color:#FF6F6F; }"""
            ]
        ):
            btn.setStyleSheet(css)
            btn.setFocusPolicy(Qt.NoFocus)
            layout.addWidget(btn)

    # WIDGETS CENTRAUX
    def init_central_widgets(self):

        # Stats
        self.label_stats = QLabel("Stats")
        font = self.label_stats.font()
        font.setPointSize(24)
        font.setBold(True)
        self.label_stats.setFont(font)
        self.label_stats.setAlignment(Qt.AlignCenter)
        self.label_stats.setStyleSheet("color: #A3C1DA;")

        # Message défilant
        self.label_message = MarqueeLabel("Rien à signaler")
        self.label_message.setFixedHeight(40)

        # Carte
        self.widget_carte = GameWidget()
        self.widget_carte.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.meteo_manager = self.widget_carte.meteo_manager

        # Landing view
        self.landing_view = LandingView()
        self.landing_view.landing_crash_callback = self.on_plane_crash
        self.landing_view.landing_game_over_callback = self.show_game_over

        # Carte group box
        self.carte_box = QGroupBox()
        self.carte_box.setFlat(True)
        self.carte_box.setStyleSheet("QGroupBox { border: none; }")

        layout_carte = QVBoxLayout()
        layout_carte.setContentsMargins(0, 0, 0, 0)
        layout_carte.addWidget(self.widget_carte)
        self.carte_box.setLayout(layout_carte)

        # Liste avions
        self.liste_avions = QListWidget()
        self.liste_avions.setFocusPolicy(Qt.NoFocus)
        self.liste_avions.setStyleSheet("""
            QListWidget::item:selected { background-color:#88C0D0; color:black; }
            QListWidget::item:hover { background-color:#A3D0E0; }
        """)

        self.group_avions = QGroupBox("Avions")
        lay_avions = QVBoxLayout()
        lay_avions.addWidget(self.liste_avions)
        self.group_avions.setLayout(lay_avions)

        style_layout_avions(self.group_avions, self.liste_avions, max_height=400)
        style_layout_stats(self.label_stats, self.score_label, self.niveau_label, self.group_avions)

    # CONTROLES AVION
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

        self.all_buttons = [
            self.btn_monter, self.btn_descendre, self.btn_gauche, self.btn_droite,
            self.btn_atterrir, self.btn_attente, self.btn_urgence,
            self.btn_accelerer, self.btn_ralentir
        ]
        for b in self.all_buttons:
            b.setFixedHeight(60)
            b.setFocusPolicy(Qt.NoFocus)

        # Connexions carte
        self.btn_monter.clicked.connect(self.widget_carte.monter_selected)
        self.btn_descendre.clicked.connect(self.widget_carte.descendre_selected)
        self.btn_gauche.clicked.connect(self.widget_carte.gauche_selected)
        self.btn_droite.clicked.connect(self.widget_carte.droite_selected)
        self.btn_accelerer.clicked.connect(self.widget_carte.accelerer_selected)
        self.btn_ralentir.clicked.connect(self.widget_carte.ralentir_selected)
        self.btn_urgence.clicked.connect(self.widget_carte.urgence_selected)
        self.btn_attente.clicked.connect(self.widget_carte.attente_selected)
        self.btn_atterrir.clicked.connect(self.on_atterrir_clicked)

        # Connexions landing view
        self.btn_monter.clicked.connect(lambda: self.landing_view.move_ground_plane(dy=-10))
        self.btn_descendre.clicked.connect(lambda: self.landing_view.move_ground_plane(dy=10))
        self.btn_gauche.clicked.connect(lambda: self.landing_view.move_ground_plane(dx=-10))
        self.btn_droite.clicked.connect(lambda: self.landing_view.move_ground_plane(dx=10))

        # Label avion
        self.label_nom_avion = ContouredLabel("Sélectionner un avion")
        f = self.label_nom_avion.font()
        f.setPointSize(18)
        f.setBold(True)
        self.label_nom_avion.setFont(f)

        # Boussole
        self.compass = ContouredCompass()

        # Layout avion top
        lay_avion_top = QHBoxLayout()
        lay_avion_top.addWidget(self.label_nom_avion, 1)
        lay_avion_top.addWidget(self.compass, 0)

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

        self.update_progress_bar_spectrum(
            self.bar_altitude, 0, 12000, [(80,0,120),(120,200,255)]
        )
        self.update_progress_bar_spectrum(
            self.bar_vitesse, 0, 900,
            [(128,0,128),(0,0,255),(0,255,0),(255,255,0),(255,128,0),(255,0,0)]
        )
        self.update_progress_bar_spectrum(
            self.bar_fuel, 0, 100, [(255,0,0),(255,255,0)]
        )

        # Grouper
        self.group_controles = QGroupBox("Contrôles")
        lay_ctrl = QVBoxLayout()
        lay_ctrl.addLayout(lay_avion_top)
        lay_ctrl.addWidget(self.bar_altitude)
        lay_ctrl.addWidget(self.bar_vitesse)
        lay_ctrl.addWidget(self.bar_fuel)

        lay_urg = QHBoxLayout()
        lay_urg.addWidget(self.btn_urgence)
        lay_urg.addWidget(self.btn_attente)

        lay_ctrl.addLayout(lay_urg)
        lay_ctrl.addWidget(self.btn_atterrir)
        self.group_controles.setLayout(lay_ctrl)

    # INSTRUCTIONS
    def init_instructions(self):

        self.group_instructions = QGroupBox("Instructions")
        lay = QVBoxLayout()
        lay.setContentsMargins(0,0,0,0)

        lay.addWidget(self.btn_monter)
        lay.addWidget(self.btn_descendre)
        lay_lr = QHBoxLayout()
        lay_lr.addWidget(self.btn_gauche)
        lay_lr.addWidget(self.btn_droite)
        lay.addLayout(lay_lr)

        lay.addWidget(self.btn_accelerer)
        lay.addWidget(self.btn_ralentir)

        self.group_instructions.setLayout(lay)
        style_layout_instructions(self.group_instructions, max_height=400)

    # LAYOUT PRINCIPAL
    def init_main_layout(self):

        # Colonnes
        col_gauche = QVBoxLayout()
        col_gauche.addWidget(self.group_controles, 1)
        col_gauche.addWidget(self.group_instructions, 1)

        col_centre = QVBoxLayout()
        col_centre.addWidget(self.carte_box, 5)
        col_centre.addWidget(self.label_message, 1)
        col_centre.addWidget(self.landing_view, 5)

        col_droite = QVBoxLayout()
        col_droite.addWidget(self.label_stats)
        col_droite.addWidget(self.score_label)
        col_droite.addWidget(self.niveau_label)
        col_droite.addWidget(self.group_avions, 1)

        zone_jeu = QHBoxLayout()
        zone_jeu.addLayout(col_droite, 1)
        zone_jeu.addLayout(col_centre, 2)
        zone_jeu.addLayout(col_gauche, 1)

        layout_global = QVBoxLayout()
        layout_global.addWidget(self.barre_haut)
        layout_global.addLayout(zone_jeu)

        w = QWidget()
        w.setLayout(layout_global)
        self.setCentralWidget(w)

    # CONNEXIONS
    def init_connections(self):
        self.liste_avions.currentItemChanged.connect(self.on_liste_avion_selected)
        self.widget_carte.avion_selectionne_changed.connect(self.on_carte_avion_selected)
        self.widget_carte.avion_updated.connect(self.update_plane_list_item)

    # MUSIQUE
    def init_music(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource("Musiques/Musique_jeu.mp3")
        self.player.setLoops(QMediaPlayer.Infinite)
        self.player.play()

    # PAUSE
    def toggle_pause(self):
        self.paused = not self.paused

        # Musique
        self.player.pause() if self.paused else self.player.play()

        # Mode normal
        if not self.control_ground_mode:
            self.widget_carte.set_paused(self.paused)
            CollisionManager.paused = self.paused
            if hasattr(self.meteo_manager, "set_paused"):
                self.meteo_manager.set_paused(self.paused)

        # Landing view
        self.landing_view.global_paused = self.paused

        self.btn_pause.setText("Reprendre" if self.paused else "Pause")

    # PROGRESS BARS COULEURS
    def update_progress_bar_spectrum(self, bar, value, maximum, spectrum):
        value = max(0, min(value, maximum))
        bar.setMaximum(maximum)
        bar.setValue(value)

        t = value / maximum
        n = len(spectrum) - 1
        idx = min(int(t * n), n - 1)
        t_local = (t * n) - idx

        r = int(spectrum[idx][0] + (spectrum[idx+1][0] - spectrum[idx][0]) * t_local)
        g = int(spectrum[idx][1] + (spectrum[idx+1][1] - spectrum[idx][1]) * t_local)
        b = int(spectrum[idx][2] + (spectrum[idx+1][2] - spectrum[idx][2]) * t_local)

        bar.setStyleSheet(f"""
        QProgressBar {{
            border:2px solid #444; border-radius:10px;
            background:#222; text-align:center;
            font-size:18px; font-weight:bold; color:white;
        }}
        QProgressBar::chunk {{
            border-radius:10px; margin:2px;
            background-color:rgb({r},{g},{b});
        }}
        """)

    # UPDATE LISTE AVION
    def update_plane_list_item(self, plane):
        # Si avion supprimé
        if plane not in self.widget_carte.planes:
            self.suppress_auto_selection = True
            self.liste_avions.blockSignals(True)
            try:
                self.liste_avions.clearSelection()
                try: self.liste_avions.setCurrentItem(None)
                except: pass

                for i in range(self.liste_avions.count()-1, -1, -1):
                    item = self.liste_avions.item(i)
                    if item.data(Qt.UserRole) == plane:
                        self.liste_avions.takeItem(i)
                        break
            finally:
                self.liste_avions.blockSignals(False)

            # Nettoyage UI
            self.widget_carte.selected_plane = None
            self.landing_view.set_selected_plane(None)
            self.label_nom_avion.setText("Sélectionner un avion")
            self.bar_altitude.setValue(0)
            self.bar_vitesse.setValue(0)
            self.bar_fuel.setValue(0)
            try: self.compass.set_cap(0)
            except: pass

            self.update_stats()
            QTimer.singleShot(50, lambda: setattr(self, "suppress_auto_selection", False))
            return

        # Mise à jour texte
        for i in range(self.liste_avions.count()):
            item = self.liste_avions.item(i)
            if item.data(Qt.UserRole) == plane:
                item.setText(
                    f"{plane.avion.nom} - Alt: {plane.avion.altitude} m - "
                    f"Vit: {plane.avion.vitesse} km/h - Fuel: {plane.avion.fuel:.1f}% - "
                    f"Cap: {plane.avion.cap:.1f}°"
                )
                break
        else:
            item = QListWidgetItem(
                f"{plane.avion.nom} - Alt: {plane.avion.altitude} m - "
                f"Vit: {plane.avion.vitesse} km/h - Fuel: {plane.avion.fuel:.1f}% - "
                f"Cap: {plane.avion.cap:.1f}°"
            )
            item.setData(Qt.UserRole, plane)
            self.liste_avions.addItem(item)

        # Si avion sélectionné → update progress bars
        if plane is self.widget_carte.selected_plane:
            self.update_progress_bar_spectrum(self.bar_altitude, plane.avion.altitude, 12000,
                                              [(80,0,120),(120,200,255)])
            self.update_progress_bar_spectrum(self.bar_vitesse, plane.avion.vitesse, 900,
                                              [(128,0,128),(0,0,255),(0,255,0),
                                               (255,255,0),(255,128,0),(255,0,0)])
            self.update_progress_bar_spectrum(self.bar_fuel, plane.avion.fuel, 100,
                                              [(255,0,0),(255,255,0)])
            try: self.compass.set_cap(plane.avion.cap)
            except: pass

        self.update_stats()

    # SELECTION LISTE → AVION
    def on_liste_avion_selected(self, current, previous):
        if self.suppress_auto_selection and current is None:
            return
        if not current:
            return

        plane = current.data(Qt.UserRole)
        self.widget_carte.selected_plane = plane
        self.landing_view.set_selected_plane(plane)
        self.widget_carte.update()

        self.label_nom_avion.setText(plane.avion.nom)
        try: self.compass.set_cap(plane.avion.cap)
        except: pass

        self.update_plane_list_item(plane)

    # SELECTION CARTE → AVION
    def on_carte_avion_selected(self, avion):
        if self.suppress_auto_selection:
            return

        if avion is None:
            self.label_nom_avion.setText("Sélectionner un avion")
            self.bar_altitude.setValue(0)
            self.bar_vitesse.setValue(0)
            self.bar_fuel.setValue(0)
            self.landing_view.set_selected_plane(None)
            try: self.compass.set_cap(0)
            except: pass
            return

        self.label_nom_avion.setText(avion.nom)
        self.update_plane_list_item(avion)
        self.landing_view.set_selected_plane(avion)

        try: self.compass.set_cap(avion.cap)
        except: pass

        for i in range(self.liste_avions.count()):
            item = self.liste_avions.item(i)
            if item.data(Qt.UserRole).avion == avion:
                self.liste_avions.setCurrentItem(item)
                break

    # ATTERRIR
    def on_atterrir_clicked(self):
        plane = self.widget_carte.selected_plane
        if not plane:
            return

        # Activation piste
        self.landing_view.activate_ground_plane(None)
        self.control_ground_mode = True

        # UI avion au sol
        self.label_nom_avion.setText("Avion au sol")
        self.bar_altitude.setValue(0)
        self.bar_vitesse.setValue(0)
        self.bar_fuel.setValue(0)
        try: self.compass.set_cap(0)
        except: pass

        # Suppression sélection
        self.suppress_auto_selection = True
        self.liste_avions.blockSignals(True)

        try:
            self.liste_avions.clearSelection()
            try: self.liste_avions.setCurrentItem(None)
            except: pass

            self.widget_carte.selected_plane = None
            try: self.widget_carte.remove_plane(plane)
            except:
                if plane in self.widget_carte.planes:
                    self.widget_carte.planes.remove(plane)
                    try: self.widget_carte.avion_updated.emit(plane)
                    except: pass

            self.widget_carte.update()
            QApplication.processEvents()

            try: self.widget_carte.avion_selectionne_changed.emit(None)
            except: pass
        finally:
            self.liste_avions.blockSignals(False)

        # Pause globale
        self.widget_carte.set_paused(True)
        CollisionManager.paused = True
        if hasattr(self.meteo_manager, "set_paused"):
            self.meteo_manager.set_paused(True)

        self.landing_view.setFocus(Qt.FocusReason.ActiveWindowFocusReason)

        QTimer.singleShot(50, lambda: setattr(self, "suppress_auto_selection", False))

        self.landing_view.landing_finished_callback = self.on_landing_finished

    # FIN ATTERRISSAGE
    def on_landing_finished(self):
        self.control_ground_mode = False
        self.paused = False
        self.widget_carte.set_paused(False)
        CollisionManager.paused = False
        if hasattr(self.meteo_manager, "set_paused"):
            self.meteo_manager.set_paused(False)

    # METEO
    def mettre_a_jour_message_defilant(self):
        if len(self.meteo_manager.evenements_actifs) > 0:
            self.label_message.setText("ATTENTION : Conditions météo dangereuses détectées !")
        else:
            self.label_message.setText("Rien à signaler")

    # TOUCHES CLAVIER
    def keyPressEvent(self, event):

        # Mode atterrissage
        if self.control_ground_mode:
            if event.key() == Qt.Key_Up: self.landing_view.move_ground_plane(dy=-10)
            elif event.key() == Qt.Key_Down: self.landing_view.move_ground_plane(dy=10)
            elif event.key() == Qt.Key_Left: self.landing_view.move_ground_plane(dx=-10)
            elif event.key() == Qt.Key_Right: self.landing_view.move_ground_plane(dx=10)
            return

        # Mode vol
        plane = self.widget_carte.selected_plane
        if plane is None:
            return

        if event.key() == Qt.Key_Left:
            plane.avion.gauche()
            self.widget_carte._update_velocity_from_cap(plane)

        elif event.key() == Qt.Key_Right:
            plane.avion.droite()
            self.widget_carte._update_velocity_from_cap(plane)

        elif event.key() == Qt.Key_Up:
            plane.avion.monter()

        elif event.key() == Qt.Key_Down:
            plane.avion.descendre()

        self.widget_carte.update_plane_position(plane)
        self.update_plane_list_item(plane)

    # STATS
    def update_stats(self):
        nb = len(self.widget_carte.planes)
        self.label_stats.setText(f"Avions présents : {nb}")

    # SCORE
    def update_score(self):
        if self.paused or self.control_ground_mode:
            return
        self.score += 10
        self.score_label.setText(f"Score : {self.score}")
        self.level_manager.calcul_niveau()

    # Crash avion
    def on_plane_crash(self):
        self.score -= 200
        self.score_label.setText(f"Score : {self.score}")
        if self.score <= 0:
            self.show_game_over()

    # GAME OVER
    def show_game_over(self):
        game_over = GameOverWidget(
            self,
            restart_callback=self.recommencer_jeu,
            quit_callback=self.retour_menu
        )
        game_over.setGeometry(self.geometry())
        game_over.show()

        self.paused = True
        self.widget_carte.set_paused(True)
        CollisionManager.paused = True
        if hasattr(self.meteo_manager, "set_paused"):
            self.meteo_manager.set_paused(True)

    # RECOMMENCER JEU
    def recommencer_jeu(self):

        # Sauvegarde musique
        player_actuel = self.player
        audio_output = self.audio_output

        # Nouvelle fenêtre
        nouvelle = MainGameWindow()

        # Injection musique
        nouvelle.player = player_actuel
        nouvelle.audio_output = audio_output
        player_actuel.setParent(nouvelle)
        player_actuel.play()

        nouvelle.showFullScreen()
        self.close()

    # RETOUR MENU
    def retour_menu(self):
        if self.player:
            self.player.stop()
        from Accueil import Window
        self.menu = Window()
        self.menu.showFullScreen()
        self.close()


# MAIN
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGameWindow()
    window.show()
    sys.exit(app.exec())