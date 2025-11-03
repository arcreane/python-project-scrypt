import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QPushButton Example")
        self.setFixedSize(QSize(1500, 800))

        #Image de fond
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1500, 800)
        pixmap = QPixmap(r"ecran_fond_interface.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            self.background.setPixmap(pixmap)
        else:
            print("⚠️ Image non trouvée : vérifie le chemin")
        self.background.setScaledContents(True)

        #Bouton
        self.button = QPushButton("Commencer la partie", self)
        self.button.clicked.connect(self.on_button_click)
        self.button.setFixedSize(400, 90)

        font = self.button.font()
        font.setPointSize(30)
        self.button.setFont(font)

        #Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.background.lower()

    def resizeEvent(self, event):
        if hasattr(self, 'background'):
            self.background.setGeometry(0, 0, self.width(), self.height())
            pixmap = QPixmap("Scrypt/ecran_fond_interface.png")
            if not pixmap.isNull():
                pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
                self.background.setPixmap(pixmap)
        return super().resizeEvent(event)

    def on_button_click(self):
        print("Bonne chance !")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
