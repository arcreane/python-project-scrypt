#Jeu.py
import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QGroupBox, QSizePolicy, QListWidget, QListWidgetItem, QProgressBar,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPalette, QColor
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
from game_level_manager import GameLevelManager



class MainGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.global_paused = False
        self.paused = False
        self.suppress_auto_selection = False

        self.setWindowTitle("SkyLink")
        self.showFullScreen()

        # 1. init top + widgets + controls
        self.init_top_bar()
        self.init_central_widgets()
        self.init_avion_controls()
        self.init_instructions()

        # 2. SCORE ET NIVEAU ICI (très important)
        self.score = 0
        self.score_label = QLabel("Score : 0")
        font_score = self.score_label.font()
        font_score.setPointSize(20)
        font_score.setBold(True)
        self.score_label.setFont(font_score)
        self.score_label.setStyleSheet("color: #FFD700;")

        self.niveau_label = QLabel("Niveau : 1")
        f = self.niveau_label.font()
        f.setPointSize(20)
        f.setBold(True)
        self.niveau_label.setFont(f)
        self.niveau_label.setStyleSheet("color: #87CEFA;")

        # 3. Manager de niveaux (il utilise les labels)
        self.level_manager = GameLevelManager(self)

        # 4. Maintenant que TOUT est prêt → construire le layout
        self.init_main_layout()

        # 5. Suite du code : timer, musique, connexions
        self.score_timer = QTimer()
        self.score_timer.timeout.connect(self.update_score)
        self.score_timer.start(1000)

        self.init_connections()
        self.meteo_manager.evenements_changed.connect(self.mettre_a_jour_message_defilant)
        self.init_music()

        self.update_stats()
        self.level_manager.calcul_niveau()

        # SCORE (doit être ici AVANT init_main_layout)
        self.score = 0
        self.score_label = QLabel("Score : 0")
        font_score = self.score_label.font()
        font_score.setPointSize(20)
        font_score.setBold(True)
        self.score_label.setFont(font_score)
        self.score_label.setStyleSheet("color: #FFD700;")

        # Label Niveau
        self.niveau_label = QLabel("Niveau : 1")
        f = self.niveau_label.font()
        f.setPointSize(20)
        f.setBold(True)
        self.niveau_label.setFont(f)
        self.niveau_label.setStyleSheet("color: #87CEFA;")

        # Manager de niveaux
        self.level_manager = GameLevelManager(self)

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

        self.btn_pause.setFocusPolicy(Qt.NoFocus)
        self.btn_recommencer.setFocusPolicy(Qt.NoFocus)
        self.btn_quitter.setFocusPolicy(Qt.NoFocus)

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

        # Modifier la police pour qu'elle soit plus grosse et en gras
        font_stats = self.label_stats.font()
        font_stats.setPointSize(24)  # taille plus grande
        font_stats.setBold(True)
        self.label_stats.setFont(font_stats)
        self.label_stats.setStyleSheet("color: #A3C1DA;")

        self.label_message = MarqueeLabel("Rien à signaler")  # message défilant
        self.label_message.setFixedHeight(40)

        # Carte et météo
        self.landing_view = LandingView()
        self.landing_view.landing_finished_callback = self.on_landing_finished
        self.widget_carte = GameWidget()
        self.widget_carte.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.meteo_manager = self.widget_carte.meteo_manager

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
        self.liste_avions.setFocusPolicy(Qt.NoFocus)
        self.liste_avions.setAlternatingRowColors(True)
        self.liste_avions.setStyleSheet("""
            QListWidget::item:selected { background-color: #88C0D0; color: black; }
            QListWidget::item:hover { background-color: #A3D0E0; }
        """)

        self.group_avions = QGroupBox("Avions")
        layout_avions = QVBoxLayout()
        layout_avions.addWidget(self.liste_avions)
        self.group_avions.setLayout(layout_avions)

        style_layout_avions(self.group_avions, self.liste_avions, max_height=400)

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
            b.setFocusPolicy(Qt.NoFocus)

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
        self.btn_atterrir.clicked.connect(self.on_atterrir_clicked)

        self.btn_monter.clicked.connect(lambda: self.landing_view.move_ground_plane(dy=-10))
        self.btn_descendre.clicked.connect(lambda: self.landing_view.move_ground_plane(dy=10))
        self.btn_gauche.clicked.connect(lambda: self.landing_view.move_ground_plane(dx=-10))
        self.btn_droite.clicked.connect(lambda: self.landing_view.move_ground_plane(dx=10))

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
        style_layout_instructions(self.group_instructions, max_height=400)

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
        layout_droite.addWidget(self.score_label)
        layout_droite.addWidget(self.niveau_label)
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
        self.paused = not self.paused  # Pause globale

        #Pause musique
        if self.paused:
            self.player.pause()
        else:
            self.player.play()

        # 🔹 Si on n’est pas en mode atterrissage
        if not getattr(self, "control_ground_mode", False):
            self.widget_carte.set_paused(self.paused)
            CollisionManager.paused = self.paused
            if hasattr(self.meteo_manager, 'set_paused'):
                self.meteo_manager.set_paused(self.paused)

        # Pause landing view (toujours respectée)
        self.landing_view.global_paused = self.paused

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
            # On empêche temporairement que la suppression provoque une nouvelle sélection
            self.suppress_auto_selection = True

            # 1) Bloquer les signaux de la QListWidget pour éviter callbacks intempestifs
            self.liste_avions.blockSignals(True)
            try:
                # 2) Désélectionner & forcer l'absence d'item courant
                self.liste_avions.clearSelection()
                try:
                    self.liste_avions.setCurrentItem(None)
                except Exception:
                    pass

                # 3) Supprimer l'item correspondant (itération inverse pour sécurité)
                for i in range(self.liste_avions.count() - 1, -1, -1):
                    item = self.liste_avions.item(i)
                    if item.data(Qt.UserRole) == plane:
                        self.liste_avions.takeItem(i)
                        break
            finally:
                # 4) Réactiver signaux quoi qu'il arrive
                self.liste_avions.blockSignals(False)

            # 5) Forcer l'état "aucune sélection" côté carte / UI
            self.widget_carte.selected_plane = None
            self.landing_view.set_selected_plane(None)
            self.label_nom_avion.setText("Sélectionner un avion")
            self.bar_altitude.setValue(0)
            self.bar_vitesse.setValue(0)
            self.bar_fuel.setValue(0)
            try:
                self.compass.set_cap(0)
            except:
                pass

            self.update_stats()

            # 6) Réinitialiser le flag légèrement plus tard (permet au loop Qt de finir les handlers)
            QTimer.singleShot(50, lambda: setattr(self, "suppress_auto_selection", False))

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

        self.update_stats()

    def on_liste_avion_selected(self, current, previous):
        # Si on bloque la sélection (suppression en cours) ET qu'il s'agit d'une désélection (current is None),
        # on ignore cet événement. Si current n'est pas None (l'utilisateur clique), on accepte la sélection.
        if getattr(self, "suppress_auto_selection", False) and current is None:
            return
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
        if getattr(self, "suppress_auto_selection", False):
            return
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

    def on_atterrir_clicked(self):
        """Gérer l'atterrissage :
        - retirer l'avion sélectionné immédiatement de la carte et de la liste
        - empêcher l'auto-sélection temporairement
        - activer la landing view (piste)
        - mettre la carte en pause (la piste reste active)
        """
        plane = getattr(self.widget_carte, "selected_plane", None)
        if not plane:
            return

        # --- activer d'abord le plan d'atterrissage ---
        self.landing_view.activate_ground_plane("Images/avion_attente.png")
        self.control_ground_mode = True
        self.label_nom_avion.setText("Avion au sol")
        self.bar_altitude.setValue(0)
        self.bar_vitesse.setValue(0)
        self.bar_fuel.setValue(0)
        try:
            self.compass.set_cap(0)
        except Exception:
            pass

        # --- ensuite, empêcher que la suppression provoque une auto-sélection ---
        self.suppress_auto_selection = True
        self.liste_avions.blockSignals(True)
        try:
            self.liste_avions.clearSelection()
            try:
                self.liste_avions.setCurrentItem(None)
            except Exception:
                pass

            self.widget_carte.selected_plane = None
            try:
                self.widget_carte.remove_plane(plane)
            except Exception:
                if plane in self.widget_carte.planes:
                    self.widget_carte.planes.remove(plane)
                    try:
                        self.widget_carte.avion_updated.emit(plane)
                    except Exception:
                        pass

            self.widget_carte.update()
            QApplication.processEvents()

            try:
                self.widget_carte.avion_selectionne_changed.emit(None)
            except Exception:
                pass

        finally:
            self.liste_avions.blockSignals(False)

        self.widget_carte.set_paused(True)
        CollisionManager.paused = True
        if hasattr(self.meteo_manager, 'set_paused'):
            self.meteo_manager.set_paused(True)

        # Forcer le focus clavier sur la landing view
        self.landing_view.setFocus(Qt.FocusReason.ActiveWindowFocusReason)

        QTimer.singleShot(50, lambda: setattr(self, "suppress_auto_selection", False))

    def on_landing_finished(self):
        """Reprendre le jeu après que l'avion ait fini l'atterrissage"""
        self.control_ground_mode = False
        self.paused = False
        self.widget_carte.set_paused(False)
        CollisionManager.paused = False
        if hasattr(self.meteo_manager, 'set_paused'):
            self.meteo_manager.set_paused(False)

    def mettre_a_jour_message_defilant(self):
        if len(self.meteo_manager.evenements_actifs) > 0:
            self.label_message.setText("ATTENTION : Conditions météo dangereuses détectées !")
        else:
            self.label_message.setText("Rien à signaler")

    def keyPressEvent(self, event):
        # 🔹 si on est en mode ground plane (atterrissage), gérer la piste
        if getattr(self, "control_ground_mode", False):
            if event.key() == Qt.Key_Up:
                self.landing_view.move_ground_plane(dy=-10)
            elif event.key() == Qt.Key_Down:
                self.landing_view.move_ground_plane(dy=10)
            elif event.key() == Qt.Key_Left:
                self.landing_view.move_ground_plane(dx=-10)
            elif event.key() == Qt.Key_Right:
                self.landing_view.move_ground_plane(dx=10)
            return

        # sinon, contrôle avion normal
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

    def update_stats(self):
        nb = len(self.widget_carte.planes)
        self.label_stats.setText(f"Avions présents : {nb}")

    def update_score(self):
        if self.paused or getattr(self, "control_ground_mode", False):
            return  # pas de points pendant pause ou atterrissage

        self.score += 10
        self.score_label.setText(f"Score : {self.score}")

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
