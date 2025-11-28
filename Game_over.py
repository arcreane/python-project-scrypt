# game_over.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt

class GameOverWidget(QWidget):
    def __init__(self, parent=None, restart_callback=None, quit_callback=None):
        super().__init__(parent)
        self.restart_callback = restart_callback
        self.quit_callback = quit_callback
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("GAME OVER")
        font = self.label.font()
        font.setPointSize(40)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: red;")
        layout.addWidget(self.label)

        # Boutons
        self.btn_restart = QPushButton("Recommencer")
        self.btn_quit = QPushButton("Quitter")
        for b in [self.btn_restart, self.btn_quit]:
            b.setFixedSize(200, 60)
            layout.addWidget(b)

        self.btn_restart.clicked.connect(self.on_restart)
        self.btn_quit.clicked.connect(self.on_quit)

        self.setLayout(layout)

    def on_restart(self):
        if self.restart_callback:
            self.restart_callback()
        self.close()

    def on_quit(self):
        if self.quit_callback:
            self.quit_callback()
        self.close()
