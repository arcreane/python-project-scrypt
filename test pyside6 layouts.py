import sys
import Avions

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFrame,
    QPushButton,
    QGroupBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SkyLink")
        self.setFixedSize(QSize(1500, 800))

        label = QLabel("Stats")
        label.setFrameShape(QFrame.Panel)
        label2 = (QLabel("Avions"))
        label2.setFrameShape(QFrame.Panel)
        label3 = (QLabel("Vue de haut"))
        label3.setFrameShape(QFrame.Panel)
        label4 = (QLabel("Message"))
        label4.setFrameShape(QFrame.Panel)
        label5 = (QLabel("Piste de côté"))
        label5.setFrameShape(QFrame.Panel)
        label6 = (QLabel("Contrôles"))
        label6.setFrameShape(QFrame.Panel)
        label7 = (QLabel("Instructions"))
        label7.setFrameShape(QFrame.Panel)
        label8 = (QLabel("Actions"))
        label8.setFrameShape(QFrame.Panel)

        # Boutons
        btn_monter = QPushButton("Monter")
        btn_descendre = QPushButton("Descendre")
        btn_gauche = QPushButton("Gauche")
        btn_droite = QPushButton("Droite")

        # Même taille que les autres
        btn_gauche.setFixedHeight(60)
        btn_droite.setFixedHeight(60)

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

        layout_gauche = QVBoxLayout()
        layout_gauche.addWidget(group_controles)
        layout_gauche.addWidget(group_instructions)
        layout_gauche.addWidget(group_actions)


        av_nom = QLabel(avion.nom)
        av_alt = QLabel(str(avion.altitude))
        av_vit = QLabel(str(avion.vitesse))
        av_fuel = QLabel(str(avion.fuel))
        av_cap = QLabel(str(avion.cap))

        layout = QHBoxLayout()
        layout_droite = QVBoxLayout()
        layout_centre = QVBoxLayout()
        layout_avions = QVBoxLayout()
        btn_monter.setFixedHeight(60)
        btn_descendre.setFixedHeight(60)


        layout_droite.addWidget(label)
        layout_droite.addLayout(layout_avions)
        layout_avions.addWidget(label2)
        layout_avions.addWidget(av_nom)
        layout_avions.addWidget(av_alt)
        layout_avions.addWidget(av_vit)
        layout_avions.addWidget(av_fuel)
        layout_avions.addWidget(av_cap)
        layout_centre.addWidget(label3)
        layout_centre.addWidget(label4)
        layout_centre.addWidget(label5)
        layout_gauche.addWidget(group_actions)

        layout.addLayout(layout_droite)
        layout.addLayout(layout_centre)
        layout.addLayout(layout_gauche)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

avion=Avions.Avions("ABC123",3500,400,50,90)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()