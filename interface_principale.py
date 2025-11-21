import sys
import Avions
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QFrame, QGroupBox
)
from PySide6.QtCore import Qt
from liste_avions_hélicos_test import ListeAvionsHelis

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SkyLink")
        self.showFullScreen()


        # Labels
        label_stats = QLabel("Stats"); label_stats.setFrameShape(QFrame.Panel)
        label_vue = QLabel("Vue de haut"); label_vue.setFrameShape(QFrame.Panel)
        label_message = QLabel("Message"); label_message.setFrameShape(QFrame.Panel)
        label_piste = QLabel("Piste de côté"); label_piste.setFrameShape(QFrame.Panel)
        label_controles = QLabel("Contrôles"); label_controles.setFrameShape(QFrame.Panel)
        label_instr = QLabel("Instructions"); label_instr.setFrameShape(QFrame.Panel)
        label_actions = QLabel("Actions"); label_actions.setFrameShape(QFrame.Panel)


        # Boutons
        btn_monter = QPushButton("Monter")
        btn_descendre = QPushButton("Descendre")
        btn_gauche = QPushButton("Gauche")
        btn_droite = QPushButton("Droite")
        btn_atterrir = QPushButton("Atterrir")

        # Même taille pour cohérence
        for b in [btn_monter, btn_descendre, btn_gauche, btn_droite, btn_atterrir]:
            b.setFixedHeight(60)

        # GROUPBOX instructions/action
        group_instructions = QGroupBox("Instructions")
        layout_instructions = QVBoxLayout()
        layout_instructions.addWidget(btn_monter)
        layout_instructions.addWidget(btn_descendre)
        group_instructions.setLayout(layout_instructions)

        group_actions = QGroupBox("Actions")
        layout_actions = QVBoxLayout()
        layout_actions.addWidget(btn_gauche)
        layout_actions.addWidget(btn_droite)
        group_actions.setLayout(layout_actions)

        group_controles = QGroupBox("Contrôles")
        layout_controles = QVBoxLayout()
        group_controles.setLayout(layout_controles)


        # Données avions/hélicos
        avions_data = [
            {"nom": "JKL101", "alt": 3800, "vit": 440, "fuel": 80},
            {"nom": "MNO112", "alt": 3900, "vit": 450, "fuel": 90},
        ]
        helis_data = [
            {"nom": "H001", "alt": 1200, "vit": 200, "fuel": 50},
            {"nom": "H002", "alt": 1250, "vit": 210, "fuel": 55},
            {"nom": "H003", "alt": 1300, "vit": 220, "fuel": 60},
        ]
        widget_avions_helicos = ListeAvionsHelis(avions=avions_data, helis=helis_data)


        # Layouts colonnes
        layout_gauche = QVBoxLayout()
        layout_gauche.addWidget(group_controles)
        layout_gauche.addWidget(group_instructions)
        layout_gauche.addWidget(group_actions)

        layout_centre = QVBoxLayout()
        layout_centre.addWidget(label_vue, 5)
        layout_centre.addWidget(label_message, 1)
        layout_centre.addWidget(label_piste, 5)

        layout_droite = QVBoxLayout()
        layout_droite.addWidget(label_stats)
        layout_droite.addWidget(widget_avions_helicos, 0, Qt.AlignTop)


        # Layout horizontal principal
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
        font = message_label.font(); font.setPointSize(18); font.setBold(True)
        message_label.setFont(font)
        message_label.setStyleSheet("color: white;")
        layout_barre.addWidget(message_label)
        layout_barre.addStretch(1)

        btn_pause = QPushButton("Pause")
        btn_recommencer = QPushButton("Recommencer")
        btn_quitter = QPushButton("Quitter")
        layout_barre.addWidget(btn_pause)
        layout_barre.addWidget(btn_recommencer)
        layout_barre.addWidget(btn_quitter)


        # Layout global
        layout_global = QVBoxLayout()
        layout_global.addWidget(barre_haut)
        layout_global.addLayout(layout_zone_jeu)

        central_widget = QWidget()
        central_widget.setLayout(layout_global)
        self.setCentralWidget(central_widget)


# Exécution
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()