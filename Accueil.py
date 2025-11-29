# Accueil.py
import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from Jeu import MainGameWindow
from InfoWindow import InfoWindow


# Classe : Fenêtre Accueil
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SkyLink")

        # Image de fond
        self.background = QLabel(self)
        self.background.setScaledContents(True)
        self.background.lower()

        # Boutons principaux
        self._init_buttons()

        # Layout principal
        self._init_layout()

        # Musique d'accueil
        self._init_music()

    # Initialisation des boutons
    def _init_buttons(self):
        # Bouton "Commencer la partie"
        self.button = QPushButton("Commencer la partie", self)
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.clicked.connect(self.on_button_click)
        self.button.setFixedSize(400, 90)
        font = self.button.font()
        font.setPointSize(30)
        self.button.setFont(font)

        # Bouton "Infos"
        self.info_button = QPushButton("Infos", self)
        self.info_button.setCursor(Qt.PointingHandCursor)
        self.info_button.clicked.connect(self.show_infos)
        self.info_button.setFixedSize(120, 40)

        # Bouton "Quitter"
        self.quit_button = QPushButton("Quitter", self)
        self.quit_button.setCursor(Qt.PointingHandCursor)
        self.quit_button.clicked.connect(self.close)
        self.quit_button.setFixedSize(120, 40)

        # 🔥 Empêcher navigation clavier
        for btn in (self.button, self.info_button, self.quit_button):
            btn.setFocusPolicy(Qt.NoFocus)

    # Initialisation du layout
    def _init_layout(self):
        layout = QVBoxLayout(self)

        # Layout horizontal pour boutons "Infos" et "Quitter" à droite
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.info_button)
        top_layout.addWidget(self.quit_button)
        layout.addLayout(top_layout)

        layout.addStretch()
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    # Initialisation de la musique d'accueil
    def _init_music(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("Musiques/Musique_accueil.mp3"))
        self.audio_output.setVolume(0.5)
        self.player.play()

    # Gestion de l'affichage du fond
    def showEvent(self, event):
        self._update_background()
        super().showEvent(event)

    def resizeEvent(self, event):
        self._update_background()
        super().resizeEvent(event)

    def _update_background(self):
        """Met à jour l'image de fond pour remplir la fenêtre"""
        if not hasattr(self, "background") or self.background is None:
            return

        pixmap = QPixmap("Images/Fond_accueil.png")
        if pixmap.isNull():
            print("⚠️ Image introuvable")
            return

        pixmap = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding
        )
        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0, self.width(), self.height())

    # Actions des boutons
    def on_button_click(self):
        print("Bonne chance !")
        self.player.stop()
        self.main_window = MainGameWindow()
        self.main_window.show()
        self.close()

    def show_infos(self):
        info = InfoWindow(self)
        info.exec()


# Lancement de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.showFullScreen()
    sys.exit(app.exec())
