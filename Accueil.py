import sys
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
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
        self.button = QPushButton("Commencer la partie", self)
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.clicked.connect(self.on_button_click)
        self.button.setFixedSize(400, 90)
        font = self.button.font()
        font.setPointSize(30)
        self.button.setFont(font)

        self.info_button = QPushButton("Infos", self)
        self.info_button.setCursor(Qt.PointingHandCursor)
        self.info_button.clicked.connect(self.show_infos)
        self.info_button.setFixedSize(120, 40)

        self.quit_button = QPushButton("Quitter", self)
        self.quit_button.setCursor(Qt.PointingHandCursor)
        self.quit_button.clicked.connect(self.close)
        self.quit_button.setFixedSize(120, 40)

        # Layout principal
        layout = QVBoxLayout(self)

        # Layout horizontal pour aligner les boutons à droite
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.info_button)
        top_layout.addWidget(self.quit_button)
        layout.addLayout(top_layout)

        layout.addStretch()
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

        # Musique d'accueil
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("Musiques/Musique_accueil.mp3"))
        self.audio_output.setVolume(0.5)
        self.player.play()

    # Gestion de l'affichage du fond
    def showEvent(self, event):
        self._update_background()
        return super().showEvent(event)

    def resizeEvent(self, event):
        self._update_background()
        return super().resizeEvent(event)

    def _update_background(self):
        if not hasattr(self, "background") or self.background is None:
            return
        pixmap = QPixmap("Images/Fond_accueil.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding
            )
            self.background.setPixmap(pixmap)
            self.background.setGeometry(0, 0, self.width(), self.height())
        else:
            print("⚠️ Image introuvable")

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
