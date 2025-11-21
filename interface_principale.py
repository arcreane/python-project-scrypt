# Main.py
import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QGroupBox, QSizePolicy, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QTimer
from Carte import GameWidget
from Avions import Avions
from message_defilant import MarqueeLabel


class MainGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SkyLink")
        self.showFullScreen()

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

        # Style pour surlignage plus clair
        self.liste_avions.setStyleSheet("""
        QListWidget::item:selected {
            background-color: #88C0D0;
            color: black;
        }
        QListWidget::item:hover {
            background-color: #A3D0E0;
        }
        """)

        # Encapsuler dans un GroupBox pour la bordure
        group_avions = QGroupBox("Avions")
        layout_avions = QVBoxLayout()
        layout_avions.addWidget(self.liste_avions)
        group_avions.setLayout(layout_avions)

        # Connecter sélection dans la liste à la carte
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

        # Connecter boutons à GameWidget
        btn_monter.clicked.connect(self.widget_carte.monter_selected)
        btn_descendre.clicked.connect(self.widget_carte.descendre_selected)
        btn_gauche.clicked.connect(self.widget_carte.gauche_selected)
        btn_droite.clicked.connect(self.widget_carte.droite_selected)

        # GroupBox Contrôles
        group_controles = QGroupBox("Contrôles")
        layout_controles = QVBoxLayout()
        layout_controles.addStretch(1)
        layout_controles.addWidget(btn_urgence)
        layout_controles.addWidget(btn_attente)
        layout_controles.addWidget(btn_atterrir)
        group_controles.setLayout(layout_controles)

        # GroupBox Instructions
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

        # Mettre à jour la liste des avions toutes les secondes
        self.update_plane_list()

    # ---------- Gestion liste <-> carte ----------
    def update_plane_list(self):
        self.liste_avions.clear()
        for p in self.widget_carte.planes:
            item = QListWidgetItem(
                f"{p.avion.nom} - Alt: {p.avion.altitude} m - Vit: {p.avion.vitesse} km/h - "
                f"Fuel: {p.avion.fuel:.1f}% - Cap: {p.avion.cap}°"
            )
            item.setData(Qt.UserRole, p)
            self.liste_avions.addItem(item)
        QTimer.singleShot(1000, self.update_plane_list)

    def on_liste_avion_selected(self, current, previous):
        if current:
            plane = current.data(Qt.UserRole)
            self.widget_carte.selected_plane = plane
            self.widget_carte.update()

    def on_carte_avion_selected(self, avion):
        # mettre à jour la sélection dans la liste
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
