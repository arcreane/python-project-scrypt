import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QGroupBox, QSizePolicy, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from Carte import GameWidget
from message_defilant import MarqueeLabel


class MainGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SkyLink")
        self.showFullScreen()
        self.menu_window = None

        # ---------- Bande du haut ----------
        barre_haut = QWidget()
        barre_haut.setMaximumHeight(40)
        barre_haut.setStyleSheet("background-color: #5D4482;")
        layout_barre = QHBoxLayout(barre_haut)
        layout_barre.setContentsMargins(5, 5, 5, 5)

        self.message_label = QLabel("L'équipe Scrypt vous souhaite une bonne partie !")
        self.message_label.setAlignment(Qt.AlignCenter)
        font = self.message_label.font()
        font.setPointSize(18)
        font.setBold(True)
        self.message_label.setFont(font)
        self.message_label.setStyleSheet("color: white;")
        layout_barre.addWidget(self.message_label)
        layout_barre.addStretch(1)

        btn_pause = QPushButton("Pause")
        btn_recommencer = QPushButton("Recommencer")
        btn_quitter = QPushButton("Quitter")
        btn_quitter.clicked.connect(self.close)
        layout_barre.addWidget(btn_pause)
        layout_barre.addWidget(btn_recommencer)
        layout_barre.addWidget(btn_quitter)

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
        carte_box = QGroupBox("Carte")
        layout_carte = QVBoxLayout()
        layout_carte.setContentsMargins(0, 0, 0, 0)
        layout_carte.setSpacing(0)
        self.widget_carte = GameWidget()
        self.widget_carte.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout_carte.addWidget(self.widget_carte)
        carte_box.setLayout(layout_carte)

        # ---------- Liste des avions ----------
        self.liste_avions = QListWidget()
        self.liste_avions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.liste_avions.setAlternatingRowColors(True)

        self.liste_avions.setStyleSheet("""
        QListWidget::item:selected {
            background-color: #88C0D0;
            color: black;
        }
        QListWidget::item:hover {
            background-color: #A3D0E0;
        }
        """)

        group_avions = QGroupBox("Avions")
        layout_avions = QVBoxLayout()
        layout_avions.addWidget(self.liste_avions)
        group_avions.setLayout(layout_avions)

        # Musique d'ambiance
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("musique_de_fond_interface_principale.mp3"))
        self.player.setLoops(QMediaPlayer.Infinite)
        self.player.play()

        # Connecter sélection liste <-> carte
        self.liste_avions.currentItemChanged.connect(self.on_liste_avion_selected)
        self.widget_carte.avion_selectionne_changed.connect(self.on_carte_avion_selected)

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

        btn_monter.clicked.connect(self.widget_carte.monter_selected)
        btn_descendre.clicked.connect(self.widget_carte.descendre_selected)
        btn_gauche.clicked.connect(self.widget_carte.gauche_selected)
        btn_droite.clicked.connect(self.widget_carte.droite_selected)

        group_controles = QGroupBox("Contrôles")
        layout_controles = QVBoxLayout()
        layout_controles.addStretch(1)
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

        # Barre du haut
        barre_haut = QWidget()
        barre_haut.setMaximumHeight(40)
        barre_haut.setStyleSheet("background-color: #5D4482;")
        layout_barre = QHBoxLayout(barre_haut)
        layout_barre.setContentsMargins(5, 5, 5, 5)
        layout_barre.setSpacing(5)

        message_label = QLabel("L'équipe Scrypt vous souhaite une bonne partie !")
        message_label.setAlignment(Qt.AlignCenter)
        font = message_label.font();
        font.setPointSize(18);
        font.setBold(True)
        message_label.setFont(font)
        message_label.setStyleSheet("color: white;")
        layout_barre.addWidget(message_label)
        layout_barre.addStretch(1)

        btn_pause = QPushButton("Pause")
        btn_recommencer = QPushButton("Recommencer")
        btn_quitter = QPushButton("Quitter")
        btn_quitter.clicked.connect(self.retour_menu)
        layout_barre.addWidget(btn_pause)
        layout_barre.addWidget(btn_recommencer)
        layout_barre.addWidget(btn_quitter)

        # Bouton Pause
        btn_pause.setStyleSheet("""
                     QPushButton {
                         background-color: rgba(80, 150, 255, 140); 
                         color: white;
                         border-radius: 10px;
                         padding: 8px 16px;
                         font-size: 16px;               /* taille uniforme */
                         font-family: 'Comic Sans MS';  /* police uniforme */
                         font-weight: bold;
                     }
                     QPushButton:hover {
                         background-color: #C5A6F0;
                     }
                 """)

        # Bouton Recommencer
        btn_recommencer.setStyleSheet("""
                     QPushButton {
                         background-color: #5BC074;
                         color: white;
                         border-radius: 10px;
                         padding: 8px 16px;
                         font-size: 16px;
                         font-family: 'Comic Sans MS';
                         font-weight: bold;
                     }
                     QPushButton:hover {
                         background-color: #79D890;
                     }
                 """)

        # Bouton Quitter
        btn_quitter.setStyleSheet("""
                     QPushButton {
                         background-color: #E85757;
                         color: white;
                         border-radius: 10px;
                         padding: 8px 16px;
                         font-size: 16px;
                         font-family: 'Comic Sans MS';
                         font-weight: bold;
                     }
                     QPushButton:hover {
                         background-color: #FF6F6F;
                     }
                 """)

        # Layout global
        layout_global = QVBoxLayout()
        layout_global.addWidget(barre_haut)
        layout_global.addLayout(layout_zone_jeu)

        central_widget = QWidget()
        central_widget.setLayout(layout_global)
        self.setCentralWidget(central_widget)

        # ---------- Timer de mise à jour liste ----------
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_plane_list)
        self.update_timer.start(1000)  # toutes les secondes

    # ---------- Retour au menu ----------
    def retour_menu(self):
        if self.player:
            self.player.stop()
        from interface import Window
        self.menu_window = Window()
        self.menu_window.showFullScreen()
        self.close()

    # ---------- Mise à jour de la liste ----------
    def update_plane_list(self):
        current_plane = None
        current_item = self.liste_avions.currentItem()
        if current_item:
            current_plane = current_item.data(Qt.UserRole)

        self.liste_avions.clear()
        for p in self.widget_carte.planes:
            item = QListWidgetItem(
                f"{p.avion.nom} - Alt: {p.avion.altitude} m - Vit: {p.avion.vitesse} km/h - "
                f"Fuel: {p.avion.fuel:.1f}% - Cap: {p.avion.cap:.1f}°"
            )
            item.setData(Qt.UserRole, p)
            self.liste_avions.addItem(item)

            # Restaurer la sélection si c'était le même avion
            if current_plane == p:
                self.liste_avions.setCurrentItem(item)

    # ---------- Sélection liste -> carte ----------
    def on_liste_avion_selected(self, current, previous):
        if current:
            plane = current.data(Qt.UserRole)
            self.widget_carte.selected_plane = plane
            self.widget_carte.update()

    # ---------- Sélection carte -> liste ----------
    def on_carte_avion_selected(self, avion):
        for i in range(self.liste_avions.count()):
            item = self.liste_avions.item(i)
            if item.data(Qt.UserRole).avion == avion:
                self.liste_avions.setCurrentItem(item)
                return
        self.liste_avions.setCurrentItem(None)


# ---------- Exécution ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGameWindow()
    window.show()
    sys.exit(app.exec())
