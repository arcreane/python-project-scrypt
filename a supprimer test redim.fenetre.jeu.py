import sys
import Avions
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFrame
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SkyLink")
        self.showFullScreen()

        # ----- Création des labels -----
        label_stats = QLabel("Stats")
        label_stats.setFrameShape(QFrame.Panel)

        label_avions = QLabel("Avions")
        label_avions.setFrameShape(QFrame.Panel)

        label_vue = QLabel("Vue de haut")
        label_vue.setFrameShape(QFrame.Panel)

        label_message = QLabel("Message")
        label_message.setFrameShape(QFrame.Panel)

        label_piste = QLabel("Piste de côté")
        label_piste.setFrameShape(QFrame.Panel)

        label_controles = QLabel("Contrôles")
        label_controles.setFrameShape(QFrame.Panel)

        label_instr = QLabel("Instructions")
        label_instr.setFrameShape(QFrame.Panel)

        label_actions = QLabel("Actions")
        label_actions.setFrameShape(QFrame.Panel)

        # Infos de l'avion
        avion = Avions.Avions("ABC123", 3500, 400, 50, 90)
        av_nom = QLabel(avion.nom)
        av_alt = QLabel(str(avion.altitude))
        av_vit = QLabel(str(avion.vitesse))
        av_fuel = QLabel(str(avion.fuel))
        av_cap = QLabel(str(avion.cap))

        # ----- Layouts colonnes -----
        layout_gauche = QVBoxLayout()
        layout_gauche.addWidget(label_controles)
        layout_gauche.addWidget(label_instr)
        layout_gauche.addWidget(label_actions)

        layout_centre = QVBoxLayout()
        layout_centre.addWidget(label_vue,5)
        layout_centre.addWidget(label_message,1)
        layout_centre.addWidget(label_piste,5)


        layout_avions = QVBoxLayout()
        layout_avions.addWidget(label_avions)
        layout_avions.addWidget(av_nom)
        layout_avions.addWidget(av_alt)
        layout_avions.addWidget(av_vit)
        layout_avions.addWidget(av_fuel)
        layout_avions.addWidget(av_cap)

        layout_droite = QVBoxLayout()
        layout_droite.addWidget(label_stats)
        layout_droite.addLayout(layout_avions)

        #Layout horizontal principal (zone de jeu)
        layout_zone_jeu = QHBoxLayout()
        layout_zone_jeu.addLayout(layout_droite, 1)   # colonne gauche plus petite
        layout_zone_jeu.addLayout(layout_centre, 2)   # colonne centrale plus grande
        layout_zone_jeu.addLayout(layout_gauche, 1)   # colonne droite plus petite

        #Barre du haut
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
        message_label.setStyleSheet("color: white;")  # texte blanc
        layout_barre.addWidget(message_label)
        layout_barre.addStretch(1)

        btn_pause = QPushButton("Pause")
        btn_recommencer = QPushButton("Recommencer")
        btn_quitter = QPushButton("Quitter")

        layout_barre.addWidget(btn_pause)
        layout_barre.addWidget(btn_recommencer)
        layout_barre.addWidget(btn_quitter)

        #Layout global
        layout_global = QVBoxLayout()
        layout_global.addWidget(barre_haut)
        layout_global.addLayout(layout_zone_jeu)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout_global)
        self.setCentralWidget(central_widget)

#Exécution
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
