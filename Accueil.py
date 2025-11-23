import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QHBoxLayout
from Jeu import MainGameWindow
from InfoWindow import InfoWindow

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SkyLink")

        #Image de fond
        self.background = QLabel(self)
        self.background.setScaledContents(True)
        self.background.lower()

        #Bouton principal
        self.button = QPushButton("Commencer la partie", self)
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.clicked.connect(self.on_button_click)
        self.button.setFixedSize(400, 90)
        font = self.button.font()
        font.setPointSize(30)
        self.button.setFont(font)

        #Bouton infos
        self.info_button = QPushButton("Infos", self)
        self.info_button.setCursor(Qt.PointingHandCursor)
        self.info_button.clicked.connect(self.show_infos)
        self.info_button.setFixedSize(120, 40)

        #Bouton quitter
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

        #Musique
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("Musiques/Musique_accueil.mp3"))
        self.audio_output.setVolume(0.5)
        self.player.play()


    def showEvent(self, event):
        if not hasattr(self, "background") or self.background is None:
            return super().showEvent(event)

        pixmap = QPixmap(r"Images/Fond_accueil.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            self.background.setPixmap(pixmap)
            self.background.setGeometry(0, 0, self.width(), self.height())
        else:
            print("⚠️ Image introuvable")

        return super().showEvent(event)


    def resizeEvent(self, event):
        if not hasattr(self, "background") or self.background is None:
            return super().resizeEvent(event)

        pixmap = QPixmap("Images/Fond_accueil.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            self.background.setPixmap(pixmap)
            self.background.setGeometry(0, 0, self.width(), self.height())

        return super().resizeEvent(event)


    def on_button_click(self):
        print("Bonne chance !")
        self.player.stop()
        self.main_window = MainGameWindow()
        self.main_window.show()
        self.close()

    def show_infos(self):
        info = InfoWindow(self)
        info.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.showFullScreen()
    sys.exit(app.exec())