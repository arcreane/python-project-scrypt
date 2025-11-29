# Accueil.py
import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from Jeu import MainGameWindow  # Import de la fenêtre principale du jeu
from InfoWindow import InfoWindow  # Import de la fenêtre d'informations/tutoriel

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SkyLink")  # Titre de la fenêtre

        # Image de fond
        self.background = QLabel(self)  # QLabel pour afficher l'image de fond
        self.background.setScaledContents(True)  # Redimension automatique de l'image pour remplir le label
        self.background.lower()  # Met l'image derrière tous les autres widgets (boutons)

        # Boutons principaux
        self._init_buttons()  # Création des boutons "Commencer", "Infos", "Quitter"

        # Layout principal
        self._init_layout()  # Organisation verticale/horizontale des boutons et fond

        # Musique d'accueil
        self._init_music()  # Lecture automatique de la musique à l'ouverture

    # Initialisation des boutons
    def _init_buttons(self):
        # Bouton "Commencer la partie"
        self.button = QPushButton("Commencer la partie", self)
        self.button.setCursor(Qt.PointingHandCursor)  # Curseur main au survol
        self.button.clicked.connect(self.on_button_click)  # Action au clic → lancement du jeu
        self.button.setFixedSize(400, 90)  # Taille fixe pour uniformité
        font = self.button.font()
        font.setPointSize(30)  # Taille de la police
        self.button.setFont(font)

        # Bouton "Infos"
        self.info_button = QPushButton("Infos", self)
        self.info_button.setCursor(Qt.PointingHandCursor)
        self.info_button.clicked.connect(self.show_infos)  # Action au clic → affiche InfoWindow
        self.info_button.setFixedSize(120, 40)

        # Bouton "Quitter"
        self.quit_button = QPushButton("Quitter", self)
        self.quit_button.setCursor(Qt.PointingHandCursor)
        self.quit_button.clicked.connect(self.close)  # Ferme la fenêtre
        self.quit_button.setFixedSize(120, 40)

        # Empêche la navigation clavier sur les boutons pour éviter les sélections automatiques
        for btn in (self.button, self.info_button, self.quit_button):
            btn.setFocusPolicy(Qt.NoFocus)

    # Organisation du layout
    def _init_layout(self):
        layout = QVBoxLayout(self)  # Layout principal vertical

        # Layout horizontal pour les boutons "Infos" et "Quitter" en haut à droite
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # Espace flexible à gauche → pousse les boutons à droite
        top_layout.addWidget(self.info_button)
        top_layout.addWidget(self.quit_button)
        layout.addLayout(top_layout)

        # Ajout du bouton principal centré verticalement
        layout.addStretch()  # Espace flexible avant le bouton
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        layout.addStretch()  # Espace flexible après le bouton

        self.setLayout(layout)  # Applique le layout à la fenêtre

    # Musique d'accueil
    def _init_music(self):
        self.player = QMediaPlayer()  # Lecteur audio
        self.audio_output = QAudioOutput()  # Sortie audio
        self.player.setAudioOutput(self.audio_output)  # Connecte lecteur et sortie
        self.player.setSource(QUrl.fromLocalFile("Musiques/Musique_accueil.mp3"))  # Fichier à jouer
        self.audio_output.setVolume(0.5)  # Volume à 50%
        self.player.play()  # Lecture automatique

    # Gestion du fond lors de l'affichage
    def showEvent(self, event):
        self._update_background()  # Met à jour l'image de fond
        super().showEvent(event)

    # Gestion du fond lors du redimensionnement
    def resizeEvent(self, event):
        self._update_background()  # Ajuste l'image pour remplir la nouvelle taille
        super().resizeEvent(event)

    def _update_background(self):
        """Met à jour l'image de fond pour remplir toute la fenêtre."""
        if not hasattr(self, "background") or self.background is None:
            return

        pixmap = QPixmap("Images/Fond_accueil.png")  # Charge l'image
        if pixmap.isNull():
            print("⚠️ Image introuvable")  # Alerte si l'image est absente
            return

        pixmap = pixmap.scaled(
            self.size(),  # Taille de la fenêtre
            Qt.AspectRatioMode.KeepAspectRatioByExpanding  # Remplit l'espace sans déformer
        )
        self.background.setPixmap(pixmap)  # Applique l'image au label
        self.background.setGeometry(0, 0, self.width(), self.height())  # Position et taille du label

    # Actions des boutons
    def on_button_click(self):
        print("Bonne chance !")  # Message console pour suivi
        self.player.stop()  # Arrête la musique
        self.main_window = MainGameWindow()  # Crée la fenêtre principale du jeu
        self.main_window.show()  # Affiche la fenêtre du jeu
        self.close()  # Ferme la fenêtre d'accueil

    def show_infos(self):
        info = InfoWindow(self)  # Crée la fenêtre d'informations
        info.exec()  # Bloque l'interaction avec la fenêtre principale tant que InfoWindow est ouverte


# Lancement de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crée l'application Qt
    window = Window()  # Crée la fenêtre d'accueil
    window.showFullScreen()  # Affiche en plein écran
    sys.exit(app.exec())  # Boucle principale de l'application et fermeture propre
