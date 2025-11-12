import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap,QIcon
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel,QHBoxLayout


class menu0(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boutons")
        self.setFixedSize(QSize(800, 500))  # Taille de la fenêtre

        #création des 3 boutons
        bouton1 = QPushButton()
        bouton2 = QPushButton()
        bouton3 = QPushButton()

        # ajout images
        bouton1.setIcon(QIcon("image1.png"))
        bouton2.setIcon(QIcon("image2.png"))
        bouton3.setIcon(QIcon("image3.png"))

        for bouton in (bouton1, bouton2, bouton3):
            bouton.setFixedSize(45, 20)  # taille du bouton
            bouton.setIconSize(QSize(50, 50))  # taille de l'image


        # Layout horizontal pour aligner les boutons
        h_layout = QHBoxLayout()
        h_layout.addWidget(bouton1)
        h_layout.addWidget(bouton2)
        h_layout.addWidget(bouton3)
        h_layout.setSpacing(8)

        #layout principal pour placer le tout en haut à droite
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(h_layout)
        main_layout.addStretch()  # pousse le contenu restant vers le bas (ici après les boutons)
        main_layout.setAlignment(h_layout, Qt.AlignmentFlag.AlignRight)
        self.setLayout(main_layout)


# Lancement de l’application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = menu0()
    window.show()
    sys.exit(app.exec())
